from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/products",
                   tags=["products"],
                   responses={404:{"message": "No encontrado"}})

# Entidad product
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: str


products_test_list = [
    Product(id=1, name="Laptop Lenovo", description="Notebook 14'' Ryzen 5, 8GB RAM, 512GB SSD", price="850.00"),
    Product(id=2, name="Mouse Logitech", description="Mouse inalámbrico ergonómico", price="25.99"),
    Product(id=3, name="Monitor Samsung", description="Monitor 24'' Full HD con tecnología IPS", price="180.49")
]

@router.get("/")
async def products():
    return products_test_list

@router.get("/{id}")
async def products(id: int):
    return products_test_list[id]
