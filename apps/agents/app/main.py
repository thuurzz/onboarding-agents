from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.checkpointer import build_checkpointer
from app.controllers.builder import build_graph
from app.views import chat

app = FastAPI(title="Onboarding Agents", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

checkpointer = build_checkpointer()
app.state.graph = build_graph(checkpointer=checkpointer)

app.include_router(chat.router)
