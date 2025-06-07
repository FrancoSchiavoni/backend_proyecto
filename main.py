from fastapi import FastAPI,Depends
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from db.client import engine
from db.models.user import Usuario
from db.models.ticket import Ticket
from db.models.cliente import Cliente
from routers import ticket, user, jwt_auth_users, cliente, adjunto


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(jwt_auth_users.router)
app.include_router(user.router)
app.include_router(adjunto.router)
app.include_router(ticket.router, dependencies=[Depends(jwt_auth_users.current_user)])
app.include_router(cliente.router, dependencies=[Depends(jwt_auth_users.current_user)])
app.include_router(ticket_intervencion.router, dependencies=[Depends(jwt_auth_users.current_user)])
