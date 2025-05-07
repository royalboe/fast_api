from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    published: Optional[bool] = True
    rating: Optional[float] = 0.0
    

class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    # id: int
    created_at: datetime
    updated_at: datetime


class PostUpdate(PostBase):
    title: Optional[str] = Field(default=None, min_length=1)
    content: Optional[str] = Field(default=None, min_length=1)
    published: Optional[float] = Field(default=None)
    rating: Optional[float] = Field(default=None)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)