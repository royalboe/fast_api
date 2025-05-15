from typing import Optional, Annotated
from datetime import datetime
from sqlmodel import Field
from pydantic import EmailStr, conint
from pydantic import Field as PyField

from app.models.post import PostBase
from ..models.user import UserBase
from sqlmodel import SQLModel

# Post Schema
class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author_id: int

class PostUpdate(PostBase):
    updated_at: Optional[datetime] = Field(default=datetime.now().isoformat())

# User Schema
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserResponse(UserBase):
    id: int

class UserUpdate(UserBase):
    username: Optional[str] = Field(default=None, min_length=1)
    email: Optional[EmailStr] = Field(default=None, min_length=1)
    password: Optional[str] = Field(default=None, min_length=1)
    updated_at: Optional[datetime] = Field(default=datetime.now)

# Vote

class VoteBase(SQLModel):
    post_id: int
    dir: Annotated[int, PyField(strict=True, le=1)]

# With relationships

class PostResponseWithUser(PostResponse):
    author: Optional["UserResponse"] = None

class UserResponseWithPosts(UserResponse):
    posts: list['PostResponse'] = []