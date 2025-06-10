import pytest
from fastapi.testclient import TestClient
from app.main import app
from urllib.parse import quote_plus
from sqlmodel import Session, create_engine, SQLModel
from app.utils.dependencies import get_session
from app.config import settings

password = quote_plus(settings.db_password)
user = settings.db_user
host = settings.db_host
port = settings.db_port
db = "test_db"
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

# Conftest is a configuration file for pytest that sets up fixtures and configurations for testing.
# It is automatically recognized by pytest and can be used to share fixtures across multiple test files.
# This file is used to set up the test environment, including the database connection and test client.
# The conftest is also folder scoped

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

@pytest.fixture(name="session")
def session():
    """Fixture to create a test database session."""
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name='client')
def client(session: Session):
    """Override the get_session dependency to use the test session."""
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()