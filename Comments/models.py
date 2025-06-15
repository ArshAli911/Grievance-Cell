from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# Define the Comment model for the comments table
class Comment(Base):
    # Specify the database table name for comments
    __tablename__ = "comments"
    
    # Primary key column for unique comment ID
    id = Column(Integer, primary_key=True, index=True)
    # Foreign key linking to the grievance associated with the comment
    grievance_id = Column(Integer, ForeignKey("grievances.id"))
    # Foreign key linking to the user who created the comment
    user_id = Column(Integer, ForeignKey("users.id"))
    # Text content of the comment
    content = Column(String)
    # Timestamp for when the comment was created, defaults to current UTC time
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Define relationship to the Grievance model for the associated grievance
    grievance = relationship("Grievance")
    # Define relationship to the User model for the comment creator
    user = relationship("User")
