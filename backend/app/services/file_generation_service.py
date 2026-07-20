from app.core.logging import get_logger
from app.prompts.file_generator_prompt import FILE_GENERATOR_PROMPT

logger = get_logger(__name__)


class FileGenerationService:

    def __init__(self, llm):

        self.llm = llm

    async def generate(
        self,
        path: str,
        instruction: str,
        repository_context: str,
    ) -> str:

        logger.info(
            "Generating file: %s",
            path,
        )

        prompt = f"""
{FILE_GENERATOR_PROMPT}

==================================================
TARGET FILE
==================================================

{path}

==================================================
USER REQUEST
==================================================

{instruction}

==================================================
REPOSITORY CONTEXT
==================================================

{repository_context}

==================================================
RULES
==================================================

Generate the COMPLETE file.

Do NOT generate snippets.

Do NOT omit imports.

Do NOT use placeholders.

The generated code must compile.

Follow the existing architecture.

Use the project's coding style.

Return ONLY the file contents.
"""

        response = await self.llm.generate(
            prompt
        )

        logger.info(
            "Generated %s successfully.",
            path,
        )

        return response