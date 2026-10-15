import json
from datetime import datetime, timezone

from app.db.database import get_connection
from app.models.ticket import Ticket


def _row_to_ticket(row) -> Ticket:
    return Ticket(
        id=row["id"],
        platform=row["platform"],
        nome_coordenacao=row["nome_coordenacao"],
        centro_custo=row["centro_custo"],
        matricula_responsavel=row["matricula_responsavel"],
        fields=json.loads(row["fields"]),
        created_at=row["created_at"],
    )


def create_ticket(ticket: Ticket) -> Ticket:
    created_at = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO tickets
                (platform, nome_coordenacao, centro_custo, matricula_responsavel, fields, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                ticket.platform,
                ticket.nome_coordenacao,
                ticket.centro_custo,
                ticket.matricula_responsavel,
                json.dumps(ticket.fields),
                created_at,
            ),
        )
        ticket_id = cursor.lastrowid
    ticket.id = ticket_id
    ticket.created_at = created_at
    return ticket


def list_tickets() -> list[Ticket]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM tickets ORDER BY id").fetchall()
    return [_row_to_ticket(row) for row in rows]


def get_ticket(ticket_id: int) -> Ticket | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    return _row_to_ticket(row) if row else None
