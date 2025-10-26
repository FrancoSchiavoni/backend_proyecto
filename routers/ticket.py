from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.client import get_session
from db.models.ticket import Ticket
from schemas.ticket import TicketConIntervenciones, TicketUpdate
from crud.ticket import  create_ticket, get_all_tickets, get_ticket, filter_tickets, update_ticket, count_tickets_by_status, count_tickets_last_7_days, count_completed_tickets_last_7_days, average_ticket_resolution_time, count_tickets_by_technician_and_status
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
    from crud.ticket_intervencion import get_intervenciones_ticket
    
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
    
    # Obtener intervenciones con labels
    intervenciones = await get_intervenciones_ticket(db, ticket_id)
    response_ticket.intervenciones = intervenciones

    return response_ticket

@router.get("/filter/", response_model=List[TicketConIntervenciones])
async def leer_ticket_filtrados(client_id: int = None, id_personal_asignado: int = None, id_estado: int = None, db: Session = Depends(get_session)):
    tickets = await filter_tickets(db, client_id, id_personal_asignado, id_estado)

    response_tickets = []
    for ticket, cliente, tecnico in tickets:
        ticket = TicketConIntervenciones.model_validate(ticket)
        if cliente:
            ticket.cliente = ClienteRead.model_validate(cliente)
        if tecnico:
            ticket.tecnico = tecnico.nombre if tecnico else None
        response_tickets.append(ticket)
    return response_tickets 


@router.post("/", response_model=Ticket)
async def crear_ticket(ticket: Ticket, db: Session = Depends(get_session)):
    return await create_ticket(db, ticket)

@router.put("/{ticket_id}", response_model=Ticket)
def actualizar_ticket(ticket_id: int, ticket: TicketUpdate, db: Session = Depends(get_session)): 
    db_ticket = update_ticket(db, ticket_id, ticket)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return db_ticket



@router.get("/stats/all", response_model=dict)
async def obtener_estadisticas_tickets(db: Session = Depends(get_session)):

    stats = {
        "tickets_por_estado": await count_tickets_by_status(db),
        "tickets_ultimos_7_dias": await count_tickets_last_7_days(db),
        "tickets_resueltos_ultimos_7_dias": await count_completed_tickets_last_7_days(db),
        "tiempo_promedio_resolucion": await average_ticket_resolution_time(db),
        "tickets_por_tecnico_y_estado": await count_tickets_by_technician_and_status(db)
    } 
    return stats
