# flexiai/core/flexiai_client.py
import asyncio
import logging
from flexiai.assistant_actions.functions_registry import FunctionRegistry
from flexiai.credentials.credential_manager import CredentialManager
from flexiai.core.flexi_managers.message_manager import MessageManager
from flexiai.core.flexi_managers.run_manager import RunManager
from flexiai.core.flexi_managers.session_manager import SessionManager
from flexiai.core.flexi_managers.thread_manager import ThreadManager
from flexiai.core.flexi_managers.vector_store_manager import VectorStoreManager
from flexiai.core.flexi_managers.local_vector_store_manager import LocalVectorStoreManager
from flexiai.core.flexi_managers.multi_agent_system import MultiAgentSystemManager
from flexiai.core.flexi_managers.embedding_manager import EmbeddingManager
from flexiai.core.flexi_managers.images_manager import ImagesManager
from flexiai.core.flexi_managers.completions_manager import CompletionsManager
from flexiai.core.flexi_managers.assistant_manager import AssistantManager
from flexiai.core.flexi_managers.audio_manager import (
    SpeechToTextManager,
    TextToSpeechManager,
    AudioTranscriptionManager,
    AudioTranslationManager
)
from flexiai.core.flexi_managers.stream_event_handler import StreamEventHandler
from flexiai.cfg.config import Config


class FlexiAI:
    """
    FlexiAI class is the central hub for managing different AI-related operations
    such as thread management, message management, run management, session management,
    vector store management, and image generation.
    """

    def __init__(self):
        """
        Initializes the FlexiAI class and its associated managers.
        """
        # Set up the logger for the class
        self.logger = logging.getLogger(__name__)
        # Load configuration from the config file
        self.config = Config()
        self.logger.info("Configuration loaded successfully.")

        # Phase 1: Create core components
        # Credential manager handles authentication and provides the client
        self.credential_manager = CredentialManager()
        self.client = self.credential_manager.client

        # Initialize managers that don't depend on RunManager yet
        # ThreadManager handles the threads of conversation
        self.thread_manager = ThreadManager(self.client, self.logger)
        # MessageManager handles the messaging operations within threads
        self.message_manager = MessageManager(self.client, self.logger)
        # CompletionsManager manages the completion generation tasks
        self.completions_manager = CompletionsManager(self.client, self.logger)
        # AssistantManager manages various assistant-related operations
        self.assistant_manager = AssistantManager(self.client, self.logger)

        # Initialize the multi-agent system manager and function registry without RunManager for now
        # MultiAgentSystemManager manages interactions between different agents in the system
        self.multi_agent_system = MultiAgentSystemManager(
            self.client, self.logger, self.thread_manager, None, self.message_manager
        )
        # FunctionRegistry manages the functions used by the assistant
        self.function_registry = FunctionRegistry(self.multi_agent_system, None)

        # Phase 2: Now create RunManager and inject dependencies into function_registry and multi_agent_system
        # RunManager handles the execution of runs (i.e., tasks or interactions)
        self.run_manager = RunManager(self.client, self.logger, self.message_manager, self.function_registry)

        # Inject run_manager back into the other components that need it
        self.function_registry.run_manager = self.run_manager
        self.multi_agent_system.run_manager = self.run_manager

        # Phase 3: Initialize the function registry after all dependencies are set
        # This ensures that all functions are registered and ready to use
        asyncio.run(self.function_registry.initialize_registry())

        # Initialize other managers
        # EmbeddingManager handles embeddings for various operations
        self.embedding_manager = EmbeddingManager(self.client, self.logger)
        # ImagesManager manages image generation and related tasks
        self.images_manager = ImagesManager(self.client, self.logger)
        # SpeechToTextManager handles speech-to-text conversions
        self.speech_to_text_manager = SpeechToTextManager(self.client, self.logger)
        # TextToSpeechManager handles text-to-speech conversions
        self.text_to_speech_manager = TextToSpeechManager(self.client, self.logger)
        # AudioTranscriptionManager manages audio transcription tasks
        self.audio_transcription_manager = AudioTranscriptionManager(self.client, self.logger)
        # AudioTranslationManager handles audio translation tasks
        self.audio_translation_manager = AudioTranslationManager(self.client, self.logger)
        # SessionManager manages user sessions
        self.session_manager = SessionManager(self.client, self.logger)
        # VectorStoreManager handles vector storage for similarity searches
        self.vector_store_manager = VectorStoreManager(self.client, self.logger)
        # LocalVectorStoreManager handles local vector storage, utilizing embeddings
        self.local_vector_store_manager = LocalVectorStoreManager(self.client, self.logger, self.embedding_manager)

        self.logger.info("FlexiAI initialized successfully.")

    def create_stream_event_handler(self, assistant_name):
        """
        Factory method to create a new instance of StreamEventHandler.
        This ensures a fresh instance for each new stream, preventing concurrency issues.
        
        :param assistant_name: Name of the assistant to be used in the event handler
        :return: An instance of StreamEventHandler
        """
        handler = StreamEventHandler(
            client=self.client,
            logger=self.logger,
            run_manager=self.run_manager,
            assistant_name=assistant_name
        )
        self.logger.info(f"Created new StreamEventHandler instance for assistant: {assistant_name}")
        return handler

    