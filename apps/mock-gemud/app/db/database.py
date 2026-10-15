import os
import sqlite3
from pathlib import Path

# Caminho do banco configurável (útil em Docker, onde o volume monta em outro lugar).
DEFAULT_DB_PATH: Path = Path(__file__).resolve().parent.parent / "mock_gemud.db"
DB_PATH: Path = Path(os.getenv("GEMUD_DB_PATH", str(DEFAULT_DB_PATH)))


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
