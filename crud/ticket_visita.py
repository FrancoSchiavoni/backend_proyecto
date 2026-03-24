from sqlmodel import Session, select
from db.models.ticket_visita import TicketVisita
from schemas.ticket_visita import TicketVisitaCreate, TicketVisitaUpdate
from datetime import datetime
from typing import Optional


def create_visita(db: Session, visita: TicketVisitaCreate) -> TicketVisita:
    nueva_visita = TicketVisita.model_validate(visita)
    db.add(nueva_visita)
    db.commit()
    db.refresh(nueva_visita)
    return nueva_visita


def get_visita(db: Session, visita_id: int) -> Optional[TicketVisita]:
    return db.get(TicketVisita, visita_id)


def get_visitas_by_ticket(db: Session, ticket_id: int) -> list[TicketVisita]:
    statement = select(TicketVisita).where(TicketVisita.id_caso == ticket_id).order_by(TicketVisita.fecha_inicio)
    return db.exec(statement).all()


def update_visita(db: Session, visita_id: int, visita_update: TicketVisitaUpdate) -> Optional[TicketVisita]:
    db_visita = db.get(TicketVisita, visita_id)
    if not db_visita:
        return None
    visita_data = visita_update.model_dump(exclude_unset=True)
    for key, value in visita_data.items():
        setattr(db_visita, key, value)
    db.add(db_visita)
    db.commit()
    db.refresh(db_visita)
    return db_visita


def delete_visita(db: Session, visita_id: int) -> bool:
    db_visita = db.get(TicketVisita, visita_id)
    if not db_visita:
        return False
    db.delete(db_visita)
    db.commit()
    return True


def get_visitas_by_date_range(
    db: Session,
    fecha_inicio: datetime,
    fecha_fin: datetime,
    id_personal_asignado: Optional[int] = None,
) -> list[TicketVisita]:
    """
    Calendar query: returns all visits whose window overlaps the given date range.
    Optionally filtered by technician. Used by the Flutter calendar view.
    """
    statement = select(TicketVisita).where(
        TicketVisita.fecha_inicio < fecha_fin,
        TicketVisita.fecha_fin > fecha_inicio,
    )
    if id_personal_asignado is not None:
        statement = statement.where(TicketVisita.id_personal_asignado == id_personal_asignado)
    statement = statement.order_by(TicketVisita.fecha_inicio)
    return db.exec(statement).all()
