from fastapi import Depends, HTTPException, status  # Import FastAPI dependencies for request handling and error responses
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials  # OAuth2 and Bearer token handling
from sqlalchemy.orm import Session  # SQLAlchemy session management
from jose import JWTError, jwt  # JWT encoding and decoding
from database import get_db  # Function to get DB session
from User import models  # User model for querying database
from roles import RoleEnum as Role  # Enum for user roles
from typing import List  # For type annotations
from datetime import datetime, timedelta  # For time-based token expiration

# Constants for JWT creation
SECRET_KEY = "your-secret-key"  # Secret key for signing JWTs (replace with a secure value in production)
ALGORITHM = "HS256"  # Algorithm used for signing JWTs
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Default token expiration time in minutes

oauth2_scheme = HTTPBearer()  # Scheme to extract Bearer token from request headers

# Function to create a JWT access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()  # Create a copy of the payload data
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))  # Set expiration time
    to_encode.update({"exp": expire})  # Add expiration to payload
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode and return JWT token

# Optional helper function to retrieve a database session
def get_db_session():
    return get_db()

# Dependency to get the currently authenticated user from a JWT token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
    token = credentials.credentials  # Extract token from Authorization header
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token and extract user ID
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))  # Extract user ID from the 'sub' claim
        if user_id is None:
            raise credentials_exception
    except JWTError:
        # Raise error if token is invalid or decoding fails
        raise credentials_exception

    # Fetch the user from the database
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception  # Raise error if user doesn't exist
    return user  # Return the authenticated user

# Dependency that returns the current authenticated and active user
def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    return current_user

# Class-based dependency to enforce role-based access control
class RoleChecker:
    def __init__(self, allowed_roles: List[Role]):
        # Convert Enum values to string if necessary
        self.allowed_roles = [role.value if isinstance(role, Role) else role for role in allowed_roles]

    def __call__(self, current_user: models.User = Depends(get_current_active_user)):
        # Check if current user's role is in the list of allowed roles
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return current_user  # Return the user if role is permitted
