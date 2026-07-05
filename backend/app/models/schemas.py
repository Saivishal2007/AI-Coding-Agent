from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    version: str
    environment: str
    timestamp: datetime


class AgentRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=8000)
    session_id: UUID | None = None
    context: dict[str, str] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    request_id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    status: Literal["completed"]
    output: str
    metadata: dict[str, str] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    detail: str
    code: str
