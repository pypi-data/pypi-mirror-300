# flexiai/core/flexi_managers/stream_event_handler.py
import json
from openai import AssistantEventHandler


class StreamEventHandler(AssistantEventHandler):
    def __init__(self, client, logger, run_manager):
        """
        Initializes the StreamEventHandler with the necessary dependencies.
        """
        self.client = client
        self.run_manager = run_manager
        self.logger = logger
        self.assistant_name = "Assistant"   # Default assistant name
        self.message_accumulator = {}       # Store message chunks
        self.printed_message_ids = set()    # Track printed message IDs
        super().__init__()


    def set_assistant_name(self, name):
        """
        Update the assistant's name dynamically.
        """
        self.assistant_name = name


    def _init(self, stream):
        """
        This method initializes the stream for the event handler.
        """
        self.__stream = stream
        super()._init(stream)


    def on_event(self, event):
        """
        Handles events coming from the streaming API.
        Specifically, it triggers when an event with 'requires_action' or message content is received.
        """
        if hasattr(event, 'event') and event.event == "thread.run.requires_action":
            run_id = event.data.id  # Retrieve the run ID from the event data
            self.logger.info(f"Run requires action: {run_id}")
            self.stream_handle_requires_action(event.data, run_id)
        elif hasattr(event, 'event') and event.event == "thread.message.delta":
            # Pass the event to the message handler and print the assistant's response
            self.handle_message_delta(event)


def handle_message_delta(self, event):
    """
    Handles incoming message deltas (streaming content) and prints the assistant's responses immediately.
    """
    # Print assistant name only once at the start of a new message
    if event.data.id not in self.printed_message_ids:
        print(f"\n{self.assistant_name}: ", end='', flush=True)
        self.printed_message_ids.add(event.data.id)  # Mark this message as printed with assistant name

    # Process the message delta and print content immediately
    if hasattr(event.data.delta, 'content'):
        for block in event.data.delta.content:
            if block.type == 'text' and hasattr(block.text, 'value'):
                # Print each chunk directly as it arrives
                chunk = block.text.value
                print(chunk, end='', flush=True)

    # Once the message is completed, ensure newline after the response
    elif hasattr(event, 'event') and event.event == "thread.message.completed":
        print()  # Ensure new line after the assistant's response completes




    def process_streamed_messages(self, stream):
        """
        Processes streamed messages dynamically and prints them with the provided assistant name.
        Ensures that the assistant's name is printed only once per message.
        """
        printed_message_ids = set()  # Track which messages have had the assistant's name printed

        for event in stream:
            if hasattr(event, 'event') and event.event == "thread.message.delta":
                message_id = event.data.id

                # If it's a new message, initialize it in the accumulator
                if message_id not in self.message_accumulator:
                    self.message_accumulator[message_id] = ''

                # Process the message delta and accumulate chunks
                if hasattr(event.data.delta, 'content'):
                    message_content = ''
                    for block in event.data.delta.content:
                        if block.type == 'text' and hasattr(block.text, 'value'):
                            message_content += block.text.value

                    # Accumulate the message content
                    if message_content:
                        self.message_accumulator[message_id] += message_content

            # Once the message is completed, ensure the message is fully printed
            elif hasattr(event, 'event') and event.event == "thread.message.completed":
                message_id = event.data.id

                if message_id in self.message_accumulator:
                    # Print the assistant's name and the full message once it's complete
                    print(f"\n{self.assistant_name}: {self.message_accumulator[message_id]}")
                    self.logger.info(f"Full message from {self.assistant_name}: {self.message_accumulator[message_id]}")

                    # Remove the message from the accumulator after printing
                    del self.message_accumulator[message_id]
                    printed_message_ids.discard(message_id)


    def start_streaming_response(self, thread_id, assistant_id):
        """
        Start streaming response from the assistant and handle the streaming process.
        """
        self.logger.info(f"Starting assistant run for thread {thread_id} with assistant {assistant_id}.")

        # Start the stream with the event handler
        try:
            with self.client.beta.threads.runs.stream(
                thread_id=thread_id,
                assistant_id=assistant_id,
                event_handler=self
            ) as stream:
                # Process and print the messages
                self.process_streamed_messages(stream)

                # After assistant finishes the response, move the user input to the next line
                print()  # Ensure new line after assistant's response
        except Exception as e:
            self.logger.error(f"Unexpected error during streaming: {str(e)}", exc_info=True)


    def stream_handle_requires_action(self, data, run_id):
        """
        Handles the required actions for a given run using event streaming.
        Submits tool outputs cleanly without logging in the streamed content.
        """
        try:
            tool_calls = data.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            # Check if we need to execute tool calls in parallel or sequentially
            use_parallel = len(tool_calls) > 1

            if use_parallel:
                self.logger.info("Executing tool calls in parallel mode.")
                try:
                    tasks = [
                        {
                            'function_name': tool_call.function.name,
                            'parameters': json.loads(tool_call.function.arguments)
                        }
                        for tool_call in tool_calls
                    ]
                    # Using your RAG pipeline parallel tool execution
                    results = self.run_manager.call_parallel_functions(tasks)

                    for tool_call, result in zip(tool_calls, results):
                        tool_outputs.append(self.run_manager.prepare_tool_output(tool_call, result))
                except Exception as e:
                    self.logger.error(f"Error during parallel execution: {str(e)}", exc_info=True)
                    raise
            else:
                # Sequential execution of tool calls
                for tool_call in tool_calls:
                    try:
                        function_name = tool_call.function.name
                        arguments = json.loads(tool_call.function.arguments)

                        # Determine whether to use a personal or assistant function
                        action_type = self.run_manager.determine_action_type(function_name)

                        if action_type == "call_assistant":
                            result = self.run_manager.call_assistant_with_arguments(function_name, **arguments)
                        else:
                            result = self.run_manager.execute_personal_function_with_arguments(function_name, **arguments)

                        tool_outputs.append(self.run_manager.prepare_tool_output(tool_call, result))
                    except Exception as e:
                        tool_outputs.append(self.run_manager.prepare_tool_output(tool_call, e, success=False))
                        self.logger.error(f"Error executing tool call {tool_call.id}: {str(e)}", exc_info=True)

            # After tool outputs are generated, stream them properly without mixing logs
            self.stream_submit_tool_outputs(tool_outputs, run_id)

        except Exception as e:
            self.logger.error(f"Error handling action for run {run_id}: {str(e)}", exc_info=True)


    def stream_submit_tool_outputs(self, tool_outputs, run_id):
        """
        Submits the tool outputs using a streaming mechanism. Ensure that the streaming
        prints only the assistant response and not logging information.
        """
        try:
            with self.client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=self,  # No need to create a new instance; reuse the current event handler
            ) as stream:
                for text_delta in stream.text_deltas:
                    # Only print actual content from the assistant
                    if text_delta.content:  # Check if the delta contains valid content
                        print(text_delta.content, end='', flush=True)  # Print each chunk of the message
                print()  # Ensure newline once the response completes
        except Exception as e:
            # Log any errors but do not mix with the assistant's response
            self.logger.error(f"Error submitting tool outputs for run {run_id}: {str(e)}", exc_info=True)
