from sqlmodel import Session, select
from db.models.ticket import Ticket
#from schemas.ticket import UsuarioCreate


def get_ticket(db: Session, ticket_id: int):
    return db.get(Ticket, ticket_id)


async def get_all_tickets(db: Session):
    statement = select(Ticket)
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