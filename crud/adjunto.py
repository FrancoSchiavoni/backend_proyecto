import os
from typing import List, Optional 
from datetime import datetime

from sqlmodel import Session, select
from db.models.adjunto import Adjunto # Asegúrate de que la ruta sea correcta
from schemas.adjunto import AdjuntoCreate, AdjuntoRead

ATTACHMENT_DIR = "static/uploads"

async def get_adjunto(db: Session, adjunto_id: int) -> Optional[Adjunto]:
    """Obtiene un adjunto por su ID."""
    return  db.get(Adjunto, adjunto_id)

async def get_adjuntos_by_ticket(db: Session, ticket_id: int) -> List[Adjunto]:
    """Obtiene todos los adjuntos para un ticket específico."""
    statement = select(Adjunto).where(Adjunto.id_caso == ticket_id)
    adjuntos = ( db.exec(statement)).all()
    return adjuntos

async def create_adjunto(db: Session, filename: str, filepath: str, ticket_id: int, usuario_id: int) -> Adjunto:
    """Crea un nuevo adjunto en la base de datos."""
    db_adjunto = Adjunto(
        filename=filename,
        filepath=filepath,
        id_caso=ticket_id,
        id_usuario_autor=usuario_id,
        fecha=datetime.now()
    )
    db.add(db_adjunto)
    db.commit()
    db.refresh(db_adjunto)
    return db_adjunto

async def delete_adjunto(db: Session, adjunto_id: int) -> bool:
    """Elimina un adjunto de la base de datos y su archivo físico."""
    adjunto =  db.get(Adjunto, adjunto_id)
    if adjunto:
        # Intenta eliminar el archivo físico
        file_path_to_delete = os.path.join(ATTACHMENT_DIR, adjunto.filepath)
        if os.path.exists(file_path_to_delete):
            try:
                os.remove(file_path_to_delete)
            except OSError as e:
                print(f"Error al eliminar el archivo {file_path_to_delete}: {e}")
                # Considera si quieres que la transacción falle si el archivo no se puede eliminar
                # o simplemente loguear el error y continuar con la eliminación del registro DB.

        db.delete(adjunto)
        db.commit()
        return True
    return False


def get_attachment_path(filename: str) -> str:
    """Genera una ruta única para el archivo."""
    # Para evitar colisiones y organizar, puedes usar un UUID o una estructura de carpetas por fecha/ID
    # Por ahora, usaremos el nombre original con un timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    unique_filename = f"{timestamp}_{filename}"
    return os.path.join(ATTACHMENT_DIR, unique_filename)

def get_attachment_relative_path(filename: str) -> str:
    """Retorna la ruta relativa para guardar en la base de datos."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    unique_filename = f"{timestamp}_{filename}"
    return unique_filename # Solo el nombre del archivo con timestamp