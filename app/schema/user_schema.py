from pydantic import EmailStr
from sqlmodel import Field
from ..models.user import UserBase

from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from ..schema.post_schema import PostResponse

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserResponse(UserBase):
    id: int

class UserUpdate(UserBase):
    username: Optional[str] = Field(default=None, min_length=1)
    email: Optional[EmailStr] = Field(default=None, min_length=1)
    password: Optional[str] = Field(default=None, min_length=1)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

class UserResponseWithPosts(UserResponse):
    posts: list['PostResponse'] = Field(default_factory=list)
