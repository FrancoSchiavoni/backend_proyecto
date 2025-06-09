from typing import Optional
from sqlmodel import Field, SQLModel

class TipoCasoBase(SQLModel):
    nombre: str = Field(index=True)
    color: int

class TipoCaso(TipoCasoBase, table=True):
    ID_TipoCaso: Optional[int] = Field(default=None, primary_key=True)

    # Si necesitas una relación con la tabla 'ticket' (ej. un ticket tiene un tipo de caso):
    # from typing import List
    # from sqlmodel import Relationship
    # tickets: List["Ticket"] = Relationship(back_populates="tipo_caso")
    # (Esto requeriría que definas el modelo Ticket en db/modelos/ticket.py
    # y la relación inversa en ese modelo también)