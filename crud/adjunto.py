# crud/adjunto.py

import os
from typing import List, Optional 
from datetime import datetime

from sqlmodel import Session, select
from db.models.adjunto import Adjunto

ATTACHMENT_DIR = "static/uploads"

async def get_adjunto(db: Session, adjunto_id: int) -> Optional[Adjunto]:
    """Obtiene un adjunto por su ID."""
    return db.get(Adjunto, adjunto_id)

async def get_adjuntos_by_ticket(db: Session, ticket_id: int) -> List[Adjunto]:
    """Obtiene todos los adjuntos para un ticket específico."""
    statement = select(Adjunto).where(Adjunto.id_caso == ticket_id)
    adjuntos = db.exec(statement).all()
    return adjuntos

async def create_adjunto(
    db: Session, 
    filename: str, 
    filepath: str, 
    usuario_id: int,
    ticket_id: int,
    intervencion_id: Optional[int] = None
) -> Adjunto:
    """Crea un nuevo adjunto en la base de datos."""
    db_adjunto = Adjunto(
        filename=filename,
        filepath=filepath,
        id_caso=ticket_id,
        id_intervencion=intervencion_id,
        id_usuario_autor=usuario_id
    )
    db.add(db_adjunto)
    db.commit()
    db.refresh(db_adjunto)
    return db_adjunto

async def delete_adjunto(db: Session, adjunto_id: int) -> bool:
    """Elimina un adjunto de la base de datos y su archivo físico."""
    adjunto = db.get(Adjunto, adjunto_id)
    if adjunto:
        file_path_to_delete = os.path.join(ATTACHMENT_DIR, adjunto.filepath)
        if os.path.exists(file_path_to_delete):
            try:
                os.remove(file_path_to_delete)
            except OSError as e:
                print(f"Error al eliminar el archivo {file_path_to_delete}: {e}")

        db.delete(adjunto)
        db.commit()
        return True
    return False