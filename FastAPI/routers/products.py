from fastapi import APIRouter

router = APIRouter(prefix="/products", 
                    tags=["products"],
                    responses={404:{"message":"No encontrado"}})

product_list = ["Producto1","Producto2","Producto3","Producto4",]

@router.get("/")
async def products():
    return product_list

@router.get("/{id}")
async def products(id: int):
    return product_list[id]