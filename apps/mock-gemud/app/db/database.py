import sqlite3
from pathlib import Path

DB_PATH: Path = Path(__file__).resolve().parent.parent / "mock_gemud.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                nome_coordenacao TEXT NOT NULL,
                centro_custo TEXT NOT NULL,
                matricula_responsavel TEXT NOT NULL,
                fields TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
