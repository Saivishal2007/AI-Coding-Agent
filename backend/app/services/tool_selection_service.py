import json

from app.core.logging import get_logger
from app.models.tool import ToolRequest
from app.prompts.tool_prompt import TOOL_PROMPT

logger = get_logger(__name__)


class ToolSelectionService:

    def __init__(self, llm):

        self.llm = llm

    async def choose(
        self,
        instruction: str,
        context: str,
    ) -> ToolRequest:

        logger.info("Selecting best tool for request...")

        prompt = f"""
{TOOL_PROMPT}

==================================================
USER REQUEST
==================================================

{instruction}

==================================================
REPOSITORY CONTEXT
==================================================

{context}

==================================================
OBJECTIVE
==================================================

Analyze the request carefully.

Choose the SINGLE BEST tool.

Selection Rules

- Read before Edit
- Search before Read when location is unknown
- Repository Search for project-wide questions
- Dependency Analysis for dependency questions
- Security Scan for vulnerabilities
- Secret Scan for credential leaks
- Review for code review requests
- Planner for large implementation tasks
- File Generator for creating new projects/files

Return ONLY valid JSON.

Example

{{
    "tool": "repository_search",
    "reason": "The user is asking about project-wide code.",
    "confidence": 0.97
}}
"""

        response = await self.llm.generate(prompt)

        logger.info("Tool selection response received.")

        try:

            data = json.loads(response)

            tool = ToolRequest.model_validate(data)

            logger.info(
                "Selected Tool: %s (confidence=%s)",
                tool.tool,
                getattr(tool, "confidence", "N/A"),
            )

            return tool

        except Exception as e:

            logger.exception(
                "Failed to parse tool selection."
            )

            logger.error(response)

            raise ValueError(
                f"Invalid Tool Selection Response:\n\n{response}"
            ) from e