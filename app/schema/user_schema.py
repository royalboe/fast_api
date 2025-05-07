from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class UserBase(SQLModel):
    username: Optional[str] = Field(min_length=1)
    email: EmailStr = Field(min_length=1)
    password: str = Field(min_length=1)
    
class UserCreate(UserBase):
    pass

class UserResponse(SQLModel):
    # id: int
    username: Optional[str] = Field(default=None, min_length=1)
    email: EmailStr = Field(min_length=1)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class UserUpdate(UserBase):
    username: Optional[str] = Field(default=None, min_length=1)
    email: Optional[str] = Field(default=None, min_length=1)
    password: Optional[str] = Field(default=None, min_length=1)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
