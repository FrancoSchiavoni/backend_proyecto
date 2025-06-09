# routers/tipo_usuario.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.models.tipo_usuario import TipoUsuario 
from crud.tipo_usuario import get_all_tipos_usuario, get_tipo_usuario_by_id 
from db.client import get_session 

router = APIRouter(
    prefix="/tipos_usuario",
    tags=["tipos_usuario"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[TipoUsuario])
def read_all_tipos_usuario(session: Session = Depends(get_session)):
    """
    Obtiene una lista de todos los tipos de usuario.
    """
    tipos_usuario = get_all_tipos_usuario(session)
    return tipos_usuario

@router.get("/{tipo_usuario_id}", response_model=TipoUsuario)
def read_tipo_usuario_by_id(tipo_usuario_id: int, session: Session = Depends(get_session)):
    """
    Obtiene un tipo de usuario específico por su ID.
    """
    db_tipo_usuario = get_tipo_usuario_by_id(session, tipo_usuario_id=tipo_usuario_id)
    if not db_tipo_usuario:
        raise HTTPException(status_code=404, detail="Tipo de Usuario not found")
    return db_tipo_usuario