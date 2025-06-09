from typing import Optional
from sqlmodel import Field, SQLModel

class PrioridadBase(SQLModel):
    nombre: str = Field(index=True)
    color: int

class Prioridad(PrioridadBase, table=True):

    ID_Prioridad: Optional[int] = Field(default=None, primary_key=True)

    # Puedes añadir relaciones aquí si las necesitas con la tabla 'ticket'
    # Por ejemplo, si un ticket tiene una prioridad:
    # from typing import List
    # from sqlmodel import Relationship
    # tickets: List["Ticket"] = Relationship(back_populates="prioridad")
    # (Necesitarías definir Ticket en db/models/ticket.py y la relación inversa allí)