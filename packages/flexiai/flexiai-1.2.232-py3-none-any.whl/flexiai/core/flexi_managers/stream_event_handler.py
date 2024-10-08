# flexiai/core/flexi_managers/stream_event_handler.py
import json
from typing_extensions import override
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

        # Track processed event and message IDs to avoid duplicates
        self.processed_event_ids = set()
        self.processed_message_ids = set()

    def set_assistant_name(self, name):
        """
        Update the assistant's name dynamically.
        
        :param name: The new name for the assistant
        """
        self.assistant_name = name
        self.logger.info(f"Assistant name updated to: {name}")

    @override
    def on_text_created(self, text) -> None:
        """
        Handles the event when initial text is created.
        
        :param text: The initial text created by the assistant
        """
        print(f"\n{self.assistant_name}: {text}", end='', flush=True)
        self.logger.debug(f"[on_text_created] Initial text: {text}")

    @override
    def on_text_delta(self, delta, snapshot):
        """
        Handles the streaming text deltas coming from the assistant.
        
        :param delta: The delta text coming in the stream
        :param snapshot: The snapshot of the current state
        """
        print(delta.value, end='', flush=True)
        self.logger.debug(f"[on_text_delta] Delta text: {delta.value}")

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
                stream.until_done()  # Wait until the stream is complete
        except Exception as e:
            self.logger.error(f"[start_streaming_response] Unexpected error during streaming: {str(e)}", exc_info=True)  # Add context for easier debugging

    def handle_requires_action(self, event_data):
        """
        Handles the required actions for a given run using event streaming.
        Submits tool outputs cleanly without logging in the streamed content.
        
        :param event_data: Data related to the required action for the run
        """
        run_id = event_data.get('id')
        if not run_id:
            self.logger.error(f"[handle_requires_action] 'id' missing in 'data' for requires_action event.")
            return

        self.logger.info(f"[handle_requires_action] Run requires action: {run_id}")
        
        try:
            tool_calls = event_data.get('required_action', {}).get('submit_tool_outputs', {}).get('tool_calls', [])
            tool_outputs = []

            # Check if we need to execute tool calls in parallel or sequentially
            use_parallel = len(tool_calls) > 1

            if use_parallel:  # Limit parallel tasks to prevent overwhelming the system
                self.logger.info("[handle_requires_action] Executing tool calls in parallel mode.")
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
                        self.logger.info(f"[handle_requires_action] Tool call result: {result}")
                except Exception as e:
                    self.logger.error(f"[handle_requires_action] Error during parallel execution: {str(e)}", exc_info=True)
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
                        self.logger.info(f"[handle_requires_action] Tool call executed: {tool_call['id']} with result")
                    except Exception as e:
                        self.logger.error(f"[handle_requires_action] Error executing tool call {tool_call['id']}: {str(e)}", exc_info=True)

        except Exception as e:
            self.logger.error(f"[handle_requires_action] Error handling action for run {run_id}: {str(e)}", exc_info=True)
