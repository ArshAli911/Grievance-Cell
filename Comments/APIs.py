from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from Comments import crud, schemas, models
from database import get_db
from dependencies import get_current_active_user
from roles import RoleEnum as Role

# Initialize FastAPI router with prefix and tags for comment-related endpoints
router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db),
                  current_user = Depends(get_current_active_user)):
    # Endpoint to create a new comment, restricted to specific roles
    # Check if the current user has a role allowed to comment (user, employee, admin, super_admin)
    if current_user.role not in [Role.user.value, Role.employee.value, Role.admin.value, Role.super_admin.value]:
        # Raise an HTTP 403 error if the user is not authorized
        raise HTTPException(status_code=403, detail="Not authorized to comment")
    # Call the CRUD function to create the comment in the database
    return crud.create_comment(db, comment)

@router.get("/grievance/{grievance_id}", response_model=List[schemas.Comment])
def get_comments(grievance_id: int, db: Session = Depends(get_db),
                current_user = Depends(get_current_active_user)):
    # Endpoint to retrieve all comments associated with a specific grievance ID
    # Call the CRUD function to fetch comments for the given grievance
    return crud.get_comments_by_grievance(db, grievance_id)
