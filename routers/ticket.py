from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.client import get_session
from db.models.ticket import Ticket
from schemas.ticket import TicketConIntervenciones
from crud.ticket import  create_ticket, get_all_tickets, get_ticket, filter_tickets
from typing import List

router = APIRouter(prefix="/tickets", tags=["tickets"])




@router.get("/", response_model=List[Ticket])
async def listar_tickets(db: Session = Depends(get_session)):
    return await get_all_tickets(db)


@router.get("/{ticket_id}", response_model=TicketConIntervenciones)
async def leer_ticket(ticket_id: int, db: Session = Depends(get_session)):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket


@router.get("/filter/", response_model=List[Ticket])
async def get_filter_tickets(client_id: int = None, id_personal_asignado: int = None, id_estado: int = None, db: Session = Depends(get_session)):
    return await filter_tickets(db, client_id, id_personal_asignado, id_estado)



@router.post("/", response_model=Ticket)
async def crear_ticket(ticket: Ticket, db: Session = Depends(get_session)):
    return await create_ticket(db, ticket)