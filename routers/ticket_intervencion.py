from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.client import get_session
from db.models.ticket import Ticket
from crud.ticket_intervencion import get_intervencion, get_intervenciones_ticket, create_intervencion
from schemas.ticket_intervencion import TicketIntervencionBase, IntervencionRead
from typing import List

router = APIRouter(prefix="/ticket_intervencion", tags=["ticket_intervencion"])

@router.get("/{id_intervencion}", response_model=IntervencionRead)
async def leer_intervencion(id_intervencion: int, db: Session = Depends(get_session)):
    intervencion = get_intervencion(db, id_intervencion)
    if not intervencion:
        raise HTTPException(status_code=404, detail="Intervención no encontrada")
    return IntervencionRead.model_validate(intervencion)

@router.get("/{ticket_id}/intervenciones", response_model=List[IntervencionRead])
async def listar_intervenciones_ticket(ticket_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    intervenciones = await get_intervenciones_ticket(db, ticket_id, skip, limit)
    if not intervenciones:
        raise HTTPException(status_code=404, detail="No se encontraron intervenciones para este ticket")
    return [IntervencionRead.model_validate(intervencion) for intervencion in intervenciones]

@router.post("/{ticket_id}/intervenciones", response_model=IntervencionRead)
async def crear_intervencion(ticket_id: int, intervencion: TicketIntervencionBase, db: Session = Depends(get_session)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    
    return await create_intervencion(db, ticket_id, intervencion)