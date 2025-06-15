from fastapi import APIRouter, Depends, HTTPException, status  # FastAPI modules for routing, dependency injection, and error handling
from sqlalchemy.orm import Session  # SQLAlchemy session for database interaction
from fastapi.security import OAuth2PasswordRequestForm  # Form class for handling OAuth2 login requests
from datetime import timedelta  # To set token expiration time

from database import get_db  # Dependency to get database session
from User import crud, schemas  # Importing CRUD operations and data schemas for the User
from dependencies import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES  # JWT utility functions and token duration
from roles import RoleEnum  # Enum class for user roles

# Create a new API router for authentication-related endpoints
router = APIRouter(tags=["Authentication"])

# Endpoint for user registration (signup)
@router.post("/signup", response_model=schemas.UserFull, status_code=status.HTTP_201_CREATED)
def signup(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # Fetch all existing users (optionally filter by role)
    existing = crud.get_users(db, role_filter=None)
    # Check if the email is already registered
    if any(u.email == user_in.email for u in existing):
        raise HTTPException(status_code=400, detail="Email already registered")
    # Create a new user if email is unique
    return crud.create_user(db, user_in)

# Endpoint for user login and JWT generation
@router.post("/login", summary="Login and get JWT")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Authenticate user with provided email and password
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        # Raise error if authentication fails
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Set the expiration duration for the JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Create a new JWT access token with user ID as the subject
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    # Return the token in response
    return {"access_token": access_token, "token_type": "bearer"}
