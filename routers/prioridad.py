# routers/prioridad.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.models.prioridad import Prioridad 
from crud.prioridad import get_all_prioridades, get_prioridad_by_id
from db.client import get_session # Nuestra dependencia de sesión de DB

router = APIRouter(
    prefix="/prioridades",
    tags=["prioridades"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Prioridad])
def read_all_prioridades(session: Session = Depends(get_session)):
    """
    Obtiene una lista de todas las prioridades.
    """
    prioridades = get_all_prioridades(session)
    return prioridades

@router.get("/{prioridad_id}", response_model=Prioridad)
def read_prioridad_by_id(prioridad_id: int, session: Session = Depends(get_session)):
    """
    Obtiene una prioridad específica por su ID.
    """
    db_prioridad = get_prioridad_by_id(session, prioridad_id=prioridad_id)
    if not db_prioridad:
        raise HTTPException(status_code=404, detail="Prioridad not found")
    return db_prioridad