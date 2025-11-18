from sqlalchemy import func
from sqlmodel import Session, select
from db.models.ticket_calificacion import TicketCalificacion
from db.models.ticket import Ticket
from db.models.cliente import Cliente
from datetime import datetime
from typing import Optional
import uuid
import httpx
import logging

logger = logging.getLogger(__name__)

WEBHOOK_URL = "https://n8n.srv1039921.hstgr.cloud/webhook-test/csat-survey-trigger"


def get_calificacion_by_token(db: Session, token: str) -> Optional[TicketCalificacion]:
    """Obtiene una calificación por su token"""
    statement = select(TicketCalificacion).where(TicketCalificacion.token_calificacion == token)
    return db.exec(statement).first()


def get_calificacion_by_ticket(db: Session, id_caso: int) -> Optional[TicketCalificacion]:
    """Obtiene una calificación por ID de ticket"""
    statement = select(TicketCalificacion).where(TicketCalificacion.id_caso == id_caso)
    return db.exec(statement).first()


def create_calificacion_token(db: Session, id_caso: int) -> TicketCalificacion:
    """
    Crea un registro de calificación con token único cuando se cierra un ticket.
    Se invoca automáticamente al cambiar el estado del ticket a 'Resuelto' o 'Cerrado'.
    Envía webhook a n8n con email del cliente y token.
    """
    # Verificar si ya existe una calificación para este ticket
    existing = get_calificacion_by_ticket(db, id_caso)
    if existing:
        return existing  # Ya existe, no crear duplicado
    
    # Generar token único
    token = str(uuid.uuid4())
    
    # Crear registro vacío listo para usar
    nueva_calificacion = TicketCalificacion(
        id_caso=id_caso,
        token_calificacion=token,
        token_usado=False
    )
    
    db.add(nueva_calificacion)
    db.commit()
    db.refresh(nueva_calificacion)
    
    # Obtener email del cliente para enviar al webhook
    ticket = db.get(Ticket, id_caso)
    if ticket:
        cliente = db.get(Cliente, ticket.id_cliente)
        if cliente and cliente.email:
            # Enviar webhook a n8n
            try:
                with httpx.Client(timeout=10.0) as client:
                    response = client.post(
                        WEBHOOK_URL,
                        json={
                            "mail": cliente.email,
                            "token": token
                        }
                    )
                    response.raise_for_status()
                    logger.info(f"Webhook enviado exitosamente para ticket {id_caso}, token: {token}")
            except httpx.HTTPError as e:
                logger.error(f"Error al enviar webhook para ticket {id_caso}: {str(e)}")
                # No fallar la creación del token si el webhook falla
            except Exception as e:
                logger.error(f"Error inesperado al enviar webhook: {str(e)}")
        else:
            logger.warning(f"No se encontró email para el cliente del ticket {id_caso}")
    
    return nueva_calificacion


def update_calificacion(
    db: Session, 
    calificacion: TicketCalificacion, 
    puntuacion: int, 
    comentario: str
) -> TicketCalificacion:
    """Actualiza una calificación con la puntuación y comentario del cliente"""
    calificacion.puntuacion = puntuacion
    calificacion.comentario_cliente = comentario
    calificacion.fecha_calificacion = datetime.utcnow()
    calificacion.token_usado = True
    
    db.add(calificacion)
    db.commit()
    db.refresh(calificacion)
    return calificacion


# promedio de calificacion de tickets de la tabla ticket_calificacion
async def average_ticket_rating(db: Session):
    statement = select(func.avg(TicketCalificacion.puntuacion).label("avg_rating"))
    rows = db.exec(statement).one()
    return float(rows) if rows is not None else 0.0
