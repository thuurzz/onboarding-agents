import os

from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool

DEFAULT_DATABASE_URL = "postgresql://onboarding:onboarding@localhost:5433/onboarding"


def build_checkpointer() -> PostgresSaver:
    conn_string = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
    pool = ConnectionPool(conn_string, max_size=10, kwargs={"autocommit": True})
    checkpointer = PostgresSaver(pool)
    checkpointer.setup()
    return checkpointer
