from sqlalchemy.orm import Session
from . import models, schemas

# Function to create a new department
def create_department(db: Session, department: schemas.DepartmentCreate):
    # Create a Department model instance with the provided name
    db_department = models.Department(name=department.name)
    
    # Add the new department to the current database session
    db.add(db_department)
    
    # Commit the session to persist the new department in the database
    db.commit()
    
    # Refresh the instance to retrieve updated fields like generated ID
    db.refresh(db_department)
    
    # Return the created department object
    return db_department

# Function to retrieve all departments from the database
def get_departments(db: Session):
    # Query and return all Department records
    return db.query(models.Department).all()
