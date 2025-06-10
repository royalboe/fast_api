from .test_database import client, session  # Import the client and session fixtures
from app.schema.schema import UserResponse
from app.schema.auth_schema import AuthResponse
from app.config import settings
from jose import jwt
import pytest 
from fastapi.testclient import TestClient


@pytest.fixture()
def test_user(client: TestClient):
    """Fixture to create a test user in the database."""
    user_data = {
        "email": "test@email.com",
        "password": "Testing123",
        "username": "testuser"
    }

    res = client.post(
        "api/users/",
        json=user_data
    )

    assert res.status_code == 201
    new_user = res.json()
    print(new_user)
    # assert new_user["email"] == user_data['email']
    
    new_user["password"] = user_data['password'] 
    print(new_user) # Ensure password is set for login
    return new_user


# Uncomment the following test if you want to test the root endpoint
@pytest.mark.skip(reason="Skipping root endpoint test for now")
def test_root_endpoint(client: TestClient):
    """Test the root endpoint of the API."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to my API"}

def test_create_user(client: TestClient):
    """Test creating a new user in the database.
    This test uses a fixture to create a session and ensures that the user is created successfully.
    """
    response = client.post(
        "api/users/",
        json={
            "email": "test4@email.com",
            "password": "testing123",
        }
    )

    new_user = UserResponse(**response.json())
    new_user.email == "test4@email.com"
    assert response.status_code == 201
  

def test_get_user(client: TestClient, test_user: dict):
    """Test retrieving a user by ID.
    This test uses a fixture to create a session and ensures that the user is retrieved successfully.
    """
    response = client.get("api/users/1/")
    assert response.status_code == 200
    user = UserResponse(**response.json())
    assert user.id == 1

def test_user_login(client: TestClient, test_user: dict):
    """Test user login functionality.
    This test uses a fixture to create a session and ensures that the user can log in successfully.
    """
    user_data = {
        "username": test_user['email'],
        "password": test_user['password']
    }

    response = client.post(
        "api/auth/login/",
        data=user_data
    )

    login_res = AuthResponse(**response.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert response.status_code == 200
    assert "access_token" in response.json()

