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
from flexiai.cfg.config import Config
from flexiai.core.flexi_managers.stream_event_handler import StreamEventHandler


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
        self.logger = logging.getLogger(__name__)
        self.config = Config()  # Load configuration
        self.logger.info("Configuration loaded successfully.")

        # Phase 1: Create core components
        self.credential_manager = CredentialManager()
        self.client = self.credential_manager.client

        # Initialize managers that don't depend on run_manager yet
        self.thread_manager = ThreadManager(self.client, self.logger)
        self.message_manager = MessageManager(self.client, self.logger)
        self.completions_manager = CompletionsManager(self.client, self.logger)
        self.assistant_manager = AssistantManager(self.client, self.logger)

        # Initialize the multi-agent system manager and function registry without run_manager for now
        self.multi_agent_system = MultiAgentSystemManager(
            self.client, self.logger, self.thread_manager, None, self.message_manager
        )
        self.function_registry = FunctionRegistry(self.multi_agent_system, None)

        # Phase 2: Now create RunManager and inject dependencies into function_registry and multi_agent_system
        self.run_manager = RunManager(self.client, self.logger, self.message_manager, self.function_registry)

        # Inject run_manager back into the other components
        self.function_registry.run_manager = self.run_manager
        self.multi_agent_system.run_manager = self.run_manager

        # Phase 3: Initialize the function registry after all dependencies are set
        asyncio.run(self.function_registry.initialize_registry())

        # Initialize other managers
        self.embedding_manager = EmbeddingManager(self.client, self.logger)
        self.images_manager = ImagesManager(self.client, self.logger)
        self.speech_to_text_manager = SpeechToTextManager(self.client, self.logger)
        self.text_to_speech_manager = TextToSpeechManager(self.client, self.logger)
        self.audio_transcription_manager = AudioTranscriptionManager(self.client, self.logger)
        self.audio_translation_manager = AudioTranslationManager(self.client, self.logger)
        self.session_manager = SessionManager(self.client, self.logger)
        self.vector_store_manager = VectorStoreManager(self.client, self.logger)
        self.local_vector_store_manager = LocalVectorStoreManager(self.client, self.logger, self.embedding_manager)

        self.stream_event_handler = StreamEventHandler(self.client, self.logger, self.run_manager)

        self.logger.info("FlexiAI initialized successfully.")
