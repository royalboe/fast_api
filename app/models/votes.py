from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
  from app.models.user import User
  from app.models.post import Post

class Vote(SQLModel, table=True):
  user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True, ondelete='CASCADE')
  post_id: Optional[int] = Field(default=None, foreign_key="post.id", primary_key=True, ondelete='CASCADE')

  user: Optional["User"] = Relationship(back_populates="votes", cascade_delete=True)
  post: Optional["Post"] = Relationship(back_populates="votes", cascade_delete=True)