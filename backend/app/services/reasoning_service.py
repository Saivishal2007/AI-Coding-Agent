import json

from app.core.logging import get_logger
from app.services.llm_service import LLMService

logger = get_logger(__name__)


class ReasoningService:
    """
    Decides the next action for the AI agent.

    It acts as the agent's decision-making layer,
    choosing what should happen next based on the
    current goal, context, execution history, and
    latest execution result.
    """

    def __init__(
        self,
        llm: LLMService,
    ):

        self.llm = llm

    async def decide(
        self,
        goal: str,
        context: str,
        history: list[dict],
        latest_result: dict | None,
    ) -> dict:

        logger.info(
            "Running reasoning step..."
        )

        prompt = f"""
You are an autonomous software engineering agent.

Your job is to decide the NEXT action.

==============================
GOAL
==============================

{goal}

==============================
PROJECT CONTEXT
==============================

{context}

==============================
EXECUTION HISTORY
==============================

{json.dumps(history, indent=2)}

==============================
LATEST RESULT
==============================

{json.dumps(latest_result, indent=2)}

==============================
RULES
==============================

Think before acting.

If more information is needed,
search first.

If enough context exists,
edit the code.

If execution failed,
consider replanning.

If the task is finished,
stop.

Return ONLY valid JSON.

Example

{{
    "decision": "search",
    "reason": "Need more context.",
    "continue": true
}}
"""

        response = await self.llm.generate(
            prompt
        )

        try:

            decision = json.loads(
                response
            )

            logger.info(
                "Reasoning decision: %s",
                decision.get("decision"),
            )

            return decision

        except Exception:

            logger.exception(
                "Reasoning failed."
            )

            return {
                "decision": "stop",
                "reason": "Unable to reason.",
                "continue": False,
            }