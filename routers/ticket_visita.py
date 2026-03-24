from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from datetime import datetime
from typing import Optional, List

from db.client import get_session
from schemas.ticket_visita import TicketVisitaCreate, TicketVisitaUpdate, TicketVisitaRead
from crud.ticket_visita import (
    create_visita,
    get_visita,
    get_visitas_by_ticket,
    update_visita,
    delete_visita,
    get_visitas_by_date_range,
)

router = APIRouter(prefix="/visitas", tags=["visitas"])


@router.post("/", response_model=TicketVisitaRead)
def crear_visita(visita: TicketVisitaCreate, db: Session = Depends(get_session)):
    return create_visita(db, visita)


@router.get("/calendar/", response_model=List[TicketVisitaRead])
def obtener_visitas_calendario(
    fecha_inicio: datetime = Query(..., description="Inicio del rango de fechas (ISO 8601)"),
    fecha_fin: datetime = Query(..., description="Fin del rango de fechas (ISO 8601)"),
    id_personal_asignado: Optional[int] = Query(default=None, description="Filtrar por técnico"),
    db: Session = Depends(get_session),
):
    """
    Retorna todas las visitas que se superponen con el rango [fecha_inicio, fecha_fin].
    Usado por la vista de Calendario en Flutter.
    """
    return get_visitas_by_date_range(db, fecha_inicio, fecha_fin, id_personal_asignado)


@router.get("/ticket/{ticket_id}", response_model=List[TicketVisitaRead])
def listar_visitas_por_ticket(ticket_id: int, db: Session = Depends(get_session)):
    return get_visitas_by_ticket(db, ticket_id)


@router.get("/{visita_id}", response_model=TicketVisitaRead)
def leer_visita(visita_id: int, db: Session = Depends(get_session)):
    visita = get_visita(db, visita_id)
    if not visita:
        raise HTTPException(status_code=404, detail="Visita no encontrada")
    return visita


@router.put("/{visita_id}", response_model=TicketVisitaRead)
def actualizar_visita(visita_id: int, visita: TicketVisitaUpdate, db: Session = Depends(get_session)):
    db_visita = update_visita(db, visita_id, visita)
    if db_visita is None:
        raise HTTPException(status_code=404, detail="Visita no encontrada")
    return db_visita


@router.delete("/{visita_id}")
def eliminar_visita(visita_id: int, db: Session = Depends(get_session)):
    success = delete_visita(db, visita_id)
    if not success:
        raise HTTPException(status_code=404, detail="Visita no encontrada")
    return {"message": "Visita eliminada correctamente"}
