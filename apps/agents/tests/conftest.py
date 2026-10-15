from fastapi import FastAPI
from langgraph.checkpoint.memory import MemorySaver

from app.controllers.builder import build_graph
from app.views import chat


def make_app() -> FastAPI:
    app = FastAPI()
    app.state.graph = build_graph(checkpointer=MemorySaver())
    app.include_router(chat.router)
    return app
