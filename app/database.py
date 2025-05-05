from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

SQLALCHEMY_DATABASE_URL = f"postgresql://"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=
                       {
                         "host": os.getenv("DB_HOST"),
                         "port": os.getenv("DB_PORT"),
                         "user": os.getenv("DB_USER"),
                         "password": os.getenv("DB_PASSWORD"),
                         "database": os.getenv("DB_NAME"),
                         }
                         )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()