# routers/estado.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.models.estado import Estado
from crud.estado import get_all_estados, get_estado_by_id
from db.client import get_session 

router = APIRouter(
    prefix="/estados",
    tags=["estados"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Estado])
def read_all_estados(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """
    Obtiene una lista de todos los estados.
    """
    estados = get_all_estados(session, skip=skip, limit=limit)
    return estados

@router.get("/{estado_id}", response_model=Estado)
def read_estado_by_id(estado_id: int, session: Session = Depends(get_session)):
    """
    Obtiene un estado específico por su ID.
    """
    db_estado = get_estado_by_id(session, estado_id=estado_id)
    if not db_estado:
        raise HTTPException(status_code=404, detail="Estado not found")
    return db_estado