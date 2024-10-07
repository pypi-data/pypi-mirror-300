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
        self.assistant_name = "Assistant"       # Default assistant name
        self.message_accumulator = {}           # Store message chunks
        self.printed_message_ids = set()        # Track printed message IDs
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
        Handles incoming message deltas (streaming content) and prints the assistant's responses.
        """
        message_id = event.data.id
        message_content = ''

        # If it's a new message, initialize it in the accumulator
        if message_id not in self.message_accumulator:
            self.message_accumulator[message_id] = ''

        # Print assistant name only once, when a new message starts
        if message_id not in self.printed_message_ids:
            print(f"\n{self.assistant_name}: ", end='', flush=True)
            self.printed_message_ids.add(message_id)  # Mark this message as having printed the assistant name

        # Process the message delta
        if hasattr(event.data.delta, 'content'):
            for block in event.data.delta.content:
                if block.type == 'text' and hasattr(block.text, 'value'):
                    message_content += block.text.value
                    print(block.text.value, end='', flush=True)  # Print the chunk

        # Accumulate the message content
        self.message_accumulator[message_id] += message_content

        # Log the received content for debugging
        if message_content:
            self.logger.info(f"SEH - Message content for ID {message_id}: {message_content}")

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
                event_handler=StreamEventHandler(self.client, self.logger, self.run_manager, self.assistant_name),
            ) as stream:
                for text_delta in stream.text_deltas:
                    # Only print actual content from the assistant
                    if text_delta.content:  # Check if the delta contains valid content
                        print(text_delta.content, end='', flush=True)  # Print each chunk of the message
                print()  # Ensure newline once the response completes
        except Exception as e:
            # Log any errors but do not mix with the assistant's response
            self.logger.error(f"Error submitting tool outputs for run {run_id}: {str(e)}", exc_info=True)
