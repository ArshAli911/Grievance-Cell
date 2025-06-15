# Database configuration and session management for SQLAlchemy

from sqlalchemy import create_engine  # Import function to create database engine
from sqlalchemy.ext.declarative import declarative_base  # Import function to create base class for models
from sqlalchemy.orm import sessionmaker  # Import function to create session factory

# Define the database URL for SQLite, pointing to a local file 'grievance.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./grievance.db"

# Create SQLAlchemy engine for database connection
# connect_args disables thread checking for SQLite to allow multi-threaded access
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory bound to the engine
# autocommit=False ensures manual transaction control, autoflush=False prevents auto-flushing
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models to inherit from
Base = declarative_base()

# Generator function to provide a database session
def get_db():
    # Create a new database session
    db = SessionLocal()
    try:
        # Yield the session for use in a context manager
        yield db
    finally:
        # Ensure the session is closed after use
        db.close()
