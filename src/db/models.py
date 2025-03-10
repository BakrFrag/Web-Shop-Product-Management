from sqlalchemy import Column, Integer, String, Float, CheckConstraint
from db.base import Base, engine


class User(Base):
    """
    represents Table User in DB
    Constraints:
        username: unique 
    """
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Product(Base):
    """
    represents Table Product in DB 
    Constraints:
        price > 0.0
        stock >= 0
    """
    
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable= False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    __table_args__ = (
        CheckConstraint('price > 0.0', name='check_price_non_negative'),
        CheckConstraint('stock_quantity >= 0', name='check_stock_non_negative'),
    )


Base.metadata.create_all(bind=engine)
