import os
import shutil
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlmodel import Session

from db.client import get_session 
from schemas.adjunto import AdjuntoRead
from crud import adjunto as crud_adjunto

from db.models.ticket import Ticket
from db.models.user import Usuario 
from routers.jwt_auth_users import current_user

router = APIRouter(prefix="/adjuntos", tags=["adjuntos"])

UPLOAD_DIRECTORY = crud_adjunto.ATTACHMENT_DIR

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/{ticket_id}", response_model=AdjuntoRead)
async def upload_adjunto(
    ticket_id: int,
    current_user_id: Usuario = Depends(current_user),
    file: UploadFile = File(...),
    db: Session = Depends(get_session)
):
    # 1. Verificar que el ticket_id existe
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    usuario_autor_id = current_user_id.id_personal

    relative_filepath = crud_adjunto.get_attachment_relative_path(file.filename)
    file_location = os.path.join(UPLOAD_DIRECTORY, relative_filepath)

    # Guardar el archivo en el sistema de archivos
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {e}")

    # Crear el registro en la base de datos
    db_adjunto = await crud_adjunto.create_adjunto(
        db=db,
        filename=file.filename, 
        filepath=relative_filepath, 
        ticket_id=ticket_id,
        usuario_id=usuario_autor_id
    )

    return db_adjunto

@router.get("/{adjunto_id}", response_class=FileResponse)
async def download_adjunto(adjunto_id: int, db: Session = Depends(get_session)):
    """Descarga un adjunto específico."""
    adjunto = await crud_adjunto.get_adjunto(db, adjunto_id)
    if not adjunto:
        raise HTTPException(status_code=404, detail="Adjunto no encontrado")

    # Reconstruye la ruta completa del archivo
    file_path = os.path.join(UPLOAD_DIRECTORY, adjunto.filepath)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo físico no encontrado")

    return FileResponse(path=file_path, filename=adjunto.filename, media_type="application/octet-stream")

@router.get("/ticket/{ticket_id}", response_model=List[AdjuntoRead])
async def get_adjuntos_ticket(ticket_id: int, db: Session = Depends(get_session)):
    """Obtiene la lista de adjuntos para un ticket dado."""
    adjuntos = await crud_adjunto.get_adjuntos_by_ticket(db, ticket_id)
    if not adjuntos:
        raise HTTPException(status_code=404, detail="No se encontraron adjuntos para este ticket")
    return adjuntos

@router.delete("/{adjunto_id}", response_model=bool)
async def delete_adjunto(adjunto_id: int, db: Session = Depends(get_session)):
    """Elimina un adjunto por su ID."""
    success = await crud_adjunto.delete_adjunto(db, adjunto_id)
    if not success:
        raise HTTPException(status_code=404, detail="Adjunto no encontrado o no se pudo eliminar")
    return success