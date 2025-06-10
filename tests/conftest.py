import pytest
from fastapi.testclient import TestClient
from app.main import app
from urllib.parse import quote_plus
from sqlmodel import Session, create_engine, SQLModel
from app.utils.dependencies import get_session
from app.config import settings
from app.utils.oauth2 import create_access_token
from app.models.post import Post as PostModel
from sqlmodel import select

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

@pytest.fixture(name="test_user")
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
    # assert new_user["email"] == user_data['email']
    
    new_user["password"] = user_data['password'] 
    return new_user

@pytest.fixture(name="test_user2")
def test_user2(client: TestClient):
    """Fixture to create another test user in the database."""
    user_data = {
        "email": "test2@email.com",
        "password": "Testing12345",
        "username": "Test user 2"
    }

    res = client.post(
        "api/users/",
        json=user_data
    )

    assert res.status_code == 201
    new_user = res.json()
    # assert new_user["email"] == user_data['email']

    new_user["password"] = user_data['password']
    return new_user

@pytest.fixture(name="session")
def test_session():
    """Fixture to create a test database session."""
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name='client')
def test_client(session: Session):
    """Override the get_session dependency to use the test session."""
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="authorized_client")
def authorized_client(client: TestClient, token):
    """Fixture to create an authorized client for testing."""
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture(name="token")
def token(test_user):
    """Fixture to generate an access token for testing."""
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture(name="test_posts")
def test_posts(session: Session, test_user: dict, test_user2: dict):
    """Fixture to create test posts in the database."""
    posts_data: list = [
        {
            "title": "Test Post One",
            "content": "This is a test post 1.",
            "author_id": test_user['id']   
        },
        {
            "title": "Test Post",
            "content": "This is a test post.",
            "author_id": test_user['id']
        },
        {
            "title": "Test Post Two",
            "content": "This is a test post 2.",
            "author_id": test_user2['id']
        },
        {
            "title": "Test Post Three",
            "content": "This is a test post 3.",
            "author_id": test_user2['id']
            }
        ]
    
    post_models =  [PostModel(**post) for post in posts_data]
    
    session.add_all(post_models)
    session.commit()
    for post in post_models:
        session.refresh(post)

    posts = session.exec(select(PostModel).order_by(PostModel.id.desc())).all()
    return posts
