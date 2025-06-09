from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from schemas.ticket import TicketRead


class TicketIntervencionBase(SQLModel):
    fecha_vencimiento: datetime
    fecha: datetime
    id_tipo_intervencion: int
    detalle: str
    tiempo_utilizado: int
    id_contacto: int


class IntervencionReadSinTicket(TicketIntervencionBase):
    id_caso: int
    id_intervencion: int

class IntervencionRead(TicketIntervencionBase):
    id_caso: int
    id_intervencion: int
    ticket: Optional[TicketRead] = None



class IntervencionCreate(TicketIntervencionBase):
    pass