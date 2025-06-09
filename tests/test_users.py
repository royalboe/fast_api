import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schema.schema import UserResponse
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

@pytest.fixture(name="session")
def session_fixture():
    """Fixture to create a test database session."""
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name='client')
def override_get_session(session: Session):
    """Override the get_session dependency to use the test session."""
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
    
# Uncomment the following test if you want to test the root endpoint
@pytest.mark.skip(reason="Skipping root endpoint test for now")
def test_root_endpoint():
    """Test the root endpoint of the API."""
    app.dependency_overrides.clear()
    client = TestClient(app)
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