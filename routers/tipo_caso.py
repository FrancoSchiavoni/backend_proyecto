# routers/tipo_caso.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.models.tipo_caso import TipoCaso # El modelo SQLModel, que también funciona como Pydantic
from crud.tipo_caso import get_all_tipos_caso, get_tipo_caso_by_id
from db.client import get_session # Nuestra dependencia de sesión de DB

router = APIRouter(
    prefix="/tipos_caso", # El prefijo de la URL para este router
    tags=["tipos_caso"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[TipoCaso])
def read_all_tipos_caso(session: Session = Depends(get_session)):
    """
    Obtiene una lista de todos los tipos de caso.
    """
    tipos_caso = get_all_tipos_caso(session)
    return tipos_caso

@router.get("/{tipo_caso_id}", response_model=TipoCaso)
def read_tipo_caso_by_id(tipo_caso_id: int, session: Session = Depends(get_session)):
    """
    Obtiene un tipo de caso específico por su ID.
    """
    db_tipo_caso = get_tipo_caso_by_id(session, tipo_caso_id=tipo_caso_id)
    if not db_tipo_caso:
        raise HTTPException(status_code=404, detail="Tipo de Caso not found")
    return db_tipo_caso