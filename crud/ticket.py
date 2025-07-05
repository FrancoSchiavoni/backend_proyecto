from sqlmodel import Session, select
from db.models.ticket import Ticket
from db.models.cliente import Cliente
from db.models.user import Usuario
from schemas.ticket import TicketConIntervenciones
#from schemas.ticket import UsuarioCreate


def get_ticket(db: Session, ticket_id: int):
    return db.get(Ticket, ticket_id)

async def get_all_tickets(db: Session):
    statement = select(Ticket, Cliente, Usuario).join(Usuario, Ticket.id_personal_asignado == Usuario.id_personal).join(Cliente, Ticket.id_cliente == Cliente.id_cliente)
    tickets = db.exec(statement).all()
    return tickets

async def get_tickets_by_user(db: Session, user_id: int):
    statement = select(Ticket).where(Ticket.id_personal_asignado == user_id)
    tickets = db.exec(statement).all()
    return tickets

async def create_ticket(db: Session, ticket: Ticket):
    nuevo_ticket = Ticket.model_validate(ticket)
    db.add(nuevo_ticket)
    db.commit()
    db.refresh(nuevo_ticket)
    return nuevo_ticket


async def filter_tickets(db: Session, client_id, id_personal_asignado, id_estado):
    statement = select(Ticket)
    
    if client_id is not None:
        statement = statement.where(Ticket.id_cliente == client_id)
    
    if id_personal_asignado is not None:
        statement = statement.where(Ticket.id_personal_asignado == id_personal_asignado)
    
    if id_estado is not None:
        statement = statement.where(Ticket.id_estado == id_estado)
    
    tickets = db.exec(statement).all()
    return tickets