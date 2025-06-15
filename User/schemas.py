# User/schemas.py
# Defines Pydantic models for user-related data validation and serialization in the application

from pydantic import BaseModel  # Import BaseModel for creating Pydantic models
from pydantic.networks import EmailStr  # Import EmailStr for email validation
from typing import Optional  # Import Optional for optional type hints
from roles import RoleEnum  # Import RoleEnum for user role enumeration

# Model for password reset requests
class PasswordReset(BaseModel):
    email: EmailStr  # User's email address, validated as a proper email format
    new_password: str  # New password to be set for the user

# Base model containing common user attributes
class UserBase(BaseModel):
    email: str  # User's email address
    password: str  # User's password
    department_id: Optional[int] = None  # Optional department ID, defaults to None if not provided
    role: RoleEnum = RoleEnum.user  # User role, defaults to 'user' from RoleEnum

# Model for limited user data, inheriting from UserBase
class UserLimited(UserBase):
    # Inherits all fields from UserBase, intentionally excludes department info in usage
    pass

# Model for complete user data, including department ID
class UserFull(UserBase):
    department_id: Optional[int]  # Explicitly includes department ID, remains optional

    # Pydantic configuration for the model
    class Config:
        orm_mode = True  # Enables ORM compatibility for database interactions
        from_attributes = True  # Allows model instantiation from object attributes

# Model for creating new users
class UserCreate(BaseModel):
    email: str  # Email address for the new user
    password: str  # Password for the new user
    department_id: Optional[int] = None  # Optional department ID, defaults to None
    role: RoleEnum  # Role for the new user, must be a valid RoleEnum value
