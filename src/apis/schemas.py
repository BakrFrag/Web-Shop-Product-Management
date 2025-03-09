from pydantic import BaseModel

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