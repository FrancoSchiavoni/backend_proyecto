from sqlmodel import select, Session
from db.models.ticket_intervencion import TicketIntervencion
from schemas.ticket_intervencion import TicketIntervencionBase, IntervencionRead, IntervencionCreate


def get_intervencion(db: Session, id_intervencion: int):
    return db.get(TicketIntervencion, id_intervencion)



async def get_intervenciones_ticket(db: Session, ticket_id: int, skip: int = 0, limit: int = 100):
    statement = select(TicketIntervencion).where(TicketIntervencion.id_caso == ticket_id).offset(skip).limit(limit)
    return db.exec(statement).all()


async def create_intervencion(db: Session, ticket_id: int, intervencion: IntervencionCreate):
    new_intervencion = TicketIntervencion(
        id_caso=ticket_id,
        **intervencion.model_dump(exclude_unset=True)
    )
    db.add(new_intervencion)
    db.commit()
    db.refresh(new_intervencion)
    return IntervencionRead.model_validate(new_intervencion)