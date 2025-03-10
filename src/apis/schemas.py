from pydantic import BaseModel, Field
from typing import Optional
class User(BaseModel):
    """
    Base user model include mandatory fields
    Args:
        username: str 
            username field in table user 
    """
    username: str
    
class UserLoginOrCreate(User):
    """
    simple schema model to login or create user
    Args:
        password: str 
            password field in table user
    """
    password: str 
    
class TokenResponse(BaseModel):
    """
    Token Response model, include access token after login 
    Args:
        access_token: str 
            access token back to user
    """
    access_token: str
    

class ProductCreate(BaseModel):
    """
    Product model 
    Fields:
        price: float
            include price of product must be > 0.0
        stock_quantity: int
            number in stock, must be >= 0 
        description: optional[str]
            description for product
    """
    name: str
    price: float = Field(..., ge=0.0, description="Price must be a positive number")
    stock_quantity: int = Field(..., ge=0, description="Stock count must be non-negative") 
    description: Optional[str] = Field(None, max_length=255, description="Optional description of the product")
  

# Product response model including all attributes
class ProductResponse(ProductCreate):
    """
    product create response
    Fields:
        int: unique identifier for product
    """
    id: int
