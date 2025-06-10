from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..utils.dependencies import SessionDep
from ..models.user import User as UserModel
from sqlmodel import select
from ..schema.auth_schema import AuthResponse
from ..utils.hashing import verify_password
from ..utils.oauth2 import create_access_token

router = APIRouter()

@router.post("/login", response_model=AuthResponse)
def login(session: SessionDep, user_credentials: OAuth2PasswordRequestForm = Depends()):
# def login(session: SessionDep, user_credentials: LoginSchema):
    
    if not user_credentials.username or not user_credentials.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid credentials")

    user = session.exec(select(UserModel).where(UserModel.email == user_credentials.username)).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Create a JWT token here if needed
    access_token = create_access_token(data={"user_id": user.id})
    # Return token
    return {"access_token": access_token, "token_type": "bearer"}