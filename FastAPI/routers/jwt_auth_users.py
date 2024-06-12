from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 # 1 min
SECRET = "30645de76d3388ca"

router = APIRouter(prefix="/jwtauth",
                tags=["jwtauth"],
                responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

ctx = CryptContext(schemes=["bcrypt"])
# https://bcrypt-generator.com/


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "sergio": {
        "username": "sergio",
        "full_name": "sergio fdez",
        "email": "sergiofdez@gmail.com",
        "disabled": False,
        "password": "$2a$12$EUZp5N9vRfN8qfs0ir3op.nUbZ.SW3Vh2t/3zV6pow8O.75iKAwiK"
    },
    "pepe": {
        "username": "pepe",
        "full_name": "pepe fdez",
        "email": "pepefdez@gmail.com",
        "disabled": True,
        "password": "$2a$12$cucrV70zojw7OfQZjwuqEeCs6Hcauo6yinVY6YEfH1oK4TeVqY/1i"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])



async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Credenciales de autentificación inválidas", 
            headers={"WWW-Authenticate":"Bearer"}
        )

    try:
        username = jwt.decode(token,SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception
    
    return search_user(username)
    

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario Inactivo", 
        )
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)

    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not ctx.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token = {"sub":user.username, 
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user