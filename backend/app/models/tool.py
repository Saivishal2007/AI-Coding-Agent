from typing import Any
from pydantic import BaseModel, Field


class ToolArgument(BaseModel):

    name: str

    value: str


class ToolRequest(BaseModel):
    """
    Represents the tool selected by the AI.
    """

    tool: str

    arguments: dict[str, Any] = Field(default_factory=dict)

    reason: str = ""

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )


class ToolResult(BaseModel):
    """
    Result returned after executing a tool.
    """

    success: bool

    output: str

    tool: str = ""

    execution_time: float | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)