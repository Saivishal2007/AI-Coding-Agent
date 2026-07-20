from app.core.logging import get_logger
from app.providers.gemini import GeminiProvider
from google.genai.errors import ClientError

logger = get_logger(__name__)


class LLMService:

    def __init__(self, provider: GeminiProvider | None = None) -> None:
        self._provider = provider or GeminiProvider()

    async def generate(self, prompt: str):

        try:

            return await self._provider.generate(prompt)

        except ClientError as e:

            message = str(e)

            if "RESOURCE_EXHAUSTED" in message or "429" in message:

                raise Exception(
                    "🚫 Gemini API quota exceeded.\n"
                    "Please wait a minute or configure another Gemini API key."
                )

            raise

    async def stream(self, prompt: str):

        try:

            async for chunk in self._provider.stream(prompt):

                yield chunk

        except ClientError as e:

            message = str(e)

            if "RESOURCE_EXHAUSTED" in message or "429" in message:

                raise Exception(
                    "🚫 Gemini API quota exceeded.\n"
                    "Please wait a minute or configure another Gemini API key."
                )

            raise