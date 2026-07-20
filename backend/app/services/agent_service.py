from uuid import uuid4
from pathlib import Path
from app.services.llm_service import LLMService
from app.core.config import settings
from app.core.logging import get_logger
from app.models.schemas import AgentRequest, AgentResponse
from app.utils.exceptions import ValidationAppError
from app.utils.helpers import compact_whitespace
from app.services.repository_service import RepositoryService
from app.services.file_reader_service import FileReaderService
from app.services.context_builder import ContextBuilder
from app.services.file_finder_service import FileFinderService
from app.services.repository_search_service import RepositorySearchService
from app.services.dependency_service import DependencyService
from app.services.file_writer_service import FileWriterService
from app.services.action_parser_service import ActionParserService
from app.services.action_executor_service import ActionExecutorService
from app.services.file_editor_service import FileEditorService
from app.services.intent_classifier_service import IntentClassifierService
from app.services.planner_service import PlannerService
from app.services.pending_edit_service import PendingEditService
from app.services.apply_edit_service import ApplyEditService
from app.services.retrieval_service import RetrievalService
from app.services.action_processing_service import ActionProcessingService
from app.services.session_service import SessionService
from app.services.project_index_service import ProjectIndexService
from app.services.file_generation_service import FileGenerationService
from app.services.review_service import ReviewService
from app.services.tool_selection_service import ToolSelectionService
from app.services.project_summary_service import ProjectSummaryService
from app.services.agent_loop_service import AgentLoopService
from app.services.agent_memory_service import AgentMemoryService
from app.services.reasoning_service import ReasoningService
from app.services.replanning_service import ReplanningService
from app.services.task_recovery_service import TaskRecoveryService

logger = get_logger(__name__)


class AgentService:
    def __init__(self):
        self.llm = LLMService()

        root = str(Path(__file__).resolve().parents[3])

        self.repository = RepositoryService(root)
        self.project_index = ProjectIndexService(root)
        self.reader = FileReaderService(root)
        self.finder = FileFinderService(root)
        self.search = RepositorySearchService(root)
        self.context_builder = ContextBuilder()
        self.dependencies = DependencyService(root)
        self.sessions = SessionService()
        self.project_summary = ProjectSummaryService(root)
        self.project_index.build()
        summary = self.project_summary.build()
        self.retrieval = RetrievalService(repository=self.repository,search=self.search,reader=self.reader,dependencies=self.dependencies,context_builder=self.context_builder,project_index=self.project_index,project_summary=self.project_summary)
        self.writer = FileWriterService(root)
        self.editor = FileEditorService(self.reader)
        self.pending_edits = PendingEditService()
        self.parser = ActionParserService()
        self.executor = ActionExecutorService(writer=self.writer,editor=self.editor,pending=self.pending_edits)
        self.processor = ActionProcessingService(llm=self.llm,parser=self.parser,executor=self.executor)
        self.intent = IntentClassifierService()
        self.apply_service = ApplyEditService(writer=self.writer,pending=self.pending_edits)
        self.planner = PlannerService(self.llm)

        logger.info(summary)
        self.generator = FileGenerationService(self.llm)
        self.reviewer = ReviewService(self.llm)
        self.tool_selector = ToolSelectionService(self.llm)
        self.memory = AgentMemoryService()

        self.reasoning = ReasoningService(
            self.llm,
        )

        self.replanning = ReplanningService(
            self.llm,
        )

        self.recovery = TaskRecoveryService(
            self.memory,
        )

        self.agent_loop = AgentLoopService(
            processor=self.processor,
            retrieval=self.retrieval,
            memory=self.memory,
            reasoning=self.reasoning,
            planner=self.planner,
            replanning=self.replanning,
            tool_selector=self.tool_selector,
        )

    async def run_pipeline(self, request: AgentRequest) -> AgentResponse:
        prompt = compact_whitespace(request.prompt)

        if not prompt:
            raise ValidationAppError("Prompt cannot be empty.")

        session_id = request.session_id or uuid4()
        logger.info("Processing agent request for session %s", session_id)

        history = self.sessions.history(session_id)

        recent_history = history[-6:]

        conversation = ""

        for message in recent_history:
            conversation += (
                f"{message['role'].upper()}: "
                f"{message['content']}\n"
            )

        # Save the user's prompt
        self.sessions.add(
            session_id,
            "user",
            request.prompt,
        )

        result = await self.agent_loop.execute(
            prompt=prompt,
            editor_context=request.context,
            conversation=conversation,
        )


        if isinstance(result, dict):

            final_result = result.get("result")

            if (
                isinstance(final_result, dict)
                and final_result.get("action") == "respond"
            ):
                self.sessions.add(
                    session_id,
                    "assistant",
                    final_result.get("message", ""),
                )
        return AgentResponse(
            session_id=session_id,
            status="completed",
            output=result,
            metadata={
                "engine": settings.MODEL_NAME,
                "timeout_seconds": str(settings.AGENT_TIMEOUT_SECONDS),
            },
        )
        
    def apply_edit(self, edit_id: str):

        return self.apply_service.apply(edit_id)
    
    async def run(
        self,
        request: AgentRequest,
    ) -> AgentResponse:
        return await self.run_pipeline(request)
    
    async def stream(
        self,
        request: AgentRequest,
    ):

        prompt = compact_whitespace(request.prompt)

        session_id = request.session_id or uuid4()

        # Get previous conversation
        history = self.sessions.history(session_id)

        recent_history = history[-6:]

        conversation = ""

        for message in recent_history:
            conversation += (
                f"{message['role'].upper()}: "
                f"{message['content']}\n"
            )

        # Save current user message
        self.sessions.add(
            session_id,
            "user",
            prompt,
        )

        # Build repository context
        context = self.retrieval.build_context(
            prompt,
            request.context,
            conversation,
        )

        # Store streamed response
        response = ""

        async for chunk in self.llm.stream(context):

            response += chunk

            yield chunk

        # Save assistant response after streaming completes
        self.sessions.add(
            session_id,
            "assistant",
            response,
        )