from sqlmodel import SQLModel, Field
from typing import Optional,Union
from datetime import datetime


class Cliente(SQLModel, table=True):
    id_cliente: Optional[int] = Field(default=None, primary_key=True)
    razonsocial: str = Field(max_length=100)
    domicilio: Optional[str] = Field(default=None, max_length=100)
    id_localidad: Optional[int] = Field(default=None)
    codigopostal: Optional[str] = Field(default=None, max_length=20)
    telefono: Optional[str] = Field(default=None, max_length=50)
    telefonomovil: Optional[str] = Field(default=None, max_length=50)
    email: Optional[str] = Field(default=None, max_length=100)
    cuit: Optional[str] = Field(default=None, max_length=50)
    id_tipocliente: Optional[int] = Field(default=None)