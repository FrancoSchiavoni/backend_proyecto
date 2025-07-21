from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.client import get_session
from db.models.ticket import Ticket
from schemas.ticket import TicketConIntervenciones, TicketUpdate
from crud.ticket import  create_ticket, get_all_tickets, get_ticket, filter_tickets, update_ticket
from crud.cliente import get_cliente
from crud.user import get_usuario
from schemas.cliente import ClienteRead
from typing import List

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.get("/", response_model=List[TicketConIntervenciones])
async def listar_tickets(db: Session = Depends(get_session)):
    tickets = await get_all_tickets(db)
    response_tickets = []
    # Asignar cliente a cada ticket si existe
    for ticket, cliente, tecnico in tickets:
        ticket =TicketConIntervenciones.model_validate(ticket)
        if cliente:
            ticket.cliente = ClienteRead.model_validate(cliente)
        if tecnico:
            ticket.tecnico = tecnico.nombre if tecnico else None
        response_tickets.append(ticket)
    return response_tickets

@router.get("/{ticket_id}", response_model=TicketConIntervenciones)
async def leer_ticket(
    ticket_id: int, 
    db: Session = Depends(get_session),
    incluir_cliente: bool = False
):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    response_ticket = TicketConIntervenciones.model_validate(ticket)
    tecnico = get_usuario(db, ticket.id_personal_asignado)
    if tecnico:
        response_ticket.tecnico = tecnico.nombre
    if incluir_cliente:
        cliente_db = get_cliente(db, ticket.id_cliente)
        if cliente_db:
            response_ticket.cliente = ClienteRead.model_validate(cliente_db)

    return response_ticket

@router.get("/filter/", response_model=List[Ticket])
async def leer_ticket_filtrados(client_id: int = None, id_personal_asignado: int = None, id_estado: int = None, db: Session = Depends(get_session)):
    return await filter_tickets(db, client_id, id_personal_asignado, id_estado)

@router.post("/", response_model=Ticket)
async def crear_ticket(ticket: Ticket, db: Session = Depends(get_session)):
    return await create_ticket(db, ticket)

@router.put("/{ticket_id}", response_model=Ticket)
def actualizar_ticket(ticket_id: int, ticket: TicketUpdate, db: Session = Depends(get_session)): 
    db_ticket = update_ticket(db, ticket_id, ticket)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return db_ticket
