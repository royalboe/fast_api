from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text

from .database import Base

class Post(Base):
    __tablename__ = "posts"
    id: int = Column(Integer, primary_key=True, nullable=False)
    title: str = Column(String, nullable=False)
    content: str = Column(String, nullable=False)
    published: bool = Column(Boolean, server_default="TRUE")
    rating: int = Column(Integer, nullable=True, server_default=text('0'))  # Optional rating field
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))  # Optional created_at field