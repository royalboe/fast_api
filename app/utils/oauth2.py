from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from ..schema.auth_schema import TokenData
from ..utils.dependencies import SessionDep
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from ..models.user import User as UserModel
from ..config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict) -> str:
  """
  Create a JWT access token with an expiration time.
  Args:
      data (dict): The data to encode in the token, typically user information.
  Returns:
      str: The encoded JWT token as a string.
  """
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode["exp"] = expire
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> TokenData:
  """
  Verify the JWT access token and return the user ID if valid.
  Args:
      token (str): The JWT token to verify.
      credentials_exception: Exception to raise if the token is invalid.
  Returns:
      TokenData: An object containing the user ID extracted from the token.
  """
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("payload", payload)
    user_id = payload.get("user_id")
    exp = payload.get("exp")
    print("exp", exp)
    if user_id is None:
      raise credentials_exception
    
    if exp is None or datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
      print("Token has expired")
      raise HTTPException(
        status_code=status.HTTP_403_UNAUTHORIZED,
        detail="Token has expired",
        headers={"WWW-Authenticate": "Bearer"},
      )
    return TokenData(id=user_id)
  except JWTError as e:
    print(e)
    raise credentials_exception


def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)) -> UserModel:
  """
  Get the current user from the JWT token.
  Args:
      token (str): The JWT token to verify.
      session (SessionDep): The database session dependency.
  Returns:
      UserModel: The user object corresponding to the token.
  Raises:
      HTTPException: If the token is invalid or the user is not found.
  """
  
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )

  user_id = verify_access_token(token, credentials_exception).id
  if user_id is None:
    raise credentials_exception
  user = session.get(UserModel, user_id)
  if user is None:
    raise credentials_exception
  
  return user