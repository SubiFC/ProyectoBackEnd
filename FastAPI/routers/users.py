from typing import Union

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["user"],
                    responses={404:{"message":"No encontrado"}})


# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [
    User(id=1, name="Sergio", surname="Fdez", url="test", age=35),
    User(id=2, name="Alba", surname="asdf", url="test", age=22),
    User(id=3, name="Pepe", surname="lola", url="test", age=15),
]


@router.get("/users")
async def users():
    return users_list


@router.get("/user/{id}") # Path
async def user(id: int):
    return search_user(id)

@router.get("/user/") # Query
async def user(id: int):
    return search_user(id)


@router.post("/user/", status_code=201) # Add user
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="El usuario ya existe")
        
    
    users_list.append(user)
    return ("Usuario añadido correctamente",user)
        


@router.put("/user/") # Update user
async def update_user(user: User):
    found = False

    for index,saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "No se ha encontrado al usuario"}
    
    return ("Usuario actualizado correctamente", user)
            

@router.delete("/user/{id}") # Delete user
async def delete_user(id: int):
    found = False

    for index,saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error": "No se ha encontrado al usuario"}
    
    return ("Usuario eliminado correctamente")


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado al usuario"}
