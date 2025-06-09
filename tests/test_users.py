from .test_database import client, session  # Import the client and session fixtures
from app.schema.schema import UserResponse
import pytest 
from fastapi.testclient import TestClient   



# Uncomment the following test if you want to test the root endpoint
@pytest.mark.skip(reason="Skipping root endpoint test for now")
def test_root_endpoint(client: TestClient):
    """Test the root endpoint of the API."""
    app.dependency_overrides.clear()
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