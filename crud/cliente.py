from sqlmodel import Session, select
from db.models.cliente import Cliente
from schemas.cliente import ClienteCreate 

def get_cliente(db: Session, cliente_id: int):
    return db.get(Cliente, cliente_id)

async def get_clientes(db: Session, skip: int = 0):
    return db.exec(select(Cliente).offset(skip)).all()

async def create_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Cliente.model_validate(cliente)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

