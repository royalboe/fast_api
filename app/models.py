from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Boolean, Float, DateTime, text
# from sqlalchemy.sql.expression import text
# from sqlalchemy.sql.sqltypes import TIMESTAMP

from sqlmodel import Field, SQLModel

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