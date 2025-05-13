from sqlmodel import SQLModel, Field
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from app.models.post import PostBase

if TYPE_CHECKING:
    from ..schema.user_schema import UserResponse
    

class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author_id: int


class PostUpdate(PostBase):
    updated_at: Optional[datetime] = Field(default=datetime.now().isoformat())

class PostResponseWithUser(PostResponse):
    user: Optional['UserResponse'] = None