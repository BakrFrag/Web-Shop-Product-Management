from passlib.context import CryptContext
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    hash plain text password to hashed password
    Args:
        password (str): parsed plain text password
    Returns:
        str: hashed password
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str ) -> bool:
    """
    verify parsed password match hashed password stored in DB 
    Args:
        plain_password (str): parsed plain password 
        hashed_password (str): hashed password stored in DB 
    Returns:
        bool: wether parsed password matched or not
    """
    return pwd_context.verify(plain_password, hashed_password)


