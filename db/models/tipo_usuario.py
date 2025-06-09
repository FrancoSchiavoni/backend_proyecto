# db/modelos/tipo_usuario.py
from typing import Optional
from sqlmodel import Field, SQLModel

class TipoUsuarioBase(SQLModel):
    nombre: str = Field(index=True)

class TipoUsuario(TipoUsuarioBase, table=True):
    __tablename__ = "tipo_usuario"

    ID_Tipo: Optional[int] = Field(default=None, primary_key=True)

    # NO incluimos relaciones todavia.
    # from typing import List
    # from sqlmodel import Relationship
    # user_tipocasos: List["UserTipoCaso"] = Relationship(back_populates="tipo_usuario")
    # usuarios: List["Usuario"] = Relationship(back_populates="tipo_usuario")