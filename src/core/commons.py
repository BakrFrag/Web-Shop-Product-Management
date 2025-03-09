import os
from dotenv import load_dotenv

load_dotenv()

def get_secret_key(key_name: str) -> str:
    """
    import secret variable values 
    Args:
        key_name (str): key name
    """
    return os.getenv(key_name)

def adjust_price(price: float, stock_quantity: int):
    """
    adjust product price as per stock quantity
    if stock_quantity < 10: price increase by 7%
    else: price decrease by 5%
    
    Args:
        price (float): represents product price 
        stock_quantity: represents stock quantity of product 
    """
    return (price + (price * 0.07)) if stock_quantity < 10 else (price - (price * 0.07))
    