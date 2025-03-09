from datetime import timedelta
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.db import get_db
from users.utils import verify_password
from apis.queries import get_user, create_user
from users.auth import create_access_token, get_current_user
from apis.schemas import UserLoginOrCreate, TokenResponse


user_router = APIRouter()

@user_router.post("users/register", tags = ["users"])
async def register(user: UserLoginOrCreate, db: Session = Depends(get_db)):
    """
    register new user 
    Args:
        user (UserLoginOrCreate): data to register new user 
        db (session): session object to db, allow interact with db
    Raises:
        HTTPException: in case register include username already assigned to anther one 
    """
    db_user = get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    create_user(db, user.username, user.password)
    return {"message": "User registered successfully"}


@user_router.post("users/login",tags = ["users"], response_model = TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    login, successfully login gain access token, token not remain forever it's expire after some time
    Args:
        form_data: include data to login 
        db (session): session object allow db interactions
    """
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=15))
    return {"access_token": access_token, "token_type": "bearer"}
