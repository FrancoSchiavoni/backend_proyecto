from sqlmodel import Session, select
from db.models.user import Usuario
from schemas.user import UsuarioCreate

def get_usuario(db: Session, usuario_id: int):
    return db.get(Usuario, usuario_id)

async def get_usuario_email(db: Session, email: str):
    statement = select(Usuario).where(Usuario.email == email)
    user = db.exec(statement).first()
    return user

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.exec(select(Usuario).offset(skip).limit(limit)).all()

async def create_usuario(db: Session, usuario: UsuarioCreate):
    nuevo_usuario = Usuario.model_validate(usuario)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario