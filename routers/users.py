from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["users"])

# Entidad user
class User(BaseModel):
    id:int
    name: str
    surname: str
    url: str
    age: int


# Test_List
users_test_list = [User(id=1, name="Franco", surname="Schiavoni", url="https://franco.dev", age=25),
                   User(id=2, name="Patricio", surname="Schiavoni", url="https://pato.dev", age=17),
                   User(id=3, name="Benicio", surname="Schiavoni", url="https://beni.dev", age=13)]

@router.get("/users")
async def users():
    return users_test_list


# GET
## Path
@router.get("/user/{id}")
async def user(id: int):
    return(search_user(id))

# Query
@router.get("/user/")
async def user(id: int):
    return(search_user(id))

def search_user(id: int):
    user = filter(lambda user: user.id == id, users_test_list)
    try:
        return list(user)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}

#POST
@router.post("/user/", response_model=User,status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    else: 
        users_test_list.append(user)
        return user

#PUT
@router.put("/user/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_test_list):
        if saved_user.id == user.id:
            users_test_list[index] = user
            found = True
    if not found:
        return {"error": "No se ha encontrado el usuario para actualizar"}
    else:
        return user

#DELETE 
@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_test_list):
        if saved_user.id == id:
            del users_test_list[index]
            found = True
    if not found:
        return {"error": "No se ha encontrado el usuario para eliminar"}