from fastapi import FastAPI

from app.db.database import init_db
from app.views import tickets

app = FastAPI(title="Mock Gemud", version="0.1.0")

init_db()

app.include_router(tickets.router)
