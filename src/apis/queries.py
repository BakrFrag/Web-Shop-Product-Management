
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from db.models import Product, User
from users.utils import hash_password

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
    Args:
        db (Session): session db object
        id (int): id of product 
    """
    return db.query(User).filter(Product.id == id).first()

def get_all_products(db: Session):
    """
    get list of all products
    Args:
        db(Session): db session object  
    """
    return db.query(Product).all()
    