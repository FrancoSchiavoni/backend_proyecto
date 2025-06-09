# crud/tipo_usuario.py
from typing import List, Optional
from sqlmodel import Session, select
from db.models.tipo_usuario import TipoUsuario, TipoUsuarioBase # Importamos el modelo SQLModel

def get_tipo_usuario_by_id(session: Session, tipo_usuario_id: int) -> Optional[TipoUsuario]:
    """Obtiene un tipo de usuario por su ID."""
    statement = select(TipoUsuario).where(TipoUsuario.ID_Tipo == tipo_usuario_id)
    return session.exec(statement).first()

def get_all_tipos_usuario(session: Session, skip: int = 0, limit: int = 100) -> List[TipoUsuario]:
    """Obtiene una lista de todos los tipos de usuario."""
    statement = select(TipoUsuario).offset(skip).limit(limit)
    return list(session.exec(statement).all())

# Si necesitaras un create para TipoUsuario:
# def create_tipo_usuario(session: Session, tipo_usuario_create: TipoUsuarioBase) -> TipoUsuario:
#     db_tipo_usuario = TipoUsuario.model_validate(tipo_usuario_create)
#     session.add(db_tipo_usuario)
#     session.commit()
#     session.refresh(db_tipo_usuario)
#     return db_tipo_usuario