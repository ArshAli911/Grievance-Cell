from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

# Function to create a new comment on a grievance
def create_comment(db: Session, comment: schemas.CommentCreate):
    # Create a Comment instance using data from the input schema
    # Add a timestamp for when the comment was created
    db_comment = models.Comment(**comment.dict(), timestamp=datetime.now())
    
    # Add the new comment to the current database session
    db.add(db_comment)
    
    # Commit the session to save the comment in the database
    db.commit()
    
    # Refresh the instance to load any updated/generated fields
    db.refresh(db_comment)
    
    # Return the newly created comment object
    return db_comment

# Function to fetch all comments associated with a specific grievance
def get_comments_by_grievance(db: Session, grievance_id: int):
    grievance_id = int(grievance_id)  # Ensure grievance_id is treated as an integer
    
    # Query and return all comments linked to the specified grievance
    return db.query(models.Comment).filter(models.Comment.grievance_id == grievance_id).all()
