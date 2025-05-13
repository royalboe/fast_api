from fastapi import APIRouter, HTTPException, status, Response
from sqlmodel import select
from typing import List

from ..models.user import User as UserModel
from ..schema.schema import UserCreate, UserUpdate, UserResponseWithPosts
from ..utils.dependencies import SessionDep
from ..utils.hashing import hash_password

router = APIRouter()

@router.get("/health")
def users():
    """
    Retrieve all blog posts.
    Returns a list of all stored posts.
    """
    return {"message": "Hello from users"}

@router.get("/", response_model=List[UserResponseWithPosts])
def get_users(session: SessionDep):
    """
    Retrieve all users.
    Returns a list of all stored users.
    """
    users = session.exec(select(UserModel)).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponseWithPosts)
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
    hash = hash_password(user.password)
    extra_data = {"hashed_password": hash}
    db_user = UserModel.model_validate(user, update=extra_data)
    # db_user = UserModel(**user.model_dump(exclude_unset=True))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=UserResponseWithPosts)
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

@router.patch("/", response_model=UserResponseWithPosts)
def update_user(user: UserUpdate, session: SessionDep):
    """
    Update a user by their unique ID.
    If the user exists, updates it; otherwise, raises a 404 error.
    """
    # db_user = session.get(UserModel, request.form.get("user_email"))
    statement = select(UserModel).where(UserModel.email == user.email)
    db_user = session.exec(statement).first()

    if not db_user:
        # Return 404 if not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with email {user.email} found")    
    # Update the user
    updated_data = user.model_dump(exclude_unset=True)
    extra_data = {}
    # Hash password if provided
    if "password" in updated_data:
         password = updated_data["password"]
         hash = hash_password(password)
         extra_data = {"hashed_password": hash}
    
    db_user.sqlmodel_update(updated_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: SessionDep):
    """
    Delete a user by their unique ID.
    If the user exists, deletes it; otherwise, raises a 404 error.
    """
    user = session.get(UserModel, user_id)
    if not user:
        # Return 404 if not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    
    session.delete(user)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)