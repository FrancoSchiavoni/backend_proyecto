from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from db.models.ticket import Ticket


class TicketVisita(SQLModel, table=True):
    __tablename__ = "ticket_visita"

    id_visita: Optional[int] = Field(default=None, primary_key=True)
    id_caso: int = Field(foreign_key="ticket.id_caso")
    fecha_inicio: datetime
    fecha_fin: datetime
    descripcion: Optional[str] = Field(default=None, max_length=1000)
    id_personal_asignado: int
    # Estado: pendiente, confirmada, completada, cancelada
    estado_visita: str = Field(default="pendiente", max_length=20)
    fecha_creacion: Optional[datetime] = Field(default_factory=datetime.utcnow)

    ticket: Optional["Ticket"] = Relationship(back_populates="visitas")
