from typing import List, Optional
from sqlmodel import Session, select
from db.models.user_tipocaso import UserTipoCaso # Importamos el modelo SQLModel

def get_user_tipocaso_by_ids(session: Session,id_tipo_usuario: int,id_tipo_caso: int) -> Optional[UserTipoCaso]:
    """Obtiene un registro user_tipocaso por sus IDs compuestos."""
    statement = select(UserTipoCaso).where(
        UserTipoCaso.ID_TipoUsuario == id_tipo_usuario,
        UserTipoCaso.ID_TipoCaso == id_tipo_caso
    )
    return session.exec(statement).first()

def get_user_tipocasos_by_tipo_usuario(session: Session, id_tipo_usuario: int) -> List[UserTipoCaso]:
    """Obtiene todos los tipos de caso asociados a un tipo de usuario específico."""
    statement = select(UserTipoCaso).where(UserTipoCaso.ID_TipoUsuario == id_tipo_usuario) 
    return list(session.exec(statement).all())

def get_user_tipocasos_by_tipo_caso(session: Session, id_tipo_caso: int) -> List[UserTipoCaso]:
    """Obtiene todos los tipos de usuario asociados a un tipo de caso específico."""
    statement = select(UserTipoCaso).where(UserTipoCaso.ID_TipoCaso == id_tipo_caso)
    return list(session.exec(statement).all())

def get_all_user_tipocasos(session: Session) -> List[UserTipoCaso]:
    """Obtiene una lista de todos los registros user_tipocaso."""
    statement = select(UserTipoCaso)
    return list(session.exec(statement).all())