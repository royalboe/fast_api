from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, DateTime, text
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from .votes import Vote

if TYPE_CHECKING:
  from app.models.post import Post

class UserBase(SQLModel):
  email: EmailStr = Field(nullable=False, index=True, unique=True)
  username: Optional[str] = Field(default=None, nullable=True)
  
class User(UserBase, table=True):
  __tablename__ = "users"
  id: Optional[int] = Field(default=None, primary_key=True, index=True)
  hashed_password: str = Field(nullable=False)
  updated_at: Optional[datetime] = Field(
    default=datetime.now().isoformat(),
    sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )
  created_at: Optional[datetime] = Field(
    default_factory=datetime.now, 
    sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )
  posts: list["Post"] = Relationship(back_populates="author", cascade_delete=True)
  votes: list["Vote"] = Relationship(back_populates="user", cascade_delete=True)
  
