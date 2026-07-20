import json
import re

from app.models.schemas import AgentAction


class ActionParserService:
    """
    Converts Gemini responses into AgentAction objects.

    Supports:
    - Raw JSON
    - ```json ... ```
    - ``` ... ```
    - Extra explanatory text before/after JSON
    """

    @staticmethod
    def parse(response: str) -> AgentAction:

        if response is None:
            raise ValueError("Gemini returned None.")

        response = response.strip()

        # -----------------------------
        # Remove Markdown Code Fences
        # -----------------------------
        response = re.sub(r"^```json", "", response, flags=re.IGNORECASE)
        response = re.sub(r"^```", "", response)
        response = re.sub(r"```$", "", response)

        response = response.strip()

        # -----------------------------
        # Extract JSON if extra text exists
        # -----------------------------
        if not response.startswith("{"):

            start = response.find("{")

            if start != -1:
                response = response[start:]

        if not response.endswith("}"):

            end = response.rfind("}")

            if end != -1:
                response = response[: end + 1]

        response = response.strip()

        # -----------------------------
        # Parse JSON
        # -----------------------------
        try:

            data = json.loads(response)

            return AgentAction.model_validate(data)

        except json.JSONDecodeError as e:

            raise ValueError(
                f"""
Gemini returned invalid JSON.

Reason:
{e}

Actual Response:

{response}
"""
            )

        except Exception as e:

            raise ValueError(
                f"Failed to parse AgentAction:\n{e}"
            )