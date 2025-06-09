from typing import List, Optional
from sqlmodel import Session, select
from db.models.prioridad import Prioridad, PrioridadBase

def get_prioridad_by_id(session: Session, prioridad_id: int) -> Optional[Prioridad]:
    """Obtiene una prioridad por su ID."""
    statement = select(Prioridad).where(Prioridad.ID_Prioridad == prioridad_id)
    return session.exec(statement).first()

def get_all_prioridades(session: Session) -> List[Prioridad]:
    """Obtiene una lista de todas las prioridades."""
    statement = select(Prioridad)
    return list(session.exec(statement).all())
