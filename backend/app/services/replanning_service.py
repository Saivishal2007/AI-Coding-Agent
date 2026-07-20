import json

from app.core.logging import get_logger
from app.services.llm_service import LLMService

logger = get_logger(__name__)


class ReplanningService:
    """
    Creates a new execution plan when the current
    plan cannot continue.

    Examples:
    - File not found
    - Edit failed
    - Compilation error
    - Dependency missing
    """

    def __init__(
        self,
        llm: LLMService,
    ):

        self.llm = llm

    async def replan(
        self,
        goal: str,
        previous_steps: list[dict],
        failure_reason: str,
    ) -> dict:

        logger.info(
            "Generating recovery plan..."
        )

        prompt = f"""
You are a senior software engineer.

The previous execution has failed.

Your job is NOT to repeat the same plan.

Instead,
analyze why it failed and produce
a better plan.

================================

GOAL

{goal}

================================

PREVIOUS STEPS

{json.dumps(previous_steps, indent=2)}

================================

FAILURE

{failure_reason}

================================

Return ONLY valid JSON.

Example

{{
    "reason": "...",
    "steps": [
        "...",
        "...",
        "..."
    ]
}}
"""

        response = await self.llm.generate(
            prompt
        )

        try:

            return json.loads(response)

        except Exception:

            logger.exception(
                "Failed to generate recovery plan."
            )

            return {
                "reason": "Unable to generate recovery plan.",
                "steps": [],
            }