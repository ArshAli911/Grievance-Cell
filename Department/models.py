from sqlalchemy import Column, Integer, String
from database import Base

# SQLAlchemy model representing the 'departments' table
class Department(Base):
    __tablename__ = "departments"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Primary key column with index
    name = Column(String, unique=True, index=True, nullable=False)  # Department name, must be unique and not null
