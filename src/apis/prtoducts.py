from fastapi import Depends, HTTPException, APIRouter, status
from db.db import get_db
from apis.queries import create_product, get_product_by_id, get_all_products
from apis.schemas import ProductCreate, ProductResponse


product_router = APIRouter()
