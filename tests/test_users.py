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


# def test_root_endpoint():
#     client = TestClient(app)
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Welcome to my API"}

def test_create_user():
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
      def get_session_override():
          return session
      app.dependency_overrides[get_session] = get_session_override
      client = TestClient(app)
      response = client.post(
          "api/users/",
          json={
              "email": "test@email.com",
              "password": "testing123",
          }
      )

      new_user = UserResponse(**response.json())
      new_user.email == "test@email.com"
      assert response.status_code == 201