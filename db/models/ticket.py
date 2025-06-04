
from sqlmodel import SQLModel, Field
from typing import Optional,Union
from datetime import datetime

    
class Ticket(SQLModel, table=True):
    id_caso: Union[int, None] = Field(default=None, primary_key=True)
    fecha: Union[datetime, None] = Field(default=None)
    titulo: str = Field(max_length=500)
    id_cliente: int
    id_personal_creador: int
    id_personal_asignado: int
    id_tipocaso: int
    id_estado: int
    id_prioridad: int
    ultima_modificacion: Union[datetime, None] = Field(default=None)
    fecha_tentativa_inicio: Union[datetime, None] = Field(default=None)
    fecha_tentativa_finalizacion: Union[datetime, None] = Field(default=None)
