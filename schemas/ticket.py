from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
from sqlmodel import SQLModel, Field
from schemas.cliente import ClienteRead
from schemas.ticket_visita import TicketVisitaRead


class TicketBase(SQLModel):
    titulo: str = Field(max_length=500)
    descripcion: str = Field(max_length=2000)
    telefono_contacto: Optional[str] = Field(default=None, max_length=50)
    id_cliente: int
    id_personal_creador: int
    id_personal_asignado: int
    id_tipocaso: int
    id_estado: int
    id_prioridad: int

class TicketRead(TicketBase):
    id_caso: int
    fecha: Optional[datetime] = None
    ultima_modificacion: Optional[datetime] = None

class TicketIntervencionBase(SQLModel):
    fecha_vencimiento: datetime
    fecha: datetime
    id_tipo_intervencion: int
    detalle: str
    tiempo_utilizado: int
    id_contacto: str = ""
    tipo_intervencion_label: Optional[str] = None

class TicketConIntervenciones(TicketRead):
    intervenciones: list[TicketIntervencionBase] = []
    visitas: list[TicketVisitaRead] = []
    cliente: Optional[ClienteRead] = None
    tecnico: Optional[str] = None

class TicketUpdate(SQLModel):
    titulo: Optional[str] = Field(default=None, max_length=500)
    descripcion: Optional[str] = Field(default=None, max_length=2000)
    id_cliente: Optional[int] = None
    id_personal_creador: Optional[int] = None
    id_personal_asignado: Optional[int] = None
    id_tipocaso: Optional[int] = None
    id_estado: Optional[int] = None
    id_prioridad: Optional[int] = None
    telefono_contacto: Optional[str] = Field(default=None, max_length=50)
    ultima_modificacion: Optional[datetime] = datetime.utcnow()
