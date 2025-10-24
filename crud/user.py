from typing import Optional
from sqlmodel import Session, select
from db.models.user import Usuario
from schemas.user import UsuarioCreate
from schemas.user import UserUpdate
from settings.security import get_password_hash

def get_usuario(db: Session, usuario_id: int):
    return db.get(Usuario, usuario_id)

async def get_usuario_email(db: Session, email: str):
    statement = select(Usuario).where(Usuario.email == email)
    user = db.exec(statement).first()
    return user

async def get_usuarios(db: Session, skip: int = 0, limit: int = 100, id_tipo: Optional[int] = None):
    query = select(Usuario)
    if id_tipo is not None:
        query = query.where(Usuario.id_tipo == id_tipo)
    query = query.offset(skip).limit(limit)
    usuarios = db.exec(query).all()
    return usuarios

async def create_usuario(db: Session, usuario: UsuarioCreate):
    nuevo_usuario = Usuario.model_validate(usuario)
    hashed_password = get_password_hash(nuevo_usuario.password)
    nuevo_usuario.password = hashed_password
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

async def delete_usuario(db: Session, usuario_id: int) -> bool:
    usuario = db.get(Usuario, usuario_id) # Using db.get for primary key lookup
    if usuario:
        db.delete(usuario)
        db.commit()
        return True
    return False

async def change_user_password(db: Session, user: Usuario, new_password: str):
    """
    Cambia la contraseña de un usuario en la base de datos usando SQLModel.
    """
    hashed_new_password = get_password_hash(new_password)
    user.password = hashed_new_password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user




async def update_user(db: Session, user_id: int, user_update_data: UserUpdate):
    """
    Actualiza un usuario en la base de datos usando SQLModel.
    """
    
    # 1. Buscar el usuario (usamos db.get, igual que en tu delete_usuario)
    # db.get es síncrono, pero está bien llamarlo dentro de un async def
    # que FastAPI corre en un threadpool.
    db_user = db.get(Usuario, user_id)

    if db_user is None:
        return None  # No se encontró el usuario

    # 2. Obtener los datos del schema como un diccionario
    # exclude_unset=True asegura que solo actualicemos los campos que se enviaron
    update_data = user_update_data.model_dump(exclude_unset=True)

    # 3. Actualizar el objeto de la base de datos
    # SQLModel 0.0.12+ prefiere .sqlmodel_update() pero setattr es universal
    for key, value in update_data.items():
        setattr(db_user, key, value)

    # 4. Guardar los cambios (igual que en tu create_usuario)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user