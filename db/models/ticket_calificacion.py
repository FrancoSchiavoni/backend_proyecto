from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime  

class TicketCalificacion(SQLModel, table=True):
    id_calificacion: Optional[int] = Field(default=None, primary_key=True)
    id_caso: Optional[int] = Field(default=None, foreign_key="ticket.id_caso")
    puntuacion: Optional[int] = Field(default=None)
    comentario_cliente: Optional[str] = Field(default=None)
    fecha_calificacion: Optional[datetime] = Field(default=None)
    token_calificacion: str = Field(index=True, unique=True)
    token_usado: bool = Field(default=False)