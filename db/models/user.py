from sqlmodel import SQLModel, Field
from typing import Optional,Union
from datetime import datetime

class Usuario(SQLModel, table=True):
    id_personal: Union[int, None] = Field(default=None, primary_key=True)
    id_sucursal: int
    id_tipo: int
    nombre: str = Field(max_length=100)
    telefono_movil: Union[str, None] = Field(default=None, max_length=50)
    email: Union[str, None] = Field(default=None, max_length=100)
    fecha_ingreso: Union[datetime, None] = None
    fecha_egreso: Union[datetime, None] = None
    password: str