from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, Boolean, Float, DateTime, text
from sqlmodel import Field, SQLModel, Relationship
from .votes import Vote

if TYPE_CHECKING:
  from app.models.user import User

class PostBase(SQLModel):
  title: str = Field(nullable=False, index=True, unique=True, min_length=5, max_length=100)
  content: str  = Field(nullable=False, min_length=5, max_length=5000)
  published: bool | None = Field(
    default=True,
    sa_column=Column(Boolean, server_default=text("true"))
  )   
  rating: float | None = Field(
    default=0,
    sa_column=Column(Float, server_default=text("0.0"))
  )
class Post(PostBase, table=True):
  __tablename__ = "posts"
  id: int | None = Field(default=None, primary_key=True, index=True)
  created_at: datetime | None = Field(
    default_factory=datetime.now, 
    sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )

  updated_at: datetime | None = Field(
    default=datetime.now().isoformat(),
    sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )

  author_id: int | None = Field(default=None, foreign_key="users.id", ondelete="CASCADE")
  author: Optional["User"] = Relationship(back_populates="posts")

  votes: list['Vote'] = Relationship(back_populates="post", cascade_delete=True)
