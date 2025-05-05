from typing import Annotated, Optional
from datetime import datetime

from sqlmodel import Field, SQLModel

def now():
  return datetime.now()

class Post(SQLModel, table=True):
  id: Optional[int] = Field(primary_key=True, index=True)
  title: str = Field(nullable=False, index=True)
  content: str  = Field(nullable=False)
  published: bool = Field(default=True)   
  rating: Optional[float] = Field(default=0)
  created_at: datetime = Field(default_factory=now)