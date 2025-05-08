from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os
from ..schema.auth_schema import TokenData
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode["exp"] = expire
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> dict:
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    if user_id is None:
      raise credentials_exception
    
    token_data = TokenData(id=user_id)
  except JWTError as e:
    print(e)
    raise credentials_exception
  return token_data


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  return verify_access_token(token, credentials_exception)