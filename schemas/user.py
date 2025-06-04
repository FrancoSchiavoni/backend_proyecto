from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class UsuarioBase(SQLModel):
    id_sucursal: int
    id_tipo: int
    nombre: str
    telefono_movil: Optional[str] = None
    email: Optional[str] = None
    fecha_ingreso: Optional[datetime] = None
    fecha_egreso: Optional[datetime] = None

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioRead(UsuarioBase):
    id_personal: int