# routers/adjunto.py

import os
import shutil
from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlmodel import Session

from db.client import get_session 
from schemas.adjunto import AdjuntoRead
from crud import adjunto as crud_adjunto

from db.models.ticket import Ticket
from db.models.ticket_intervencion import TicketIntervencion
from db.models.user import Usuario 
from routers.jwt_auth_users import current_user

router = APIRouter(prefix="/adjuntos", tags=["adjuntos"])

UPLOAD_DIRECTORY = crud_adjunto.ATTACHMENT_DIR
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/ticket/{ticket_id}", response_model=AdjuntoRead, status_code=status.HTTP_201_CREATED)
async def upload_adjunto_a_ticket(
    ticket_id: int,
    file: UploadFile = File(...),
    current_user_obj: Usuario = Depends(current_user),
    db: Session = Depends(get_session)
):
    """Sube un adjunto y lo asocia directamente a un ticket."""
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    date_str = datetime.now().strftime("%Y%m%d")
    new_filename = f"{date_str}_ticket{ticket_id}_{file.filename}"

    relative_path_dir = f"ticket_{ticket_id}"
    relative_filepath = os.path.join(relative_path_dir, new_filename)
    
    full_dir_path = os.path.join(UPLOAD_DIRECTORY, relative_path_dir)
    os.makedirs(full_dir_path, exist_ok=True)

    full_file_path = os.path.join(full_dir_path, new_filename)
    try:
        with open(full_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {e}")

    db_adjunto = await crud_adjunto.create_adjunto(
        db=db,
        filename=file.filename,
        filepath=relative_filepath,
        ticket_id=ticket_id,
        intervencion_id=None,
        usuario_id=current_user_obj.id_personal
    )
    return db_adjunto

@router.post("/intervencion/{intervencion_id}", response_model=AdjuntoRead, status_code=status.HTTP_201_CREATED)
async def upload_adjunto_a_intervencion(
    intervencion_id: int,
    file: UploadFile = File(...),
    current_user_obj: Usuario = Depends(current_user),
    db: Session = Depends(get_session)
):
    """Sube un adjunto y lo asocia a una intervención específica."""
    intervencion = db.get(TicketIntervencion, intervencion_id)
    if not intervencion:
        raise HTTPException(status_code=404, detail="Intervención no encontrada")

    date_str = datetime.now().strftime("%Y%m%d")
    new_filename = f"{date_str}_ticket{intervencion.id_caso}_intervencion{intervencion_id}_{file.filename}"
    
    relative_path_dir = os.path.join(f"ticket_{intervencion.id_caso}", f"intervencion_{intervencion_id}")
    relative_filepath = os.path.join(relative_path_dir, new_filename)

    full_dir_path = os.path.join(UPLOAD_DIRECTORY, relative_path_dir)
    os.makedirs(full_dir_path, exist_ok=True)

    full_file_path = os.path.join(full_dir_path, new_filename)
    try:
        with open(full_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {e}")

    db_adjunto = await crud_adjunto.create_adjunto(
        db=db,
        filename=file.filename,
        filepath=relative_filepath,
        ticket_id=intervencion.id_caso,
        intervencion_id=intervencion_id,
        usuario_id=current_user_obj.id_personal
    )
    return db_adjunto

@router.get("/{adjunto_id}", response_class=FileResponse)
async def download_adjunto(adjunto_id: int, db: Session = Depends(get_session)):
    """Descarga un adjunto específico."""
    adjunto = await crud_adjunto.get_adjunto(db, adjunto_id)
    if not adjunto:
        raise HTTPException(status_code=404, detail="Adjunto no encontrado")

    file_path = os.path.join(UPLOAD_DIRECTORY, adjunto.filepath)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo físico no encontrado en el servidor")

    # Al descargar, se usa el nombre de archivo original guardado en la DB
    return FileResponse(path=file_path, filename=adjunto.filename, media_type="application/octet-stream")

@router.get("/ticket/{ticket_id}", response_model=List[AdjuntoRead])
async def get_adjuntos_del_ticket(ticket_id: int, db: Session = Depends(get_session)):
    """Obtiene la lista de todos los adjuntos para un ticket."""
    adjuntos = await crud_adjunto.get_adjuntos_by_ticket(db, ticket_id)
    return adjuntos

@router.delete("/{adjunto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_adjunto_endpoint(adjunto_id: int, db: Session = Depends(get_session)):
    """Elimina un adjunto por su ID."""
    success = await crud_adjunto.delete_adjunto(db, adjunto_id)
    if not success:
        raise HTTPException(status_code=404, detail="Adjunto no encontrado")
    return {"ok": True}