from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.client import get_session
from db.models.ticket import Ticket
from crud.ticket import  create_ticket, get_all_tickets, get_ticket
from typing import List

router = APIRouter(prefix="/tickets", tags=["tickets"])




@router.get("/", response_model=List[Ticket])
async def listar_tickets(db: Session = Depends(get_session)):
    return await get_all_tickets(db)


@router.get("/{ticket_id}", response_model=Ticket)
async def leer_ticket(ticket_id: int, db: Session = Depends(get_session)):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket

#create ticket

@router.post("/", response_model=Ticket)
async def crear_ticket(ticket: Ticket, db: Session = Depends(get_session)):
    return await create_ticket(db, ticket)