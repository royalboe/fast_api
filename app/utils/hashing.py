# Using argon2 for hashing passwords
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

ph = PasswordHasher()

def hash_password(password: str) -> str:
    """Hash a plain-text password using argon2."""
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a hashed password."""
    try:
        return ph.verify(hashed_password, plain_password)
    except (VerifyMismatchError, VerificationError) as e:
        # If the password does not match, an exception is raised
        print(f"Password verification failed: {e}")
        # Return False to indicate the password does not match
        return False



# # CryptoContext is a library for hashing passwords
# from passlib.context import CryptContext

# # Set up bcrypt hashing context \ which is the global instance for the app
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def hash_password(password: str) -> str:
#     """Hash a plain-text password."""
#     return pwd_context.hash(password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """Verify a plain-text password against a hashed password."""
#     return pwd_context.verify(plain_password, hashed_password)
