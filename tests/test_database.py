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