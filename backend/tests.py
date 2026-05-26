"""
Tests for JWT authentication API
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "endpoints" in response.json()


def test_login_success():
    """Test successful login with correct credentials"""
    response = client.post(
        "/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 300


def test_login_invalid_username():
    """Test login with invalid username"""
    response = client.post(
        "/login",
        json={"username": "invalid", "password": "admin123"}
    )
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]


def test_login_invalid_password():
    """Test login with invalid password"""
    response = client.post(
        "/login",
        json={"username": "admin", "password": "wrong123"}
    )
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]


def test_refresh_token_success():
    """Test successful token refresh"""
    # First, login to get tokens
    login_response = client.post(
        "/login",
        json={"username": "admin", "password": "admin123"}
    )
    refresh_token = login_response.json()["refresh_token"]
    
    # Then, refresh the token
    response = client.post(
        "/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 300


def test_refresh_token_invalid():
    """Test refresh with invalid token"""
    response = client.post(
        "/refresh",
        json={"refresh_token": "invalid.token.here"}
    )
    assert response.status_code == 401
    assert "Invalid or expired refresh token" in response.json()["detail"]
