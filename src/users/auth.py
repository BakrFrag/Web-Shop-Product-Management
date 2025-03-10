import logging
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db import get_db, User
from core import get_secret_key
from users.utils import hash_password

ALGORITHM = get_secret_key("ALGORITHM")
SECRET_KEY = get_secret_key("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

    hashed_password = hash_password(password)
    user_exits = get_user(db, username)
    if user_exits:
        logger.error(f"query to create user with username {username}, username already assigned to anther user")
        raise HTTPException(detail="username is already assigned to anther user, try to register with different username", status_code = status.HTTP_400_BAD_REQUEST)
    db_user = User(username=username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"create new user with unique username {username}")
    return db_user


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    generate access token
    Args:
        data: parsed data 
        expires_delta: when token expires
    """
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    logger.info(f"create new user with data {data}")
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    get current login user
    Args:
        db (Session): db session object
        token (str): parsed token
    Raises:
        HTTPException: trigger if parsed token is invalid, or user not exists 
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.error(f"username not exists")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = get_user(db, username)
        if user is None:
            logger.error(f"user not exists")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        logger.info(f"user exists, and can process requests")
        return user
    except JWTError as exc:
        logger.error(f"parsed token is invalid")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

