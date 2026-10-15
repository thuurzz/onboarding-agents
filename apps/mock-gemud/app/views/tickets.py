from fastapi import APIRouter, HTTPException, status

from app.controllers import ticket_service
from app.models.ticket import Ticket

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", response_model=Ticket, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: Ticket) -> Ticket:
    return ticket_service.create_ticket(ticket)


@router.get("", response_model=list[Ticket])
def list_tickets() -> list[Ticket]:
    return ticket_service.list_tickets()


@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int) -> Ticket:
    ticket = ticket_service.get_ticket(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket não encontrado")
    return ticket
