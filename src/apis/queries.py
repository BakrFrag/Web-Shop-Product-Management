
import logging
from sqlalchemy import Case
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from db import Product, User
from users import hash_password


logger = logging.getLogger("web_shop")

async def get_user(db: Session, username: str):
    """
    Filter user table in DB and get user matched by username
    Args:
        db (session): session object to db, allow interact with db 
        username (str): parsed username, filed to filter against in DB 
    """
    logger.debug(f"query to get user with filter as username as {username}")
    return db.query(User).filter(User.username == username).first()


async def create_user(db: Session, username: str, password: str):
    """
    create user object row in User table
    Args:
        db (session): session object to db, allow interact with db 
        username (str): parsed username
        password (str): parsed password
    """

    hashed_password = await hash_password(password)
    user_exits = await get_user(db, username)
    if user_exits:
        logger.error(f"query to create user with username {username}, username already assigned to anther user")
        raise HTTPException(detail="username is already assigned to anther user, try to register with different username", status_code = status.HTTP_400_BAD_REQUEST)
    db_user = User(username=username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"create new user with unique username {username}")
    return db_user


async def create_product(db: Session, name: str, description: str, price: float, stock_quantity: int):
    """
    create product row 
    Args:
        db (session): session object to db, allow interact with db 
        name (str): product name
        stock_quantity (int): number of product in stock 
        price (float): product price 
        description (str): description of product
    """
    product = Product(name = name, price = price, description = description, stock_quantity = stock_quantity)
    db.add(product)
    db.commit()
    db.refresh(product)
    logger.info(f"create new product with as {name} like {description}")
    return product

async def get_product_by_id(db: Session, id: int):
    """
    get product by id
    adjust price of product as
    if stock_quantity = 0, return original price 
    if stock_quantity > 0 and stock_quantity <=5, increase price by 5 %
    if stock_quantity > 5 decease price by 7%
    
    Args:
        db(Session): session object to interact with db 
        id (int): product id
    """
    product = (
        db.query(
            Product.id,
            Case(
                (Product.stock_quantity == 0, Product.price),  # If stock is 0, return original price
                (Product.stock_quantity <= 5, Product.price * 1.05),  # If stock <= 5, increase by 5%
                else_=Product.price * 0.93,  #  if stock_quantity > 5, decrease by 7%
            ).label("dynamic_price"),
            Product.stock_quantity,
            Product.description,
            Product.name,
            Product.price
        ).filter(Product.id == id ).first()
    )
    if product:
        logger.info(f"get product by id {id}, with price as {product.price} and dynamic price as per stock quantity as {round(product.dynamic_price, 2)}")
        return {
            "id": id, "name": product.name, "description": product.description, "price": round(product.dynamic_price, 2), "stock_quantity": product.stock_quantity
        } 
    logger.debug(f"no product with related id {id}, not found")
    raise HTTPException(detail="product not exits", status_code = status.HTTP_404_NOT_FOUND)


async def get_products_list(db: Session):
    """
    get all products with price adjust as 
    if stock_quantity = 0, return original price 
    if stock_quantity > 0 and stock_quantity <=5, increase price by 5 %
    if stock_quantity > 5 , decease price by 7%
    """
    products = (
        db.query(
            Product.id,
            Case(
                (Product.stock_quantity == 0, Product.price),  # If stock is 0, return original price
                (Product.stock_quantity <= 5, Product.price * 1.05),  # If stock <= 5, increase by 5%
                else_=Product.price * 0.93,  #  if stock_quantity > 5, decease by 7%
            ).label("dynamic_price"),
            Product.stock_quantity,
            Product.description,
            Product.name,
            Product.price
        )
        .all()
    )
    logger.info("query to get list of all products with their dynamic prices as per their stock quantity")
    return [
        {
            "id": product.id,
            "name": product.name,
            "price": round(product.dynamic_price, 2),
            "stock_quantity": product.stock_quantity,
            "description": product.description,
        }
        for product in products
    ] if products else []
    
    
async def update_product(db: Session, product_id: int, product_update_data: dict):
    """
    update product by id 
    Args:
        db (Session): db object 
        product_id (int): the id of product 
        product_update_data (dict): update product data
    Raises:
        HTTPException: trigger if product not exists
    """
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        logger.error(f"update product that not exists, no product with id {product_id}")
        raise HTTPException(detail="product not exists", status_code = status.HTTP_404_NOT_FOUND)
    for key,value in product_update_data.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product