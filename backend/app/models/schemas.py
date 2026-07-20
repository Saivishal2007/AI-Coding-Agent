from datetime import datetime
from typing import Any, Literal, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ApplyEditRequest(BaseModel):
    edit_id: str


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    version: str
    environment: str
    timestamp: datetime


class AgentRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=8000)
    session_id: UUID | None = None
    context: dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    request_id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    status: Literal["completed"]
    output: dict
    metadata: dict[str, str] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    detail: str
    code: str


class AgentFile(BaseModel):
    path: str
    content: str

class AgentAction(BaseModel):
    action: Literal[
        "respond",

        # File tools
        "read_file",
        "write_file",

        # Repository tools
        "search_repository",

        # Edit tools
        "edit_file",
        "edit_files",

        # Security tools
        "scan_secrets",
        "scan_vulnerabilities",
        "analyze_dependency_security",
        "generate_security_report",
    ]

    # Response action
    message: Optional[str] = None

    # Single-file actions
    path: Optional[str] = None
    content: Optional[str] = None

    # Repository search
    query: Optional[str] = None
    limit: int = 10

    # Multi-file actions
    files: list[AgentFile] = Field(default_factory=list)