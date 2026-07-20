from pydantic import BaseModel
from typing import Any, Dict


class MCPRequest(BaseModel):
    tool: str
    arguments: Dict[str, Any]


class MCPResponse(BaseModel):
    success: bool
    result: Any = None
    error: str | None = None