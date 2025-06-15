from pydantic import BaseModel

# Base Pydantic model for shared department attributes
class DepartmentBase(BaseModel):
    # Define the department name as a string field
    name: str

# Pydantic model for creating a department, inheriting from DepartmentBase
class DepartmentCreate(DepartmentBase):
    # No additional fields or logic needed for creation
    pass

# Pydantic model for department output, used for API responses
class DepartmentOut(BaseModel):
    # Define the department ID as an integer field
    id: int
    # Include the department name from DepartmentBase
    name: str

# Pydantic model for representing a department with ORM compatibility
class Department(DepartmentBase):
    # Define the department ID as an integer field
    id: int
    # Configuration class to enable ORM mode
    class Config:
        # Enable ORM mode to allow mapping from SQLAlchemy models to Pydantic
        orm_mode = True
