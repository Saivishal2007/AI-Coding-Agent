from app.core.logging import get_logger
from app.services.tool_selection_service import ToolSelectionService
from app.services.review_service import ReviewService
from app.services.file_generation_service import FileGenerationService
from app.services.retrieval_service import RetrievalService
from app.services.planner_service import PlannerService
from app.services.action_processing_service import ActionProcessingService

logger = get_logger(__name__)


class OrchestratorService:
    """
    Decides which AI capability should handle
    the user's request.

    User
        ↓
    Tool Selection
        ↓
    Route Request
        ↓
    Return Result
    """

    def __init__(
        self,
        tool_selector: ToolSelectionService,
        retrieval: RetrievalService,
        planner: PlannerService,
        generator: FileGenerationService,
        reviewer: ReviewService,
        processor: ActionProcessingService,
    ):

        self.tool_selector = tool_selector

        self.retrieval = retrieval

        self.planner = planner

        self.generator = generator

        self.reviewer = reviewer

        self.processor = processor

    async def execute(
        self,
        instruction: str,
        context: str,
    ):

        logger.info("=" * 70)
        logger.info("ORCHESTRATOR STARTED")
        logger.info("=" * 70)

        tool = await self.tool_selector.choose(
            instruction,
            context,
        )

        logger.info(
            "Routing to tool: %s",
            tool.tool,
        )

        # --------------------------
        # Review
        # --------------------------

        if tool.tool == "review":

            return await self.reviewer.review(
                instruction,
                context,
            )

        # --------------------------
        # File Generation
        # --------------------------

        if tool.tool == "generate":

            return await self.generator.generate(
                instruction,
                context,
            )

        # --------------------------
        # Planner
        # --------------------------

        if tool.tool == "planner":

            return await self.planner.create_plan(
                context,
            )

        # --------------------------
        # Default AI Pipeline
        # --------------------------

        return await self.processor.process(
            context,
        )