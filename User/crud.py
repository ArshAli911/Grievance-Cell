from sqlalchemy.orm import Session
from . import models, schemas
from Department.models import Department
from Department.crud import create_department, get_departments
from passlib.context import CryptContext
from typing import List, Optional

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to generate a hashed password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify if a plain password matches a hashed password
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Function to create a new user in the database
def create_user(db: Session, user: schemas.UserCreate):
    # If department_id is not provided, use/create a fallback department "OTR"
    if user.department_id is None:
        print("No department_id provided, checking for OTR...")
        department = db.query(Department).filter_by(name="OTR").first()
        if not department:
            print("OTR not found, creating...")
            department = Department(name="OTR")  # Create a new Department instance
            db.add(department)                  # Add department to the session
            db.commit()                         # Commit to persist the new department
            db.refresh(department)              # Refresh to get the assigned ID
            print("OTR created.")
        department_id = department.id           # Use the fetched/created department's ID
        print("Using department_id:", department_id)
    else:
        department_id = user.department_id      # Use the provided department ID

    # Create a new User instance with hashed password
    db_user = models.User(
        email=user.email,
        password=get_password_hash(user.password),  # Hash password for secure storage
        department_id=department_id,
        role=user.role
    )

    # Add user to the session and commit to save
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Refresh to get generated fields like ID
    return db_user       # Return the created user object

# Function to authenticate user credentials
def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    # Find user by email
    user = db.query(models.User).filter(models.User.email == email).first()
    
    # If user not found or password doesn't match, return None
    if not user:
        return None
    if not verify_password(password, user.password):
        return None

    # Return authenticated user
    return user

# Function to retrieve a list of users, optionally filtered by role(s)
def get_users(db: Session, role_filter: List[str] = None):
    query = db.query(models.User)  # Base query on User model
    
    # If role_filter is provided, apply filtering
    if role_filter:
        query = query.filter(models.User.role.in_(role_filter))
    
    # Return all matched users
    return query.all()

# Function to get a user by user ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
