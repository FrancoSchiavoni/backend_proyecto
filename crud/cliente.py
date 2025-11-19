from sqlmodel import Session, select
from db.models.cliente import Cliente
from schemas.cliente import ClienteCreate 

def get_cliente(db: Session, cliente_id: int):
    return db.get(Cliente, cliente_id)

def get_cliente_by_email(db: Session, email: str):
    statement = select(Cliente).where(Cliente.email == email)
    return db.exec(statement).first()

async def get_clientes(db: Session, skip: int = 0):
    return db.exec(select(Cliente).offset(skip)).all()

async def create_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Cliente.model_validate(cliente)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def update_cliente(db: Session, cliente_id: int, cliente_data: Cliente):
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        return None

    update_data = cliente_data.model_dump(exclude_unset=False) # Para PUT

    for key, value in update_data.items():
        setattr(db_cliente, key, value)

    db.commit()
    db.refresh(db_cliente)
    return db_cliente
