from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

# Esquema base para Adjunto (lo que se envía o recibe)
class AdjuntoBase(SQLModel):
    id_caso: Optional[int] = Field(default=None)
    id_usuario_autor: Optional[int] = Field(default=None) 
    filename: str
    filepath: str 
    fecha: Optional[datetime] = None 

class AdjuntoCreate(SQLModel):
    id_caso: int


# Esquema para leer un Adjunto (incluye el ID generado)
class AdjuntoRead(AdjuntoBase):
    id_adjunto: int
    fecha: datetime 

# Esquema para actualizar un Adjunto (campos opcionales)
class AdjuntoUpdate(SQLModel):
    filename: Optional[str] = None
    filepath: Optional[str] = None