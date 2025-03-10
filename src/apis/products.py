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
    product: ProductCreate, db: 
    Session = Depends(get_db), 
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
async def list_all_products(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """
    list and get all products with their price adjusted as stock_quantity
    Args:
        db (Session): db session object
        current_user: current login user
    """
    return get_products_list(db)


@product_router.get("/products/{product_id}/", tags = ["products"], response_model = ProductResponse)
async def get_product(  
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """
    get product by id, product price will be adjusted as stock quantity
    Args:
        db (session): db session object 
        product_id (int): id of project, parsed as url variable
        current_user: current login user
    Raises:
        HTTPException: if product not exits     
    """
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product