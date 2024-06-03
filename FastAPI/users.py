from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [
    User(id=1, name="Sergio", surname="Fdez", url="test", age=35),
    User(id=2, name="Alba", surname="Fdez", url="test", age=35),
    User(id=3, name="Pepe", surname="Fdez", url="test", age=35),
]


@app.get("/users")
async def users():
    return users_list


@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado al usuario."}
