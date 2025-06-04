from fastapi import Depends,HTTPException, status, APIRouter,Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta,timezone
from settings import settings
from sqlmodel import Session
from db.client import get_session
from schemas.user import UsuarioRead
from crud.user import get_usuario_email

router = APIRouter(prefix="/jwt",
                   tags=["auth"],
                   responses={404:{"message": "No encontrado"}})


oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

async def auth_user(db: Session = Depends(get_session), token: str = Depends(oauth2)):
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Credenciales de autenticacion invalida", 
        headers={"WWW-Authenticate": "Bearer"})

    try:
        email = jwt.decode(token, settings.settings.secret_key, 
            algorithms=[settings.settings.algorithm]).get("sub")
        if email is None:
            raise auth_exception
    except JWTError:
        raise auth_exception

    return await get_usuario_email(db, email)


async def current_user(user: UsuarioRead = Depends(auth_user)):
    return user

@router.post("/login")
async def login(response: Response, db: Session = Depends(get_session), form: OAuth2PasswordRequestForm = Depends()):
    user = await get_usuario_email(db, form.username)
    if not user:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")

    now = datetime.now(timezone.utc)
    access_token_payload = {
        "sub": user.email,
        "exp": now + timedelta(minutes=settings.settings.access_token_duration)
    }
    refresh_token_payload = {
        "sub": user.email,
        "exp": now + timedelta(days=1)
    }

    access_token = jwt.encode(access_token_payload, settings.settings.secret_key, algorithm=settings.settings.algorithm)
    refresh_token = jwt.encode(refresh_token_payload, settings.settings.secret_key, algorithm=settings.settings.algorithm)

    # Set cookie segura
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7*24*60*60,
        path="/jwt/refresh"
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh")
async def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="No hay token de refresh")

    try:
        payload = jwt.decode(refresh_token, settings.settings.secret_key, algorithms=[settings.settings.algorithm])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    new_access_token = jwt.encode({
        "sub": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.settings.access_token_duration)
    }, settings.settings.secret_key, algorithm=settings.settings.algorithm)

    return {"access_token": new_access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UsuarioRead)
async def me(user: UsuarioRead = Depends(current_user)):
    return user