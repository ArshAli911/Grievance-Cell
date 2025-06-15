from sqlalchemy import Column, Integer, String  # Import SQLAlchemy column types
from database import Base  # Base class for model inheritance

# Define User model mapped to 'user_detail' table
class User(Base):
    __tablename__ = "user_detail"  # Set the table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key column with index
    name = Column(String, index=True)  # Name of the user, indexed for search
    email = Column(String, unique=True, index=True)  # Unique email field with index
    password = Column(String, index=True)  # Password field (should be stored as hashed)

# Define Admin model mapped to 'admin_detail' table
class Admin(Base):
    __tablename__ = "admin_detail"  # Set the table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key column with index
    name = Column(String, index=True)  # Name of the admin, indexed for search
    email = Column(String, unique=True, index=True)  # Unique email field with index
    password = Column(String, index=True)  # Password field (should be stored as hashed)

# Define Grievances model mapped to 'Grievances' table
class Grievances(Base):
    __tablename__ = "Grievances"  # Set the table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key column with index
    name = Column(String, index=True)  # Name of the person lodging the grievance
    Grievances_content = Column(String, index=True)  # Actual grievance content/text
    department = Column(String, index=True)  # Department related to the grievance
