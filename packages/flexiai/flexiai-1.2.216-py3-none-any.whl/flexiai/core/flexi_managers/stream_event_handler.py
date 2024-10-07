# flexiai/core/flexi_managers/stream_event_handler.py
from openai import AssistantEventHandler
import json

class StreamEventHandler(AssistantEventHandler):
    def __init__(self, client, logger, run_manager):
        """
        Initializes the StreamEventHandler with the necessary dependencies.
        """
        self.client = client
        self.run_manager = run_manager
        self.logger = logger
        super().__init__()

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
        # self.logger.info(f"Event received: {event}")
        
        if hasattr(event, 'event') and event.event == "thread.run.requires_action":
            run_id = event.data.id  # Retrieve the run ID from the event data
            self.logger.info(f"Run requires action: {run_id}")
            self.stream_handle_requires_action(event.data, run_id)
        elif hasattr(event, 'event') and event.event == "thread.message.delta":
            # Pass the event to the message handler and print the assistant's response
            self.handle_message_delta(event)


    def handle_message_delta(self, event):
        """
        Handles incoming message deltas (streaming content) and logs the assistant's responses.
        Does not print immediately to avoid incomplete message printing.
        """
        message_id = event.data.id
        message_content = ''

        # Check if the message contains content (this could be streaming chunks)
        if hasattr(event.data.delta, 'content'):
            for block in event.data.delta.content:
                if block.type == 'text' and hasattr(block.text, 'value'):
                    message_content += block.text.value

        # Log the received content but don't print yet
        if message_content:
            self.logger.info(f"SEH - Message content for ID {message_id}: {message_content}")


    def stream_handle_requires_action(self, data, run_id):
        """
        Handles the required actions for a given run using event streaming.
        
        Processes tool calls by dynamically retrieving the tool outputs
        and submitting them via the streaming API.
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

            # Submit the tool outputs via streaming
            self.stream_submit_tool_outputs(tool_outputs, run_id)

        except Exception as e:
            self.logger.error(f"Error handling action for run {run_id}: {str(e)}", exc_info=True)


    def stream_submit_tool_outputs(self, tool_outputs, run_id):
        """
        Submits the tool outputs using a streaming mechanism.
        
        Utilizes OpenAI's `submit_tool_outputs_stream` helper to process the outputs
        in a streaming fashion, allowing real-time responses.
        """
        try:
            with self.client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=StreamEventHandler(self.client, self.logger, self.run_manager),
            ) as stream:
                for text_delta in stream.text_deltas:
                    # Prefix the assistant's name to the tool output message
                    print(f"{self.logger.name}: {text_delta}", end='', flush=True)
                # print()  # Print a newline once done
        except Exception as e:
            self.logger.error(f"Error submitting tool outputs for run {run_id}: {str(e)}", exc_info=True)

