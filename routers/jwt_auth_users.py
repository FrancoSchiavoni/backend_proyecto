from fastapi import FastAPI,Depends,HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta,timezone
from settings import settings


router = APIRouter(prefix="/jwt",
                   tags=["auth"],
                   responses={404:{"message": "No encontrado"}})


oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

# Entidad user
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool


class UserDB(User):
    password: str

users_db = {
    "fschiavoni":{
        "username": "fschiavoni",
        "full_name": "Franco Schiavoni",
        "email": "francoschiavoni@gmail.com",
        "disable": False,
        "password": "$2a$12$uMvjtBVpmi2QKgcPnqfc8.sN.T5XWpgc7pA6KHXRPEYjD8vO/oSE."
    },
    "fschiavoni2":{
        "username": "fschiavoni",
        "full_name": "Franco Schiavoni",
        "email": "francoschiavoni@gmail.com",
        "disable": True,
        "password": "$2a$12$tXPzOc6ku7X3wXaNRE7Uwe4XhNU8N.Za6oBX5fPFB2GbDP2c4rYzm"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Credenciales de autenticacion invalida", 
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, settings.settings.secret_key, 
            algorithms=[settings.settings.algorithm]).get("sub")
        if username is None:
            raise auth_exception
    except JWTError:
        raise auth_exception

    return search_user(username)


async def current_user( user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")

    access_token = {
        "sub":user.username,
        "exp":datetime.now(timezone.utc) + timedelta(minutes= settings.settings.access_token_duration),
    }

    return {"access_token": jwt.encode(access_token, settings.settings.secret_key, 
            algorithm=settings.settings.algorithm), 
            "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user