from sqlmodel import SQLModel, Field, Relationship
from typing import Optional,Union, List, TYPE_CHECKING
from datetime import datetime
if TYPE_CHECKING:
    from db.models.adjunto import Adjunto

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
    activo: bool = Field(default=True)
    profile_photo_url: Union[str, None] = Field(default=None, max_length=255)
    adjuntos: Optional[List["Adjunto"]] = Relationship(back_populates="usuario_autor")