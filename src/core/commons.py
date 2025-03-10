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
    