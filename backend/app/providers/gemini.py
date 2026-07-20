from google import genai
from google.genai import types

from app.core.config import settings
from app.core.logging import get_logger
from app.prompts.system_prompt import SYSTEM_PROMPT

logger = get_logger(__name__)


class GeminiProvider:
    def __init__(self, api_key: str | None = None, model_name: str | None = None) -> None:
        self._api_key = api_key or settings.GEMINI_API_KEY
        self._model_name = model_name or settings.MODEL_NAME

        if not self._api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        if not self._model_name:
            raise ValueError("MODEL_NAME is not configured.")

        self._client = genai.Client(api_key=self._api_key)

    async def generate(self, prompt: str) -> str:
        response = await self._client.aio.models.generate_content(
            model=self._model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
            ),
        )

        print("\n========== GEMINI RAW RESPONSE ==========")
        print(repr(response.text))
        print("=========================================\n")

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")
        print("\n" + "=" * 60)
        print("GEMINI RESPONSE")
        print("=" * 60)
        print(repr(response.text))
        print("=" * 60 + "\n")
        return response.text
    async def stream(self, prompt: str):

        stream = await self._client.aio.models.generate_content_stream(

            model=self._model_name,

            contents=prompt,

            config=types.GenerateContentConfig(

                system_instruction=SYSTEM_PROMPT,

            ),

        )

        async for chunk in stream:

            if chunk.text:

                yield chunk.text