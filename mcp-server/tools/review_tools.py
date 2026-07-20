from app.providers.gemini import GeminiProvider
from app.services.llm_service import LLMService
from app.services.review_service import ReviewService


def register_review_tools(mcp):
    """
    Register all AI review-related MCP tools.
    """

    @mcp.tool()
    async def review_code(
        instruction: str,
        path: str,
        content: str,
    ) -> dict:
        """
        Review code using AI and return an improved version.

        Args:
            instruction: Review or refactoring instruction.
            path: Relative path of the file being reviewed.
            content: Source code to review.

        Returns:
            AI review result.
        """
        try:
            if not instruction:
                raise ValueError("Instruction cannot be empty.")

            if not path:
                raise ValueError("Path cannot be empty.")

            provider = GeminiProvider()
            llm = LLMService(provider)
            service = ReviewService(llm)

            return await service.review(
                instruction=instruction,
                path=path,
                content=content,
            )

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }