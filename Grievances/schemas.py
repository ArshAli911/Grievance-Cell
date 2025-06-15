from pydantic import BaseModel
from datetime import datetime

# Schema for creating a new grievance (input model)
class GrievanceCreate(BaseModel):
    department_id: int  # ID of the department to which the grievance is related

# Schema for reading grievance details (output model)
class GrievanceOut(BaseModel):
    id: int                    # Auto-incremented primary key ID of the grievance
    ticket_id: str             # Unique ticket ID generated for the grievance
    user_id: int               # ID of the user who submitted the grievance
    department_id: int         # ID of the department involved
    assigned_to: int | None    # ID of the employee assigned (None if unassigned)
    status: str                # Current status of the grievance (e.g., pending, solved)
    created_at: datetime       # Timestamp when the grievance was created

    class Config:
        # Enable compatibility with ORM objects (e.g., SQLAlchemy models)
        orm_mode = True
