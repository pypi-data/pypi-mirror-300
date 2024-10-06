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
        self.logger = logger  # Now properly passing the logger

    def on_event(self, event):
        """
        Handles events coming from the streaming API.
        Specifically, it triggers when an event with 'requires_action' is received.
        """
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id  # Retrieve the run ID from the event data
            self.stream_handle_requires_action(event.data, run_id)


    def stream_handle_requires_action(self, data, run_id):
        """
        Handles the required actions for a given run using event streaming.
        
        Processes tool calls by dynamically retrieving the tool outputs
        and submitting them via the streaming API.

        Args:
            data (EventData): The event data that contains required action details.
            run_id (str): The ID of the run for which actions are required.
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

        Args:
            tool_outputs (list): The list of tool outputs to be submitted.
            run_id (str): The ID of the run for which the tool outputs are submitted.
        """
        try:
            # Use the stream to submit the tool outputs
            with self.client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=StreamEventHandler(self.client, self.logger, self.run_manager),
            ) as stream:
                for text_delta in stream.text_deltas:
                    # Print the streamed response output incrementally
                    print(text_delta, end="", flush=True)
                print()  # Print a newline once done
        except Exception as e:
            self.logger.error(f"Error submitting tool outputs for run {run_id}: {str(e)}", exc_info=True)
