from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import custom modules for CRUD operations, schemas, and models
from Grievances import crud, schemas, models
from User.models import User
from database import get_db
from dependencies import get_current_active_user, RoleChecker
from roles import RoleEnum

# Define role-based access control
admin_only = RoleChecker([RoleEnum.admin, RoleEnum.super_admin])  # Only admins and super_admins
user_only  = RoleChecker([RoleEnum.user])                         # Only users
emp_only   = RoleChecker([RoleEnum.employee])                     # Only employees

# Create an API router for grievance-related endpoints
router = APIRouter(prefix="/grievances", tags=["Grievances"])

# Endpoint to create a grievance (accessible only by users)
@router.post("/", response_model=schemas.GrievanceOut)
def create_grievance(
    grievance: schemas.GrievanceCreate,                  # Input grievance data
    db: Session = Depends(get_db),                       # Dependency to get DB session
    current_user: User = Depends(user_only),             # Dependency to ensure only users can access
):
    # Only users can raise grievances
    return crud.create_grievance(db, grievance, current_user.id)

# Endpoint to read grievances based on user role
@router.get("/", response_model=List[schemas.GrievanceOut])
def read_grievances(
    db: Session = Depends(get_db),                       # Dependency to get DB session
    current_user: User = Depends(get_current_active_user),  # Get the current authenticated user
):
    # Users see only their own grievances
    if current_user.role == RoleEnum.user:
        return crud.get_grievances_by_user(db, current_user.id)
    
    # Employees see grievances assigned to them
    if current_user.role == RoleEnum.employee:
        return crud.get_grievances_by_employee(db, current_user.id)
    
    # Admins and Super Admins see all grievances
    if current_user.role in (RoleEnum.admin, RoleEnum.super_admin):
        return crud.get_all_grievances(db)
    
    # If role is not recognized, deny access
    raise HTTPException(status_code=403, detail="Not authorized")

# Endpoint to assign grievances to employees (accessible only by admins and super_admins)
@router.post("/assign", status_code=status.HTTP_204_NO_CONTENT)
def assign_all(
    db: Session = Depends(get_db),                       # Dependency to get DB session
    current_user: User = Depends(admin_only),            # Only admin/super_admin allowed
):
    # Assign all pending grievances to employees
    crud.assign_grievances_to_employees(db)
    return  # No content response

# Endpoint to mark a grievance as resolved or not resolved
@router.post("/{grievance_id}/resolve", response_model=schemas.GrievanceOut)
def resolve_grievance(
    grievance_id: int,                                   # ID of the grievance to resolve
    resolver_id: int,                                    # ID of the person resolving it
    solved: bool = True,                                 # Status flag (solved or not)
    db: Session = Depends(get_db),                       # Dependency to get DB session
):
    """
    Mark a grievance as solved or not solved.
    Also updates resolver ID and resolved timestamp.
    """
    updated = crud.resolve_grievance(db, grievance_id, resolver_id, solved)
    
    # If the grievance does not exist, raise a 404 error
    if not updated:
        raise HTTPException(404, "Grievance not found")
    
    # Return updated grievance data
    return updated
