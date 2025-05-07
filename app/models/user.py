from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Boolean, Float, DateTime, text
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
  id: Optional[int] = Field(primary_key=True, index=True)
  email: str = Field(nullable=False, index=True, unique=True)
  password: str = Field(nullable=False)
  created_at: Optional[datetime] = Field(
    default_factory=datetime.now,
    sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )
  full_name: Optional[str] = Field(default=None, nullable=True)

  updated_at: Optional[datetime] = Field(
    default_factory=datetime.now,
    sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )
  created_at: Optional[datetime] = Field(
    default_factory=datetime.now, 
    sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )
