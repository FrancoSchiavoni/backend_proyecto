from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from db.client import get_session
from crud.ticket_calificacion import get_calificacion_by_token, update_calificacion, get_calificacion_by_ticket
from crud.ticket import get_ticket
from schemas.ticket_calificacion import (
    CalificacionRequest, 
    CalificacionTokenResponse, 
    CalificacionSubmitResponse,
    GetCalificacionResponse
)

router = APIRouter(prefix="/calificacion", tags=["calificacion"])

# get calification by id_caso
@router.get("/ticket/{id_caso}", response_model=GetCalificacionResponse)
async def obtener_calificacion(id_caso: int, db: Session = Depends(get_session)):
    """
    Obtiene la calificación asociada a un caso específico.
    
    - **id_caso**: ID del caso/ticket
    
    Retorna la calificación si existe, de lo contrario retorna un error 404.
    """
    # Buscar calificación por id_caso
    calificacion = get_calificacion_by_ticket(db, id_caso)
    
    # Validar que la calificación existe
    if not calificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calificación no encontrada para el caso especificado"
        )
    return GetCalificacionResponse(
        id_calificacion=calificacion.id_calificacion,
        id_caso=calificacion.id_caso,
        puntuacion=calificacion.puntuacion,
        comentario_cliente=calificacion.comentario_cliente,
        fecha_calificacion=calificacion.fecha_calificacion.isoformat() if calificacion.fecha_calificacion else None   
    )


@router.get("/{token}", response_model=CalificacionTokenResponse)
async def verificar_token_calificacion(token: str, db: Session = Depends(get_session)):
    """
    Verifica el token de calificación y devuelve información del ticket.
    
    - **token**: Token único de calificación
    
    Retorna los detalles del ticket para mostrar en la página de calificación.
    Si el token no existe o ya fue usado, devuelve error 410 (Gone).
    """
    # Buscar calificación por token
    calificacion = get_calificacion_by_token(db, token)
    
    # Validar que el token existe
    if not calificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token de calificación no encontrado"
        )
    
    # Validar que el token no haya sido usado
    if calificacion.token_usado:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Este token de calificación ya ha sido utilizado"
        )
    
    # Obtener información del ticket
    ticket = get_ticket(db, calificacion.id_caso)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket no encontrado"
        )
    
    # Devolver información del ticket para mostrar en la página
    return CalificacionTokenResponse(
        id_caso=ticket.id_caso,
        titulo=ticket.titulo,
        descripcion=ticket.descripcion
    )


@router.post("/{token}", response_model=CalificacionSubmitResponse)
async def enviar_calificacion(
    token: str, 
    calificacion_data: CalificacionRequest, 
    db: Session = Depends(get_session)
):
    """
    Recibe y guarda la calificación del cliente.
    
    - **token**: Token único de calificación
    - **puntuacion**: Puntuación del 1 al 5
    - **comentario**: Comentario opcional del cliente
    
    Marca el token como usado y guarda la calificación con la fecha actual.
    """
    # Buscar calificación por token
    calificacion = get_calificacion_by_token(db, token)
    
    # Validar que el token existe
    if not calificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token de calificación no encontrado"
        )
    
    # Validar que el token no haya sido usado
    if calificacion.token_usado:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Este token de calificación ya ha sido utilizado"
        )
    
    # Actualizar la calificación
    updated_calificacion = update_calificacion(
        db=db,
        calificacion=calificacion,
        puntuacion=calificacion_data.puntuacion,
        comentario=calificacion_data.comentario or ""
    )
    
    return CalificacionSubmitResponse(
        message="Calificación registrada exitosamente. ¡Gracias por su tiempo!",
        id_calificacion=updated_calificacion.id_calificacion
    )
