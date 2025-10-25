# schemas/cliente.py
from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field

# Schema para la creación de un Cliente (lo que recibe el endpoint POST)
class ClienteCreate(SQLModel):
    razonsocial: str = Field(max_length=100)
    domicilio: Optional[str] = Field(default=None, max_length=100)
    id_localidad: Optional[int] = Field(default=None)
    codigopostal: Optional[str] = Field(default=None, max_length=20)
    telefono: Optional[str] = Field(default=None, max_length=50)
    telefonomovil: Optional[str] = Field(default=None, max_length=50)
    email: Optional[str] = Field(default=None, max_length=100)
    cuit: Optional[str] = Field(default=None, max_length=50)
    id_tipocliente: Optional[int] = Field(default=None)
    activo: bool = Field(default=True)
    fecha_baja: Optional[datetime] = None

# Schema para la lectura de un Cliente (lo que devuelve la API)
class ClienteRead(ClienteCreate):
    id_cliente: int