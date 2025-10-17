
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Response
from fastapi.responses import FileResponse
from sqlmodel import Session
from db.client import get_session
from schemas.user import UsuarioCreate, UsuarioRead
from crud.user import get_usuario, get_usuarios, create_usuario, delete_usuario, get_usuario_email
from typing import List, Optional
import os
import shutil

router = APIRouter(prefix="/usuarios", tags=["usuarios"])
PROFILE_PHOTOS_DIR = os.path.join("static", "profile_photos")

def get_profile_photo_path(user_id: int, filename: str) -> str:
    ext = os.path.splitext(filename)[1]
    return os.path.join(PROFILE_PHOTOS_DIR, f"user_{user_id}{ext}")

@router.get("/", response_model=List[UsuarioRead])
async def listar_usuarios(skip: int = 0, limit: int = 100, id_tipo: Optional[int] = None ,db: Session = Depends(get_session)):
    return await get_usuarios(db, skip, limit, id_tipo=id_tipo)

@router.get("/{usuario_id}", response_model=UsuarioRead)
async def leer_usuario(usuario_id: int, db: Session = Depends(get_session)):
    usuario = get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/", response_model=UsuarioRead)
async def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_session)):
    db_usuario_existente_email = await get_usuario_email(db, email=usuario.email)
    if db_usuario_existente_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya está registrado")
    return await create_usuario(db, usuario)


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(usuario_id: int, db: Session = Depends(get_session)):
    usuario_to_delete = get_usuario(db, usuario_id)
    if not usuario_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    success = await delete_usuario(db, usuario_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar el usuario")
    return True

@router.get("/{usuario_id}/profile_photo")
async def get_profile_photo(usuario_id: int, db: Session = Depends(get_session)):
    usuario = get_usuario(db, usuario_id)
    if not usuario or not usuario.profile_photo_url:
        raise HTTPException(status_code=404, detail="Foto de perfil no encontrada")
    if not os.path.exists(usuario.profile_photo_url):
        raise HTTPException(status_code=404, detail="Archivo de foto no encontrado")
    return FileResponse(usuario.profile_photo_url)

@router.post("/{usuario_id}/profile_photo", response_model=UsuarioRead)
async def upload_profile_photo(usuario_id: int, file: UploadFile = File(...), db: Session = Depends(get_session)):
    usuario = get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Eliminar foto anterior si existe
    if usuario.profile_photo_url:
        try:
            os.remove(usuario.profile_photo_url)
        except Exception:
            pass
    # Guardar nueva foto
    os.makedirs(PROFILE_PHOTOS_DIR, exist_ok=True)
    file_path = get_profile_photo_path(usuario_id, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    usuario.profile_photo_url = file_path.replace("\\", "/")
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/{usuario_id}/profile_photo", response_model=UsuarioRead)
async def delete_profile_photo(usuario_id: int, db: Session = Depends(get_session)):
    usuario = get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.profile_photo_url:
        try:
            os.remove(usuario.profile_photo_url)
        except Exception:
            pass
        usuario.profile_photo_url = None
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
    return usuario