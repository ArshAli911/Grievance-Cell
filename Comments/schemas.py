from pydantic import BaseModel
from datetime import datetime

# Base schema containing shared fields for all comment-related operations
class CommentBase(BaseModel):
    grievance_id: int  # ID of the grievance the comment belongs to
    user_id: int       # ID of the user who made the comment
    content: str       # Text content of the comment

# Schema used when creating a new comment (inherits from CommentBase)
class CommentCreate(CommentBase):
    pass  # No additional fields needed for creation

# Schema used for reading a comment, including extra fields like ID and timestamp
class Comment(CommentBase):
    id: int                    # Unique ID of the comment
    timestamp: datetime        # Time when the comment was created

    class Config:
        orm_mode = True        # Enables ORM compatibility (e.g., with SQLAlchemy models)
