from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum
from enum import Enum as PyEnum
from sqlalchemy.sql import func
from datetime import datetime
from database import Base
from roles import RoleEnum

class GrievanceStatus(str, PyEnum):
    # Define grievance status options as an enumeration
    pending = "pending"
    solved = "solved"
    not_solved = "not_solved"

class Grievance(Base):
    # Define the database table name for grievances
    __tablename__ = "grievances"
    
    # Primary key column for unique grievance ID
    id = Column(Integer, primary_key=True, index=True)
    # Unique ticket ID for each grievance, indexed for faster lookup
    ticket_id = Column(String, unique=True, index=True)
    # Foreign key linking to the user who created the grievance
    user_id = Column(Integer, ForeignKey("users.id"))
    # Foreign key linking to the department associated with the grievance
    department_id = Column(Integer, ForeignKey("departments.id"))
    # Foreign key linking to the user (employee) assigned to handle the grievance, nullable
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    # Status of the grievance, using the GrievanceStatus enum, defaults to 'pending'
    status = Column(SQLEnum(GrievanceStatus), default=GrievanceStatus.pending)
    # Timestamp for when the grievance was created, auto-set to current time
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Foreign key linking to the user who resolved the grievance, nullable
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    # Timestamp for when the grievance was resolved, nullable
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Define relationship to the User model for the grievance creator
    user = relationship("User", foreign_keys=[user_id])
    # Define relationship to the Department model
    department = relationship("Department")
    # Define relationship to the User model for the assigned employee
    employee = relationship("User", foreign_keys=[assigned_to])
    # Define relationship to the User model for the resolver
    resolver = relationship("User", foreign_keys=[resolved_by])
