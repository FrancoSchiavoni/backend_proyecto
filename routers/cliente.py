from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.client import get_session
from db.models.cliente import Cliente
from crud.cliente import get_cliente, get_clientes, create_cliente
from typing import List


router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("/", response_model=List[Cliente])
async def listar_clientes(skip: int = 0,  db: Session = Depends(get_session)):
    return await get_clientes(db, skip)


@router.get("/{cliente_id}", response_model=Cliente)
async def leer_cliente(cliente_id: int, db: Session = Depends(get_session)):
    cliente = get_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.post("/", response_model=Cliente)
async def crear_cliente(cliente: Cliente, db: Session = Depends(get_session)):
    return await create_cliente(db, cliente)    