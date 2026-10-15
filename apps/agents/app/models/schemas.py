from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None


class ChatResponse(BaseModel):
    thread_id: str
    reply: str
    ticket_result: dict[str, Any] | None = None


class Message(BaseModel):
    role: str
    content: str


class Conversation(BaseModel):
    thread_id: str
    messages: list[Message] = Field(default_factory=list)
