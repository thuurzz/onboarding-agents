import uuid

from fastapi import APIRouter, HTTPException, Request

from app.models.schemas import ChatRequest, ChatResponse, Conversation, Message

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: Request, body: ChatRequest) -> ChatResponse:
    graph = request.app.state.graph
    thread_id = body.thread_id or str(uuid.uuid4())

    config = {"configurable": {"thread_id": thread_id}}
    result = graph.invoke(
        {"messages": [{"role": "user", "content": body.message}]},
        config=config,
    )

    return ChatResponse(
        thread_id=thread_id,
        reply=result.get("reply", ""),
        ticket_result=result.get("ticket_result"),
    )


@router.get("/conversation/{thread_id}", response_model=Conversation)
def conversation(request: Request, thread_id: str) -> Conversation:
    graph = request.app.state.graph
    snapshot = graph.get_state({"configurable": {"thread_id": thread_id}})
    messages = snapshot.values.get("messages", []) if snapshot.values else []
    if not messages:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")

    return Conversation(
        thread_id=thread_id,
        messages=[Message(role=m["role"], content=m["content"]) for m in messages],
    )
