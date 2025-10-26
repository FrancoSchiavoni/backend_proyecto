from sqlmodel import select, Session
from db.models.ticket_intervencion import TicketIntervencion
from schemas.ticket_intervencion import TicketIntervencionBase, IntervencionRead, IntervencionCreate, IntervencionReadSinTicket


def get_intervencion(db: Session, id_intervencion: int):
    return db.get(TicketIntervencion, id_intervencion)


def get_tipo_intervencion_label(id_tipo_intervencion: int) -> str:
    """Obtiene el nombre del tipo de intervención por su ID (valores fijos)"""
    tipos = {
        1: "Soporte Técnico",
        2: "Mantenimiento",
        3: "Instalación",
        4: "Actualización de datos",
    }
    return tipos.get(id_tipo_intervencion, "Desconocido")



async def get_intervenciones_ticket(db: Session, ticket_id: int, skip: int = 0, limit: int = 100):
    statement = select(TicketIntervencion).where(TicketIntervencion.id_caso == ticket_id).offset(skip).limit(limit)
    intervenciones = db.exec(statement).all()
    
    # Agregar labels a cada intervención usando el schema base
    result = []
    for intervencion in intervenciones:
        label = get_tipo_intervencion_label(intervencion.id_tipo_intervencion)
        # Convertir el modelo a un dict y agregar el label
        intervention_data = intervencion.model_dump()
        intervention_data['tipo_intervencion_label'] = label
        result.append(intervention_data)
    
    return result


async def create_intervencion(db: Session, ticket_id: int, intervencion: IntervencionCreate):
    new_intervencion = TicketIntervencion(
        id_caso=ticket_id,
        **intervencion.model_dump(exclude_unset=True)
    )
    db.add(new_intervencion)
    db.commit()
    db.refresh(new_intervencion)
    
    # Agregar label al resultado
    result = IntervencionRead.model_validate(new_intervencion)
    result.tipo_intervencion_label = get_tipo_intervencion_label(new_intervencion.id_tipo_intervencion)
    return result