from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


# Iniciar el server: uvicorn main:app --reload
# Detener el server: CTRL+C

# Documentación con Swagger: http://127.0.0.1:8000/docs/
# Documentación con Redocly: http://127.0.0.1:8000/redoc/
