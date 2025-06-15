from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Department import crud, schemas, models
from database import get_db
from dependencies import get_current_active_user, RoleChecker
from roles import RoleEnum as Role
from User.models import User
from Department.models import Department
from Department.schemas import DepartmentOut, DepartmentCreate

# Initialize FastAPI router with prefix and tags for department-related endpoints
router = APIRouter(prefix="/departments", tags=["Departments"])

# Create a role checker for admin and super_admin roles
role_admin = RoleChecker([Role.admin, Role.super_admin])

@router.post("/", response_model=schemas.DepartmentOut)
def create_department(dept: schemas.DepartmentCreate, db: Session = Depends(get_db),
                     current_user: User = Depends(role_admin)):
    # Endpoint to create a new department, restricted to admin/super_admin
    try:
        # Create a new Department instance with the provided name
        new_dept = Department(name=dept.name)
        # Add the department to the database session
        db.add(new_dept)
        # Commit the transaction to save the department
        db.commit()
        # Refresh the department object to get updated data from the database
        db.refresh(new_dept)
        # Return the created department
        return new_dept
    except Exception as e:
        # Log the error for debugging purposes
        print("create_department error:", repr(e))
        # Raise an HTTP 500 error with the exception details
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[schemas.Department])
def read_departments(db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_active_user)):
    # Endpoint to retrieve all departments, accessible to admin, super_admin, and employees
    # Restrict access: only admin, super_admin, and employees can view departments
    if current_user.role not in [Role.admin.value, Role.employee.value, Role.super_admin.value]:
        # Raise an HTTP 403 error if the user is not authorized
        raise HTTPException(status_code=403, detail="Not authorized to view departments")
    # Call the CRUD function to fetch all departments from the database
    return crud.get_departments(db)
