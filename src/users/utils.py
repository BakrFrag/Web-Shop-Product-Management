from sqlalchemy.orm import Session
from db.models import User
from passlib.context import CryptContext

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
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
