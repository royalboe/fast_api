from pydantic import EmailStr
from typing import Optional
from sqlmodel import SQLModel, Field

class UserLogin(SQLModel):
    """
    Schema for user login.
    """
    email: EmailStr = Field(min_length=1)
    password: str = Field(min_length=1)


class AuthResponse(SQLModel):
    """
    Schema for authentication response.
    """
    access_token: str
    token_type: str = "bearer"

class TokenData(SQLModel):
    """
    Schema for token data.
    """
    id: Optional[int]