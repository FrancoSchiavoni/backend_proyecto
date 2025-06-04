from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.client import get_session
from schemas.user import UsuarioCreate, UsuarioRead
from crud.user import get_usuario, get_usuarios, create_usuario
from typing import List

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/", response_model=List[UsuarioRead])
async def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return get_usuarios(db, skip, limit)

@router.get("/{usuario_id}", response_model=UsuarioRead)
async def leer_usuario(usuario_id: int, db: Session = Depends(get_session)):
    usuario = get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/", response_model=UsuarioRead)
async def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_session)):
    return await create_usuario(db, usuario)