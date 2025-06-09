from sqlmodel import Session, select
from db.models.cliente import Cliente

def get_cliente(db: Session, cliente_id: int):
    return db.get(Cliente, cliente_id)

async def get_clientes(db: Session, skip: int = 0):
    return db.exec(select(Cliente).offset(skip)).all()

async def create_cliente(db: Session, cliente: Cliente):
    nuevo_cliente = Cliente.model_validate(cliente)
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


