from pydantic import BaseModel, Field


class SessionMessage(BaseModel):

    role: str

    content: str


class ChatSession(BaseModel):

    id: str

    messages: list[SessionMessage] = Field(default_factory=list)