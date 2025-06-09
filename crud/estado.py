from typing import List, Optional
from sqlmodel import Session, select
from db.models.estado import Estado, EstadoBase

def get_estado_by_id(session: Session, estado_id: int) -> Optional[Estado]:
    """Obtiene un estado por su ID."""
    statement = select(Estado).where(Estado.ID_Estado == estado_id)
    return session.exec(statement).first()

def get_all_estados(session: Session, skip: int = 0, limit: int = 100) -> List[Estado]:
    """Obtiene una lista de todos los estados."""
    statement = select(Estado).offset(skip).limit(limit)
    return list(session.exec(statement).all())