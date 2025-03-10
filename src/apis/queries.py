
from sqlalchemy import Case
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from db import Product, User
from users import hash_password

def get_user(db: Session, username: str):
    """
    Filter user table in DB and get user matched by username
    Args:
        db (session): session object to db, allow interact with db 
        username (str): parsed username, filed to filter against in DB 
    """
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username: str, password: str):
    """
    create user object row in User table
    Args:
        db (session): session object to db, allow interact with db 
        username (str): parsed username
        password (str): parsed password
    """
    
    hashed_password = hash_password(password)
    user_exits = get_user(db, username)
    if user_exits:
        raise HTTPException(detail="username is already assigned to anther user, try to register with different username", status_code = status.HTTP_400_BAD_REQUEST)
    db_user = User(username=username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_product(db: Session, name: str, stock_quantity: int, description: str, price: float):
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
    return product

def get_product_by_id(db: Session, id: int):
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
                else_=Product.price * 0.93,  #  if stock_quantity > 5, decease by 7%
            ).label("dynamic_price"),
            Product.stock_quantity,
            Product.description,
            Product.name
        ).filter(Product.id = id ).first()
    )
    return {
        "id": id, "name": product.name, "description": product.description, "price": round(product.dynamic_price, 2), "stock_quantity": product.stock_quantity
    } if product else None


def get_products_list(db: Session):
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
            Product.name
        )
        .all()
    )

    return [
        {
            "id": product.id,
            "name": product.name,
            "price": round(product.dynamic_price, 2),
            "stock": product.stock,
            "description": product.description,
        }
        for product in products
    ] if products else []