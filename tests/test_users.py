# from .test_database import client, session  # Import the client and session fixtures
from app.schema.schema import UserResponse
from app.schema.auth_schema import AuthResponse
from app.config import settings
from jose import jwt
import pytest 
from fastapi.testclient import TestClient


# Uncomment the following test if you want to test the root endpoint
# @pytest.mark.skip(reason="Skipping root endpoint test for now")
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

def test_token_error(client: TestClient, test_user: dict):
    """Test token error handling.
    This test uses a fixture to create a session and ensures that the user receives an error when trying to access a protected endpoint without a valid token.
    """
    response = client.get("api/posts/")
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@email.com', 'testing123', 401),
    ('test@email.com', 'wrongpassword', 401),
    ('XXXXXXXXXXXXXXXXXXXX', 'wrongpassword', 401),
    (None, 'password123', 422),
    ('test@email.com', None, 422)
])
def test_invalid_credentials(client: TestClient, test_user: dict, email, password, status_code):
    """Test invalid credentials error handling.
    This test uses a fixture to create a session and ensures that the user receives an error when trying to log in with invalid credentials.
    """
    user_data = {
        "username": email,
        "password": password
    }

    response = client.post(
        "api/auth/login/",
        data=user_data
    )

    assert response.status_code == status_code
    # assert response.json() == {'detail': 'Invalid credentials'}