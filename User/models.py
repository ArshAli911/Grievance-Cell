from sqlalchemy import Column, Integer, String, Enum, ForeignKey  # Import necessary SQLAlchemy classes
from database import Base  # Import Base class for SQLAlchemy model inheritance
from roles import RoleEnum  # Import custom Enum class for user roles

# Define the User model which inherits from SQLAlchemy's Base class
class User(Base):
    __tablename__ = "users"  # Set the table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key column with indexing for faster queries
    name = Column(String, nullable=True)  # User's name (optional)
    email = Column(String, unique=True, index=True)  # User's email, must be unique and indexed
    password = Column(String)  # Hashed password for the user
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)  # Foreign key to departments table (optional)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)  # Role of the user, defaults to 'user' from RoleEnum
