from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, DateTime, text
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from .votes import Vote

if TYPE_CHECKING:
  from app.models.post import Post

class UserBase(SQLModel):
  email: EmailStr = Field(nullable=False, index=True, unique=True)
  username: str | None = Field(default=None, nullable=True)
  
class User(UserBase, table=True):
  __tablename__ = "users"
  id: int | None = Field(default=None, primary_key=True, index=True)
  hashed_password: str = Field(nullable=False)
  phone_number: str | None = Field(default=None, nullable=True)
  updated_at: datetime | None = Field(
    default=datetime.now().isoformat(),
    sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )
  created_at: datetime | None = Field(
    default_factory=datetime.now, 
    sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )
  posts: list["Post"] = Relationship(back_populates="author", cascade_delete=True)
  votes: list["Vote"] = Relationship(back_populates="user", cascade_delete=True)
  
