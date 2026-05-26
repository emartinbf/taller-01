"""
Configuration settings for the FastAPI JWT application
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 300  # 5 minutes
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # API Configuration
    API_TITLE: str = "JWT Authentication API"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "FastAPI application with JWT authentication"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
