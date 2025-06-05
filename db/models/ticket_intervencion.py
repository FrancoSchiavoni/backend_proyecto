from sqlmodel import SQLModel, Field
from typing import Optional,Union
from datetime import datetime

class TicketIntervencion(SQLModel, table=True):
    id_caso: int
    id_intervencion: Optional[int] = Field(default=None, primary_key=True) 
    fecha_vencimiento: datetime
    fecha: datetime
    id_tipo_intervencion: int
    detalle: str
    tiempo_utilizado: int
    id_contacto: int