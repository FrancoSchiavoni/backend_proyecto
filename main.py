from fastapi import FastAPI, Depends
from routers import products,users,jwt_auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router, dependencies=[Depends(jwt_auth_users.current_user)])
app.include_router(users.router)
app.include_router(jwt_auth_users.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
