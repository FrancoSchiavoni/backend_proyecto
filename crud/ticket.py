from sqlmodel import Session, func, select, case
from db.models.ticket import Ticket
from db.models.cliente import Cliente
from db.models.user import Usuario
from schemas.ticket import TicketUpdate
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
    statement = select(Ticket, Cliente, Usuario).join(Usuario, Ticket.id_personal_asignado == Usuario.id_personal).join(Cliente, Ticket.id_cliente == Cliente.id_cliente)
    if client_id is not None:
        statement = statement.where(Ticket.id_cliente == client_id)
    
    if id_personal_asignado is not None:
        print(id_personal_asignado)
        statement = statement.where(Ticket.id_personal_asignado == id_personal_asignado)
    
    if id_estado is not None:
        statement = statement.where(Ticket.id_estado == id_estado)
    

    tickets = db.exec(statement).all()
    return tickets

def update_ticket(db: Session, ticket_id: int, ticket_update: TicketUpdate) -> Ticket: # USA TicketUpdate
    db_ticket = db.get(Ticket, ticket_id)
    if not db_ticket:
        return None

    # model_dump(exclude_unset=True) para solo actualizar los campos que vienen en la petición
    ticket_data = ticket_update.model_dump(exclude_unset=True)
    for key, value in ticket_data.items():
        setattr(db_ticket, key, value)

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


# funciones de estadisticas de tickets

# tickets por estado
async def count_tickets_by_status(db: Session):
    statement = select(Ticket.id_estado, func.count().label("count")).group_by(Ticket.id_estado)
    rows = db.exec(statement).all()
    # Convert SQLAlchemy Row objects to plain dicts for safe JSON serialization
    return [{"id_estado": row[0], "count": row[1]} for row in rows]

# tickets creados los ultimos 7 dias
async def count_tickets_last_7_days(db: Session):
    from datetime import datetime, timedelta
    seven_days_ago = datetime.now() - timedelta(days=7)
    statement = select(func.count().label("count")).where(Ticket.fecha >= seven_days_ago)
    # Return scalar int instead of Row
    return db.exec(statement).one()

# tiempo promedio de resolucion de tickets (en dias)
async def average_ticket_resolution_time(db: Session):
    from datetime import datetime
    statement = select(func.avg(func.julianday(Ticket.ultima_modificacion) - func.julianday(Ticket.fecha)).label("avg_resolution_time")).where(Ticket.id_estado == 3).where(Ticket.ultima_modificacion != None)
    # Return scalar float (days). Could be None if no data; normalize to 0.0
    avg_days = db.exec(statement).one_or_none()
    return float(avg_days) if avg_days is not None else 0.0

# tickets completados en los ultimos 7 dias
async def count_completed_tickets_last_7_days(db: Session):
    from datetime import datetime, timedelta
    seven_days_ago = datetime.now() - timedelta(days=7)
    statement = select(func.count().label("count")).where(Ticket.id_estado == 3).where(Ticket.ultima_modificacion >= seven_days_ago)
    # Return scalar int instead of Row
    return db.exec(statement).one()


# tickets por tecnico por estado
async def count_tickets_by_technician_and_status(db: Session):
    # Use conditional aggregation (CASE WHEN) to pivot estados into columns
    statement = select(
        Ticket.id_personal_asignado,
        Usuario.nombre,
        func.sum(case((Ticket.id_estado == 1, 1), else_=0)).label("pendientes"),
        func.sum(case((Ticket.id_estado == 2, 1), else_=0)).label("en_progreso"),
        func.sum(case((Ticket.id_estado == 3, 1), else_=0)).label("finalizados"),
        func.sum(case((Ticket.id_estado == 4, 1), else_=0)).label("cancelados"),
    ).join(Usuario, Ticket.id_personal_asignado == Usuario.id_personal).group_by(Ticket.id_personal_asignado, Usuario.nombre)
    
    rows = db.exec(statement).all()
    # Convert to dicts with one row per technician, columns for each estado
    return [
        {
            "id_personal_asignado": row[0],
            "nombre_tecnico": row[1],
            "pendientes": row[2],
            "en_progreso": row[3],
            "finalizados": row[4],
            "cancelados": row[5],
        }
        for row in rows
    ]