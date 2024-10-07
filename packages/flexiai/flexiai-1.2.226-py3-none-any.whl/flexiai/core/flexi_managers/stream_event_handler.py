# flexiai/core/flexi_managers/stream_event_handler.py
import json
from openai import AssistantEventHandler

class StreamEventHandler(AssistantEventHandler):
    def __init__(self, client, logger, run_manager, assistant_name):
        """
        Initializes the StreamEventHandler with the necessary dependencies.
        
        :param client: The API client for interacting with the backend
        :param logger: Logger instance for logging events and errors
        :param run_manager: Manager for handling assistant runs and tool calls
        :param assistant_name: Name of the assistant, used for printing responses
        """
        self.client = client
        self.logger = logger
        self.run_manager = run_manager
        self.assistant_name = assistant_name  # Accept assistant_name here
        super().__init__()  # Call the parent class constructor
        
        # Initialize the logger to track stream behavior
        self.logger.info("StreamEventHandler initialized successfully.")

    def set_assistant_name(self, name):
        """
        Update the assistant's name dynamically.
        
        :param name: The new name for the assistant
        """
        self.assistant_name = name
        self.logger.info(f"Assistant name updated to: {name}")

    def _init(self, stream):
        """
        This method initializes the stream for the event handler.
        
        :param stream: The stream to initialize for handling events
        """
        self.__stream = stream
        super()._init(stream)
        self.logger.info("Stream initialized for event handling.")

    def on_event(self, event):
        """
        Handles events coming from the streaming API.
        Specifically, it triggers when an event with 'requires_action' or message content is received.
        
        :param event: The incoming event from the streaming API
        """
        try:
            # Ensure event is a dictionary before parsing
            if not isinstance(event, dict):
                event = event.to_dict()

            # Log the received event for debugging
            self.logger.info(f"[on_event] Received event: {event}")

            # Check for necessary keys before proceeding
            if 'event' not in event or 'data' not in event:
                self.logger.error(f"[on_event] Malformed event: Missing 'event' or 'data' key.")
                return

            # Extract event type and data
            event_type = event['event']
            event_data = event['data']

            # Handle specific types of events
            if event_type == "thread.run.requires_action":
                run_id = event_data.get('id')  # Retrieve the run ID from the event data
                if run_id:
                    self.logger.info(f"[on_event] Run requires action: {run_id}")
                    self.stream_handle_requires_action(event_data, run_id)
                else:
                    self.logger.error(f"[on_event] 'id' missing in 'data' for requires_action event.")
            elif event_type == "thread.message.delta":
                # Pass the event to the message handler and print the assistant's response
                self.handle_message_delta(event_data)

        except Exception as e:
            self.logger.error(f"[on_event] Error processing event: {str(e)}", exc_info=True)

    def handle_message_delta(self, event_data):
        """
        Handles incoming message deltas (streaming content) and prints the assistant's responses immediately.
        
        :param event_data: Parsed event containing message delta information
        """
        # Log the event to debug behavior
        self.logger.info(f"[handle_message_delta] Received event data: {event_data}")

        # Extract delta content
        delta = event_data.get('delta')

        if not delta:
            self.logger.error(f"[handle_message_delta] Missing 'delta' in event data.")
            return

        # Print assistant name only once at the start of a new message
        print(f"\n{self.assistant_name}: ", end='', flush=True)  # Print assistant name once

        # Process the message delta and print content immediately
        for block in delta.get('content', []):
            if block.get('type') == 'text' and 'text' in block and 'value' in block['text']:
                # Print each chunk directly as it arrives
                chunk = block['text']['value']
                self.logger.info(f"[handle_message_delta] Received message chunk: {chunk}")  # Debug log for message chunk
                print(chunk, end='', flush=True)  # Print the message chunk
            else:
                self.logger.info("[handle_message_delta] No valid content found in this message block.")

        # Ensure newline after the response completes
        if event_data.get('status') == "completed":
            self.logger.info("[handle_message_delta] Message completed.")  # Log message completion
            print()  # Ensure new line after the assistant's response completes

    def start_streaming_response(self, thread_id, assistant_id):
        """
        Start streaming response from the assistant and handle the streaming process.
        Uses the instance of StreamEventHandler.
        
        :param thread_id: The ID of the thread for which the response is being streamed
        :param assistant_id: The ID of the assistant providing the response
        """
        self.logger.info(f"[start_streaming_response] Starting assistant run for thread {thread_id} with assistant {assistant_id}.")

        # Start the stream with the event handler
        try:
            with self.client.beta.threads.runs.stream(
                thread_id=thread_id,
                assistant_id=assistant_id,
                event_handler=self  # Use the current instance (self) as the event handler
            ) as stream:
                self.logger.info("[start_streaming_response] Stream started successfully.")  # Log stream start
                # Process each event as it arrives in the stream
                for event in stream:  # Consider adding a timeout or retry mechanism to prevent blocking
                    self.logger.info(f"[start_streaming_response] Processing event: {event}")
                    self.on_event(event)  # Handle each event using the on_event method
        except Exception as e:
            self.logger.error(f"[start_streaming_response] Unexpected error during streaming: {str(e)}", exc_info=True)  # Add context for easier debugging

    def stream_handle_requires_action(self, data, run_id):
        """
        Handles the required actions for a given run using event streaming.
        Submits tool outputs cleanly without logging in the streamed content.
        
        :param data: Data related to the required action for the run
        :param run_id: The ID of the run requiring action
        """
        try:
            tool_calls = data.get('required_action', {}).get('submit_tool_outputs', {}).get('tool_calls', [])
            tool_outputs = []

            # Check if we need to execute tool calls in parallel or sequentially
            use_parallel = len(tool_calls) > 1

            if use_parallel:  # Limit parallel tasks to prevent overwhelming the system
                self.logger.info("[stream_handle_requires_action] Executing tool calls in parallel mode.")
                try:
                    # Prepare tasks for parallel execution
                    tasks = [
                        {
                            'function_name': tool_call['function']['name'],
                            'parameters': json.loads(tool_call['function']['arguments'])
                        }
                        for tool_call in tool_calls
                    ]
                    # Execute the tasks in parallel
                    results = self.run_manager.call_parallel_functions(tasks)

                    # Prepare tool outputs based on the results
                    for tool_call, result in zip(tool_calls, results):
                        tool_outputs.append(self.run_manager.prepare_tool_output(tool_call, result))
                        self.logger.info(f"[stream_handle_requires_action] Tool call result: {result}")
                except Exception as e:
                    self.logger.error(f"[stream_handle_requires_action] Error during parallel execution: {str(e)}", exc_info=True)
                    raise
            else:
                # Sequential execution of tool calls
                for tool_call in tool_calls:
                    try:
                        function_name = tool_call['function']['name']
                        arguments = json.loads(tool_call['function']['arguments'])

                        # Determine the type of action to perform
                        action_type = self.run_manager.determine_action_type(function_name)

                        if action_type == "call_assistant":
                            # Call the assistant with the provided arguments
                            result = self.run_manager.call_assistant_with_arguments(function_name, **arguments)
                        else:
                            # Execute a personal function with the provided arguments
                            result = self.run_manager.execute_personal_function_with_arguments(function_name, **arguments)

                        # Prepare the output for the tool call
                        tool_outputs.append(self.run_manager.prepare_tool_output(tool_call, result))
                        self.logger.info(f"[stream_handle_requires_action] Tool call executed: {tool_call['id']} with result: {result}")
                    except Exception as e:
                        # Prepare the output with an error if the tool call fails
                        tool_outputs.append(self.run_manager.prepare_tool_output(tool_call, e, success=False))
                        self.logger.error(f"[stream_handle_requires_action] Error executing tool call {tool_call['id']}: {str(e)}", exc_info=True)

            # After tool outputs are generated, stream them properly without mixing logs
            self.stream_submit_tool_outputs(tool_outputs, run_id)

        except Exception as e:
            self.logger.error(f"[stream_handle_requires_action] Error handling action for run {run_id}: {str(e)}", exc_info=True)

    def stream_submit_tool_outputs(self, tool_outputs, run_id):
        """
        Submits the tool outputs using a streaming mechanism. Ensure that the streaming
        prints only the assistant response and not logging information.
        
        :param tool_outputs: The outputs generated by the tool calls
        :param run_id: The ID of the run for which the outputs are being submitted
        """
        try:
            with self.client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=self  # Reuse the current event handler
            ) as stream:
                for text_delta in stream.text_deltas:
                    if text_delta.content:
                        self.logger.info(f"[stream_submit_tool_outputs] Streaming content: {text_delta.content}")
                        print(text_delta.content, end='', flush=True)  # Print the text delta content as it arrives
        except Exception as e:
            self.logger.error(f"[stream_submit_tool_outputs] Error submitting tool outputs for run {run_id}: {str(e)}", exc_info=True)