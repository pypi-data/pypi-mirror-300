# flexiai/core/flexi_managers/stream_event_handler.py
import json
from pydantic import BaseModel
from typing import Optional, List
from openai import AssistantEventHandler

class TextDelta(BaseModel):
    value: str  # Represents the value of the text in a message delta

class TextDeltaBlock(BaseModel):
    index: int  # Index of the delta block within the message
    type: str  # Type of the block, e.g., 'text'
    text: Optional[TextDelta]  # Optional text delta if the block contains text

class MessageDelta(BaseModel):
    content: List[TextDeltaBlock]  # List of content blocks in the message delta

class MessageDeltaEvent(BaseModel):
    id: str  # Unique identifier for the message event
    delta: Optional[MessageDelta]  # Optional message delta containing content

class EventModel(BaseModel):
    event: str  # Type of event, e.g., 'thread.message.delta'
    data: MessageDeltaEvent  # Data associated with the event

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
        self.printed_message_ids = set()  # Track printed message IDs to avoid printing duplicates
        self.processed_event_ids = set()  # Track processed event IDs to avoid handling duplicates
        super().__init__()  # Call the parent class constructor

    def set_assistant_name(self, name):
        """
        Update the assistant's name dynamically.
        
        :param name: The new name for the assistant
        """
        self.assistant_name = name

    def _init(self, stream):
        """
        This method initializes the stream for the event handler.
        
        :param stream: The stream to initialize for handling events
        """
        self.__stream = stream
        super()._init(stream)

    def on_event(self, event):
        """
        Handles events coming from the streaming API.
        Specifically, it triggers when an event with 'requires_action' or message content is received.
        
        :param event: The incoming event from the streaming API
        """
        try:
            # Parse the event using Pydantic model to ensure proper schema
            parsed_event = EventModel(**event)
        except Exception as e:
            self.logger.error(f"[on_event] Error parsing event: {str(e)}", exc_info=True)
            return

        event_identifier = (parsed_event.event, parsed_event.data.id)

        # Avoid handling the same event twice
        if event_identifier in self.processed_event_ids:
            return

        # Handle specific types of events
        if parsed_event.event == "thread.run.requires_action":
            run_id = parsed_event.data.id  # Retrieve the run ID from the event data
            self.logger.info(f"[on_event] Run requires action: {run_id}")
            self.stream_handle_requires_action(parsed_event.data, run_id)
        elif parsed_event.event == "thread.message.delta":
            # Pass the event to the message handler and print the assistant's response
            self.handle_message_delta(parsed_event)

        # Track processed event to avoid duplication
        self.processed_event_ids.add(event_identifier)  # Track event early to avoid reprocessing in case of errors

    def handle_message_delta(self, parsed_event):
        """
        Handles incoming message deltas (streaming content) and prints the assistant's responses immediately.
        
        :param parsed_event: Parsed event containing message delta information
        """
        # Log the event to debug duplicates
        self.logger.info(f"[handle_message_delta] Received event: {parsed_event}")

        # Print assistant name only once at the start of a new message
        if parsed_event.data.id not in self.printed_message_ids:
            self.logger.info(f"[handle_message_delta] Processing message with ID: {parsed_event.data.id}")  # Debug log for message ID
            print(f"\n{self.assistant_name}: ", end='', flush=True)  # Print assistant name once
            self.printed_message_ids.add(parsed_event.data.id)  # Mark this message as printed with assistant name

        # Process the message delta and print content immediately
        if parsed_event.data.delta:
            for block in parsed_event.data.delta.content:
                if block.type == 'text' and block.text and block.text.value:
                    # Print each chunk directly as it arrives
                    chunk = block.text.value
                    self.logger.info(f"[handle_message_delta] Received message chunk: {chunk}")  # Debug log for message chunk
                    print(chunk, end='', flush=True)  # Print the message chunk
                else:
                    self.logger.info("[handle_message_delta] No valid content found in this message block.")
        else:
            self.logger.info("[handle_message_delta] No delta content found in the event.")

        # Once the message is completed, ensure newline after the response
        if parsed_event.event == "thread.message.completed":
            self.logger.info(f"[handle_message_delta] Message completed: {parsed_event.data.id}")  # Log message completion
            print()  # Ensure new line after the assistant's response completes
            self.processed_event_ids.add(parsed_event.data.id)  # Mark this message as completed

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
            tool_calls = data.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            # Check if we need to execute tool calls in parallel or sequentially
            use_parallel = len(tool_calls) > 1

            if use_parallel:  # Limit parallel tasks to prevent overwhelming the system
                self.logger.info("[stream_handle_requires_action] Executing tool calls in parallel mode.")
                try:
                    # Prepare tasks for parallel execution
                    tasks = [
                        {
                            'function_name': tool_call.function.name,
                            'parameters': json.loads(tool_call.function.arguments)
                        }
                        for tool_call in tool_calls
                    ]
                    # Execute the tasks in parallel
                    results = self.run_manager.call_parallel_functions(tasks)

                    # Prepare tool outputs based on the results
                    for tool_call, result in zip(tool_calls, results):
                        tool_outputs.append(self.run_manager.prepare_tool_output(tool_call, result))
                except Exception as e:
                    self.logger.error(f"[stream_handle_requires_action] Error during parallel execution: {str(e)}", exc_info=True)
                    raise
            else:
                # Sequential execution of tool calls
                for tool_call in tool_calls:
                    try:
                        function_name = tool_call.function.name
                        arguments = json.loads(tool_call.function.arguments)

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
                    except Exception as e:
                        # Prepare the output with an error if the tool call fails
                        tool_outputs.append(self.run_manager.prepare_tool_output(tool_call, e, success=False))
                        self.logger.error(f"[stream_handle_requires_action] Error executing tool call {tool_call.id}: {str(e)}", exc_info=True)

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
                        print(text_delta.content, end='', flush=True)  # Print the text delta content as it arrives
        except Exception as e:
            self.logger.error(f"[stream_submit_tool_outputs] Error submitting tool outputs for run {run_id}: {str(e)}", exc_info=True)