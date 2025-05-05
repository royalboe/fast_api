from urllib.parse import quote_plus
import os
from sqlmodel import Session, create_engine, SQLModel

password = quote_plus(os.getenv("DB_PASSWORD"))
user = os.getenv("DB_USER")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def  create_db_and_tables():
    SQLModel.metadata.create_all(engine)

