import json

from app.core.logging import get_logger
from app.models.plan import ExecutionPlan
from app.prompts.planner_prompt import PLANNER_PROMPT

logger = get_logger(__name__)


class PlannerService:

    def __init__(self, llm):

        self.llm = llm

    async def create_plan(
        self,
        goal: str,
        context: str,
    ) -> ExecutionPlan:

        logger.info("Creating execution plan...")

        prompt = f"""
{PLANNER_PROMPT}

==================================================
USER GOAL
==================================================

{goal}

==================================================
REPOSITORY CONTEXT
==================================================

{context}

==================================================
TASK
==================================================

Create the BEST execution plan for accomplishing the user's goal.

Rules

- Think before planning.
- Search before reading.
- Read before editing.
- Edit only required files.
- Create new files only if absolutely necessary.
- Produce an efficient step-by-step plan.

Return ONLY valid JSON.
"""

        response = await self.llm.generate(prompt)

        logger.info("Planner response received.")

        try:

            plan = ExecutionPlan.model_validate(
                json.loads(response)
            )

            logger.info(
                "Execution plan created with %d steps.",
                len(plan.steps),
            )

            return plan

        except Exception as e:

            logger.exception(
                "Failed to parse execution plan."
            )

            raise ValueError(
                f"Invalid planner response:\n\n{response}"
            ) from e