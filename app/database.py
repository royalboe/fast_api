from urllib.parse import quote_plus
from sqlmodel import Session, create_engine, SQLModel
from .config import settings

password = quote_plus(settings.db_password)
user = settings.db_user
host = settings.db_host
port = settings.db_port
db = settings.db_name
# DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def  create_db_and_tables():
    SQLModel.metadata.create_all(engine)