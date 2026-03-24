from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class TicketVisitaCreate(SQLModel):
    id_caso: int
    fecha_inicio: datetime
    fecha_fin: datetime
    descripcion: Optional[str] = Field(default=None, max_length=1000)
    id_personal_asignado: int
    estado_visita: str = Field(default="pendiente", max_length=20)


class TicketVisitaUpdate(SQLModel):
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    descripcion: Optional[str] = Field(default=None, max_length=1000)
    id_personal_asignado: Optional[int] = None
    estado_visita: Optional[str] = Field(default=None, max_length=20)


class TicketVisitaRead(SQLModel):
    id_visita: int
    id_caso: int
    fecha_inicio: datetime
    fecha_fin: datetime
    descripcion: Optional[str] = None
    id_personal_asignado: int
    estado_visita: str
    fecha_creacion: Optional[datetime] = None
