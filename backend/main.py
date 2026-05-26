"""
Main FastAPI application with JWT authentication
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from config import settings
from models import TokenRequest, Token, TokenRefreshRequest, HealthResponse
from jwt_utils import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    verify_token
)

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns:
        HealthResponse: The health status
    """
    return HealthResponse(
        status="healthy",
        message="API is running"
    )


@app.post("/login", response_model=Token)
async def login(credentials: TokenRequest):
    """
    Login endpoint that returns a JWT token
    
    This endpoint accepts username and password and returns:
    - access_token: JWT token with 300 seconds expiration
    - refresh_token: JWT token for refreshing the access token
    - token_type: Type of token (bearer)
    - expires_in: Expiration time in seconds
    
    Default credentials:
    - username: admin
    - password: admin123
    
    Args:
        credentials: TokenRequest containing username and password
        
    Returns:
        Token: Response with access_token, refresh_token, and expiration time
        
    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Authenticate user
    if not authenticate_user(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create tokens
    access_token, expires_in = create_access_token(credentials.username)
    refresh_token = create_refresh_token(credentials.username)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=expires_in
    )


@app.post("/refresh", response_model=Token)
async def refresh_token(request: TokenRefreshRequest):
    """
    Refresh token endpoint that returns a new access token
    
    This endpoint accepts a refresh_token and returns a new access_token
    
    Args:
        request: TokenRefreshRequest containing the refresh_token
        
    Returns:
        Token: Response with new access_token and expiration time
        
    Raises:
        HTTPException: 401 if refresh token is invalid
    """
    # Verify refresh token
    token_data = verify_token(request.refresh_token, token_type="refresh")
    
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create new access token
    access_token, expires_in = create_access_token(token_data.username)
    
    return Token(
        access_token=access_token,
        refresh_token=request.refresh_token,  # Return the same refresh token
        token_type="bearer",
        expires_in=expires_in
    )


@app.get("/")
async def root():
    """
    Root endpoint with API information
    
    Returns:
        dict: API information
    """
    return {
        "message": "JWT Authentication API",
        "version": settings.API_VERSION,
        "endpoints": {
            "login": "/login (POST)",
            "refresh": "/refresh (POST)",
            "health": "/health (GET)",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level="info"
    )
