from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Union
from passlib.context import CryptContext
from User import crud, schemas, models
from database import get_db
from dependencies import get_current_active_user, RoleChecker
from roles import RoleEnum as Role

# Initialize FastAPI router with prefix and tags for user-related endpoints
router = APIRouter(prefix="/users", tags=["Users"])

# Configure password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create a role checker for admin, employee, and super_admin roles
role_admin_employee_super = RoleChecker([Role.admin, Role.employee, Role.super_admin])

@router.post("/", response_model=schemas.UserFull)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(role_admin_employee_super),
):
    # Endpoint to create a new user, restricted to admin, employee, or super_admin
    # Call the CRUD function to create and return the user
    return crud.create_user(db, user)

@router.get("/", response_model=List[Union[schemas.UserLimited, schemas.UserFull]])
def read_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    # Endpoint to retrieve all users, with role-based response data
    # Fetch all users from the database
    users = crud.get_users(db)
    # If the current user is a regular user, return limited user information
    if current_user.role == Role.user:
        return [schemas.UserLimited.from_orm(u) for u in users]
    # If the current user is admin, employee, or super_admin, return full user information
    return [schemas.UserFull.from_orm(u) for u in users]

@router.get("/{user_id}", response_model=Union[schemas.UserLimited, schemas.UserFull])
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    # Endpoint to retrieve a single user by ID, with role-based response data
    # Fetch the user by ID from the database
    user = crud.get_user(db, user_id)
    # Raise an HTTP 404 error if the user is not found
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # If the current user is viewing their own profile or has elevated roles, return full info
    if current_user.id == user_id or current_user.role in [Role.admin, Role.employee, Role.super_admin]:
        return schemas.UserFull.from_orm(user)

    # If the current user is a regular user, return limited info
    if current_user.role == Role.user:
        return schemas.UserLimited.from_orm(user)

    # Raise an HTTP 403 error if the user is not authorized
    raise HTTPException(status_code=403, detail="Not authorized")

@router.post("/reset-password")
def reset_password(data: schemas.PasswordReset, db: Session = Depends(get_db)):
    # Endpoint to reset a user's password using
