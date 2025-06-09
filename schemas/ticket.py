from typing import Optional,TYPE_CHECKING, List
from datetime import datetime
from sqlmodel import SQLModel, Field

class TicketBase(SQLModel):
    titulo: str = Field(max_length=500)
    id_cliente: int
    id_personal_creador: int
    id_personal_asignado: int
    id_tipocaso: int
    id_estado: int
    id_prioridad: int
    fecha_tentativa_inicio: Optional[datetime] = None
    fecha_tentativa_finalizacion: Optional[datetime] = None

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
    id_contacto: int

class TicketConIntervenciones(TicketRead):
    intervenciones: list[TicketIntervencionBase] = []



