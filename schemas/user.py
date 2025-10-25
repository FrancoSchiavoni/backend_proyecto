from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from datetime import date
from pydantic import BaseModel

class UsuarioBase(SQLModel):
    id_sucursal: int
    id_tipo: int
    nombre: str
    telefono_movil: Optional[str] = None
    email: Optional[str] = None
    fecha_ingreso: Optional[datetime] = None
    fecha_egreso: Optional[datetime] = None
    profile_photo_url: Optional[str] = None
    activo: Optional[bool] = None
class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioRead(UsuarioBase):
    id_personal: int

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono_movil: Optional[str] = None
    id_sucursal: Optional[int] = None
    id_tipo: Optional[int] = None
    activo: Optional[bool] = None
    fecha_ingreso: Optional[datetime] = None
    fecha_egreso: Optional[datetime] = None
    profile_photo_url: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

