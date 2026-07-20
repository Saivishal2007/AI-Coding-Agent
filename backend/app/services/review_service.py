from app.core.logging import get_logger
from app.services.llm_service import LLMService

logger = get_logger(__name__)


class ReviewService:

    def __init__(self, llm: LLMService):

        self.llm = llm

    async def review(
        self,
        instruction: str,
        path: str,
        content: str,
    ) -> str:

        logger.info(
            "Reviewing generated file: %s",
            path,
        )

        prompt = f"""
You are a Senior Software Engineer performing a production code review.

==================================================
TASK
==================================================

{instruction}

==================================================
TARGET FILE
==================================================

{path}

==================================================
FILE CONTENT
==================================================

{content}

==================================================
REVIEW CHECKLIST
==================================================

Review the code for:

- Correctness
- Bugs
- Missing imports
- Unused imports
- Edge cases
- Readability
- Maintainability
- Project consistency
- Performance
- Security

If improvements are needed,
rewrite the ENTIRE file.

If the file is already good,
return it unchanged.

==================================================
RULES
==================================================

Return ONLY the complete source code.

Do NOT return:

- Markdown
- JSON
- Triple backticks
- Explanations
- Notes
- Comments outside the code
"""

        reviewed = await self.llm.generate(prompt)

        logger.info(
            "Review completed for %s",
            path,
        )

        return reviewed