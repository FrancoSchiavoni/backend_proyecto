from typing import Optional
from sqlmodel import Field, SQLModel

class EstadoBase(SQLModel):
    nombre: str = Field(index=True)
    color: int

class Estado(EstadoBase, table=True):
    ID_Estado: Optional[int] = Field(default=None, primary_key=True)

