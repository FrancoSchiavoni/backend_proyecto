from fastapi import FastAPI,Depends
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from db.client import engine
from routers import ticket, user, jwt_auth_users, cliente, adjunto, ticket_intervencion
from routers import estado, prioridad, tipo_caso, tipo_usuario
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:*",  # The origin of your Flutter web app
    "http://localhost",
    "http://localhost:8080", # A common default for other local servers
]






@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows specific origins
    allow_credentials=True, # Allows cookies to be included in requests
    allow_methods=["*"],    # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],    # Allows all headers
)

app.include_router(jwt_auth_users.router)
app.include_router(user.router)
app.include_router(cliente.router, dependencies=[Depends(jwt_auth_users.current_user)])
app.include_router(ticket.router, dependencies=[Depends(jwt_auth_users.current_user)])
app.include_router(ticket_intervencion.router, dependencies=[Depends(jwt_auth_users.current_user)])
app.include_router(adjunto.router)
app.include_router(estado.router)
app.include_router(prioridad.router)
app.include_router(tipo_caso.router)
app.include_router(tipo_usuario.router)


