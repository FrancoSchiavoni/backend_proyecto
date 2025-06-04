from fastapi import FastAPI,Depends
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from db.client import engine
from routers import users_db, jwt_auth_users

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)
