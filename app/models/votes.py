from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
  from app.models.user import User
  from app.models.post import Post

class Vote(SQLModel, table=True):
  __tablename__ = 'votes'
  user_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True, ondelete='CASCADE')
  post_id: int | None = Field(default=None, foreign_key="posts.id", primary_key=True, ondelete='CASCADE')

  user: Optional["User"] = Relationship(back_populates="votes")
  post: Optional["Post"] = Relationship(back_populates="votes")