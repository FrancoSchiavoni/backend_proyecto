from sqlmodel import SQLModel, Field, Relationship
from typing import Optional,TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from db.models.ticket import Ticket


class TicketIntervencion(SQLModel, table=True):
    id_caso: Optional[int] = Field(default=None, foreign_key="ticket.id_caso")
    id_intervencion: Optional[int] = Field(default=None, primary_key=True) 
    fecha_vencimiento: datetime
    fecha: datetime
    id_tipo_intervencion: int
    detalle: str
    tiempo_utilizado: int
    id_contacto: int
    ticket: Optional["Ticket"] = Relationship(back_populates="intervenciones")