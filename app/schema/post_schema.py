from sqlmodel import SQLModel, Field
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from ..schema.user_schema import UserResponse

class PostBase(SQLModel):
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

class PostResponseWithUser(PostResponse):
    user: Optional['UserResponse'] = None