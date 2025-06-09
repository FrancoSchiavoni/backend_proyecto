from typing import List, Optional
from sqlmodel import Session, select
from db.models.tipo_caso import TipoCaso, TipoCasoBase
def get_tipo_caso_by_id(session: Session, tipo_caso_id: int) -> Optional[TipoCaso]:
    """Obtiene un tipo de caso por su ID."""
    statement = select(TipoCaso).where(TipoCaso.ID_TipoCaso == tipo_caso_id)
    return session.exec(statement).first()

def get_all_tipos_caso(session: Session, skip: int = 0, limit: int = 100) -> List[TipoCaso]:
    """Obtiene una lista de todos los tipos de caso."""
    statement = select(TipoCaso).offset(skip).limit(limit)
    return list(session.exec(statement).all())