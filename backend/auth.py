from typing import Optional
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel

# --- Configuration (CRITICAL: Replace with environment variables in production) ---
# This key is used to sign and verify JWT tokens. It MUST be kept secret and strong.
# In a real application, fetch this from an environment variable (e.g., os.getenv("SECRET_KEY"))
SECRET_KEY = "your-super-secret-key-please-change-this-in-production" # <-- CHANGE THIS
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Not directly used in get_current_user, but useful for token creation

# --- Pydantic Models ---
# Represents a user as exposed by the API (e.g., for profile data)
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

# Represents a user as stored in the database (includes sensitive data like hashed_password)
class UserInDB(User):
    hashed_password: str

# Represents the data extracted from the JWT payload
class TokenData(BaseModel):
    username: Optional[str] = None

# --- Security Scheme ---
# OAuth2PasswordBearer is used to extract the token from the Authorization header.
# `tokenUrl` specifies the URL where the client can obtain a token (e.g., login endpoint).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token") # Adjust "/token" to your actual login/token endpoint

# --- Mock Database (CRITICAL: Replace with actual database interaction) ---
# In a real application, this would fetch user data from a persistent database
# (e.g., PostgreSQL, MongoDB) based on the username.
users_db = {
    "testuser": UserInDB(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        # IMPORTANT: In a real app, this would be a securely hashed password!
        # Use libraries like 'passlib' (e.g., bcrypt) to hash passwords.
        # This is a placeholder for demonstration purposes.
        hashed_password="hashed_test_password_placeholder"
    )
}

def get_user_from_db(username: str):
    """
    Simulates fetching a user from a database based on their username.
    In a real application, this function would perform a database query.
    """
    return users_db.get(username)

# --- CRITICAL FIX: get_current_user implementation ---
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    FastAPI dependency function to get the current authenticated user.
    It extracts the JWT token, decodes it, validates it, and fetches the user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # The 'sub' (subject) claim typically holds the user identifier (e.g., username)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # Create a TokenData instance from the decoded username
        token_data = TokenData(username=username)
    except JWTError:
        # If decoding fails (e.g., invalid signature, expired token), raise an exception
        raise credentials_exception

    # Fetch the user from the "database" using the username from the token
    user = get_user_from_db(username=token_data.username)
    if user is None:
        # If the user specified in the token does not exist, it's also an authentication failure
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Optional: Add checks for user status, e.g., if the user is disabled
    # if user.disabled:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    # Return a User object (without sensitive data like hashed password)
    return User(username=user.username, email=user.email, full_name=user.full_name, disabled=user.disabled)