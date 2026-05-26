"""
Pydantic models for request and response schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TokenRequest(BaseModel):
    """Request model for login endpoint"""
    username: str
    password: str


class Token(BaseModel):
    """Response model for token endpoint"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefreshRequest(BaseModel):
    """Request model for refresh token endpoint"""
    refresh_token: str


class User(BaseModel):
    """User model"""
    username: str
    is_active: bool = True


class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None
    exp: Optional[datetime] = None
    type: str = "access"  # access or refresh


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
