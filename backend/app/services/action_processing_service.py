from app.core.logging import get_logger
from app.services.llm_service import LLMService
from app.services.action_parser_service import ActionParserService
from app.services.action_executor_service import ActionExecutorService

logger = get_logger(__name__)


class ActionProcessingService:
    """
    Handles the complete AI execution pipeline.

    Context
        ↓
    LLM
        ↓
    Parse JSON Action
        ↓
    Validate Action
        ↓
    Execute Action
        ↓
    Return Result
    """

    def __init__(
        self,
        llm: LLMService,
        parser: ActionParserService,
        executor: ActionExecutorService,
    ):
        self.llm = llm
        self.parser = parser
        self.executor = executor

    async def process(
        self,
        context: str,
    ) -> dict:

        logger.info("=" * 70)
        logger.info("STARTING ACTION PIPELINE")
        logger.info("=" * 70)

        # ---------------------------
        # Generate LLM Response
        # ---------------------------

        output = await self.llm.generate(context)

        logger.info("LLM response received.")

        logger.info("=" * 70)
        logger.info("RAW GEMINI OUTPUT")
        logger.info("=" * 70)
        logger.info(repr(output))
        logger.info("=" * 70)

        # ---------------------------
        # Parse Action
        # ---------------------------

        action = self.parser.parse(output)

        logger.info(
            "Action Selected: %s",
            action.action,
        )

        logger.info(
            "Parsed Action: %s",
            action.model_dump(),
        )

        # ---------------------------
        # Execute Action
        # ---------------------------

        result = await self.executor.execute(action)

        logger.info(
            "Execution completed successfully."
        )

        logger.info("=" * 70)
        logger.info("ACTION PIPELINE FINISHED")
        logger.info("=" * 70)

        return result