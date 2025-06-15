from sqlalchemy.orm import Session
from . import models, schemas
from User.models import User
from .models import GrievanceStatus
from roles import RoleEnum
import uuid
import datetime

def create_grievance(db: Session, grievance: schemas.GrievanceCreate, user_id: int):
    # Generate a unique ticket ID using UUID4
    ticket = str(uuid.uuid4())
    # Create a new Grievance object with ticket ID, user ID, and department ID
    db_g = models.Grievance(
        ticket_id=ticket,
        user_id=user_id,
        department_id=grievance.department_id
    )
    # Add the grievance to the database session
    db.add(db_g)
    # Commit the transaction to save the grievance to the database
    db.commit()
    # Refresh the grievance object to get updated data from the database
    db.refresh(db_g)
    # Return the created grievance object
    return db_g

def assign_grievances_to_employees(db: Session):
    # Query all unassigned grievances (where assigned_to is None)
    pend = db.query(models.Grievance)\
             .filter(models.Grievance.assigned_to.is_(None))\
             .all()
    # Query all users with the role of employee
    emps = db.query(User).filter(User.role == RoleEnum.employee).all()
    # If no employees are found, exit the function
    if not emps:
        return
    # Assign grievances to employees in a round-robin fashion
    for i, g in enumerate(pend):
        g.assigned_to = emps[i % len(emps)].id
    # Commit the changes to the database
    db.commit()

def get_grievances_by_user(db: Session, user_id: int):
    # Query all grievances associated with the given user ID
    return db.query(models.Grievance)\
             .filter(models.Grievance.user_id == user_id)\
             .all()

def get_grievances_by_employee(db: Session, employee_id: int):
    # Query all grievances assigned to the given employee ID
    return db.query(models.Grievance)\
             .filter(models.Grievance.assigned_to == employee_id)\
             .all()

def get_all_grievances(db: Session):
    # Query all grievances in the database
    return db.query(models.Grievance).all()

def resolve_grievance(
    db: Session,
    grievance_id: int,
    resolver_id: int,
    solved: bool = True
) -> models.Grievance | None:
    # Fetch the grievance by its ID
    g = db.query(models.Grievance).filter(models.Grievance.id == grievance_id).first()
    # If grievance not found, return None
    if not g:
        return None
    # Update grievance status based on the 'solved' parameter
    g.status = GrievanceStatus.solved if solved else GrievanceStatus.not_solved
    # Record the ID of the resolver
    g.resolved_by = resolver_id
    # Record the current UTC timestamp as the resolution time
    g.resolved_at = datetime.datetime.utcnow()
    # Commit the changes to the database
    db.commit()
    # Refresh the grievance object to get updated data
    db.refresh(g)
    # Return the updated grievance object
    return g
