from pydantic import BaseModel, Field
from typing import Optional


class CalificacionRequest(BaseModel):
    """Schema para recibir la calificación del cliente"""
    puntuacion: int = Field(..., ge=1, le=5, description="Puntuación del 1 al 5")
    comentario: Optional[str] = Field(default="", max_length=500, description="Comentario opcional del cliente")


class CalificacionTokenResponse(BaseModel):
    """Schema para la respuesta del GET con información del ticket"""
    id_caso: int
    titulo: str
    descripcion: Optional[str] = None
    
    class Config:
        from_attributes = True


class CalificacionSubmitResponse(BaseModel):
    """Schema para la respuesta del POST tras enviar la calificación"""
    message: str
    id_calificacion: int
