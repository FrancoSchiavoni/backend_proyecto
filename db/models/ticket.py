
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional,Union,List,TYPE_CHECKING
from datetime import datetime
if TYPE_CHECKING:
    from db.models.adjunto import Adjunto
from typing import List
if TYPE_CHECKING:
    from db.models.ticket_intervencion import TicketIntervencion

    
class Ticket(SQLModel, table=True):
    id_caso: Union[int, None] = Field(default=None, primary_key=True)
    fecha: Union[datetime, None] = Field(default=None)
    titulo: str = Field(max_length=500)
    id_cliente: int
    id_personal_creador: int
    id_personal_asignado: int
    id_tipocaso: int
    id_estado: int
    id_prioridad: int
    ultima_modificacion: Union[datetime, None] = Field(default=None)
    fecha_tentativa_inicio: Union[datetime, None] = Field(default=None)
    fecha_tentativa_finalizacion: Union[datetime, None] = Field(default=None)
    adjuntos: Optional[List["Adjunto"]] = Relationship(back_populates="ticket")
    intervenciones: list["TicketIntervencion"] = Relationship(back_populates="ticket")