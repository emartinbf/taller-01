"""
JWT utility functions for token creation and validation
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import settings
from models import TokenData

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(username: str) -> tuple[str, int]:
    """
    Create a JWT access token
    
    Args:
        username: The username for the token
        
    Returns:
        tuple: (token, expires_in_seconds)
    """
    expires_in = settings.ACCESS_TOKEN_EXPIRE_SECONDS
    expire = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    
    to_encode = {
        "username": username,
        "exp": expire,
        "type": "access"
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt, expires_in


def create_refresh_token(username: str) -> str:
    """
    Create a JWT refresh token
    
    Args:
        username: The username for the token
        
    Returns:
        str: The refresh token
    """
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode = {
        "username": username,
        "exp": expire,
        "type": "refresh"
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[TokenData]:
    """
    Verify a JWT token and extract its data
    
    Args:
        token: The token to verify
        token_type: Type of token (access or refresh)
        
    Returns:
        TokenData: The token data if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        username: str = payload.get("username")
        token_type_payload: str = payload.get("type", "access")
        
        if username is None:
            return None
            
        if token_type_payload != token_type:
            return None
            
        return TokenData(username=username, type=token_type_payload)
        
    except JWTError:
        return None


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user with username and password
    
    For this simple example, we only accept:
    username: admin
    password: admin123
    
    Args:
        username: The username
        password: The password
        
    Returns:
        bool: True if authentication is successful
    """
    # In a real application, you would verify against a database
    if username == "admin" and password == "admin123":
        return True
    return False
