from typing import Optional
from sqlmodel import Field, SQLModel

class TipoCasoBase(SQLModel):
    nombre: str = Field(index=True)
    color: int

class TipoCaso(TipoCasoBase, table=True):
    ID_TipoCaso: Optional[int] = Field(default=None, primary_key=True)
