from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


router = APIRouter(prefix="/basicauth",
                tags=["basicauth"],
                responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


# Entidad user
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
        "password": "1234"
    },
    "pepe": {
        "username": "pepe",
        "full_name": "pepe fdez",
        "email": "pepefdez@gmail.com",
        "disabled": True,
        "password": "4321"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def created_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user_db(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autentificación inválidas", 
            headers={"WWW-Authenticate":"Bearer"}
        )
    
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
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user