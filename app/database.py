from urllib.parse import quote_plus
import os
from sqlmodel import Session, create_engine

password = quote_plus(os.getenv("DB_PASSWORD"))
user = os.getenv("DB_USER")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

