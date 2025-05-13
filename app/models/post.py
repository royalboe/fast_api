from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, Boolean, Float, DateTime, text
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
  from app.models.user import User


class Post(SQLModel, table=True):
  id: Optional[int] = Field(primary_key=True, index=True)
  title: str = Field(nullable=False, index=True)
  content: str  = Field(nullable=False)
  published: Optional[bool] = Field(
    default=True,
    sa_column=Column(Boolean, server_default=text("true"))
  )   
  rating: Optional[float] = Field(
    default=0,
    sa_column=Column(Float, server_default=text("0.0"))
  )
  created_at: Optional[datetime] = Field(
    default_factory=datetime.now, 
    sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )

  updated_at: Optional[datetime] = Field(
    default_factory=datetime.now,
    sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )

  author_id: Optional[int] = Field(default=None, foreign_key="user.id", ondelete="CASCADE")
  author: Optional["User"] = Relationship(back_populates="posts", passive_deletes='all')

