from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from db.client import get_session
from schemas.user import UsuarioCreate, UsuarioRead
from crud.user import get_usuario, get_usuarios, create_usuario, delete_usuario, get_usuario_email
from typing import List

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/", response_model=List[UsuarioRead])
async def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return await get_usuarios(db, skip, limit)

@router.get("/{usuario_id}", response_model=UsuarioRead)
async def leer_usuario(usuario_id: int, db: Session = Depends(get_session)):
    usuario = get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/", response_model=UsuarioRead)
async def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_session)):
    db_usuario_existente_email = await get_usuario_email(db, email=usuario.email)
    if db_usuario_existente_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya está registrado")
    return await create_usuario(db, usuario)


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(usuario_id: int, db: Session = Depends(get_session)):
    usuario_to_delete = get_usuario(db, usuario_id)
    if not usuario_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    success = await delete_usuario(db, usuario_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar el usuario")
    return True