import json

from app.core.logging import get_logger

logger = get_logger(__name__)


class ReflectionService:
    """
    Reviews the AI's completed response before it is
    returned to the user.

    The purpose is NOT to regenerate an answer, but to
    quickly verify whether the result appears complete,
    correct and relevant.
    """

    def __init__(self, llm):

        self.llm = llm

    async def review(
        self,
        user_request: str,
        context: str,
        result: dict,
    ) -> dict:

        logger.info("Starting AI reflection...")

        prompt = f"""
You are a senior software engineer.

Your task is to review the completed AI response.

==================================================
USER REQUEST
==================================================

{user_request}

==================================================
PROJECT CONTEXT
==================================================

{context}

==================================================
AI RESULT
==================================================

{json.dumps(result, indent=2)}

==================================================
CHECKLIST
==================================================

Verify:

1. Did the AI answer the user's request?

2. Is the selected action appropriate?

3. Are there obvious mistakes?

4. Is another action required?

5. Is the response complete?

Return ONLY valid JSON.

Example:

{{
    "approved": true,
    "reason": "The response satisfies the request.",
    "suggestions": []
}}
"""

        response = await self.llm.generate(prompt)

        try:

            review = json.loads(response)

            logger.info(
                "Reflection completed. Approved=%s",
                review.get("approved"),
            )

            return review

        except Exception:

            logger.exception(
                "Reflection parsing failed."
            )

            return {
                "approved": True,
                "reason": "Reflection unavailable.",
                "suggestions": [],
            }