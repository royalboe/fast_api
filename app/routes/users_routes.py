from fastapi import APIRouter, HTTPException, status, Response
from sqlmodel import select
from typing import List

from ..models.user import User as UserModel
from ..schema.user_schema import UserCreate, UserUpdate, UserResponse
from ..dependencies import SessionDep
from ..hashing import hash_password, verify_password

router = APIRouter()

@router.get("/")
def users(session: SessionDep):
    """
    Retrieve all blog posts.
    Returns a list of all stored posts.
    """
    return {"message": "Hello from users"}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, session: SessionDep):
    """
    Create a new user.
    """
    if session.exec(select(UserModel).where(UserModel.email == user.email)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    if session.exec(select(UserModel).where(UserModel.username == user.username)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    # db_user = UserModel.model_validate(user)
    user.password = hash_password(user.password)
    db_user = UserModel(**user.model_dump(exclude_unset=True))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: SessionDep):
    """
    Get a user by their unique ID.
    If the user exists, returns it; otherwise, raises a 404 error.
    """
    user = session.get(UserModel, user_id)
    if not user:
        # Return 404 if not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user