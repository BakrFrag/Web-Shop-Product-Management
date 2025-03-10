from typing import List
from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from db import get_db
from apis.queries import create_product, get_product_by_id, get_products_list
from apis.schemas import ProductCreate, ProductResponse
from users import get_current_user

product_router = APIRouter()


@product_router.post("/products/", tags = ["products"], response_model = ProductResponse)
async def create_new_product(
    product: ProductCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """
    create new product
    Args:
        product (ProductCreate): data to create and add new product
        db (Session): db session object
        current_user: current authenticated user
    """
    return create_product(db, product)


@product_router.get("/products/", tags = ["products"], response_model = List[ProductResponse])
@product_router.get("/products/{product_id}/", tags = ["products"], response_model = ProductResponse)
async def list_all_products(
    product_id: int,
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """
    list or get specific product with their prices adjusted as per stock quantity
    Args:
        product_id (int): specific product id
        db (Session): db session object
        current_user: current login user
    """
     
    return get_product_by_id(db, product_id) if product_id else get_products_list(db)

