from datetime import datetime
from typing import Optional,TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship
if TYPE_CHECKING:
    from db.models.ticket import Ticket
    from db.models.user import Usuario

class AdjuntoBase(SQLModel):
    id_caso: Optional[int] = Field(default=None, foreign_key="ticket.id_caso")
    id_usuario_autor: Optional[int] = Field(default=None, foreign_key="usuario.id_personal")
    filename: str = Field(index=True)
    filepath: str 
    fecha: datetime = Field(default_factory=datetime.now)

class Adjunto(AdjuntoBase, table=True):
    id_adjunto: Optional[int] = Field(default=None, primary_key=True)
    ticket: Optional["Ticket"] = Relationship(back_populates="adjuntos")
    usuario_autor: Optional["Usuario"] = Relationship(back_populates="adjuntos")
