from pydantic import BaseModel


class ToolCall(BaseModel):

    tool: str

    arguments: dict = {}