from typing import Optional
from sqlmodel import Field, SQLModel

class PrioridadBase(SQLModel):
    nombre: str = Field(index=True)
    color: int

class Prioridad(PrioridadBase, table=True):
    ID_Prioridad: Optional[int] = Field(default=None, primary_key=True)