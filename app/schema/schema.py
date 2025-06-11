from __future__ import annotations

from typing import Annotated
from datetime import datetime
from sqlmodel import Field
from pydantic import EmailStr
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
    author: UserResponse | None = None

class PostUpdate(PostBase):
    updated_at: datetime | None = Field(default=datetime.now().isoformat())

# User Schema
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserResponse(UserBase):
    id: int

class UserUpdate(UserBase):
    username: str | None = Field(default=None, min_length=1)
    email: EmailStr | None = Field(default=None, min_length=1)
    password: str | None = Field(default=None, min_length=1)
    updated_at: datetime | None = Field(default=datetime.now)

# Vote

class VoteBase(SQLModel):
    post_id: int
    dir: Annotated[int, PyField(strict=True, ge=0, le=1)]

# With relationships

class PostResponseWithUser(PostResponse):
    author: UserResponse | None = None

class UserResponseWithPosts(UserResponse):
    posts: list[PostResponse] = []

class PostWithVotesSchema(SQLModel):
    Post: PostResponse
    votes: int
