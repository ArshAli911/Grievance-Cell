# Main FastAPI application setup with middleware, routers, and database initialization

from fastapi import FastAPI  # Import FastAPI framework for building APIs
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware for cross-origin requests

from database import engine, Base  # Import SQLAlchemy engine and base class for database
from Department.APIs import router as dept_router  # Import Department API router
from User.APIs import router as user_router  # Import User API router
from Grievances.APIs import router as grv_router  # Import Grievances API router
from Comments.APIs import router as com_router  # Import Comments API router
import auth  # Import authentication module (assumed to contain auth router)
import User.APIs as user_apis  # Import User APIs module (assumed to contain additional router)
from Department import models as dept_models  # Import Department database models
from User import models as user_models  # Import User database models

# Create all database tables defined in the Base metadata
Base.metadata.create_all(bind=engine)
# Create Department-specific database tables
dept_models.Base.metadata.create_all(bind=engine)
# Create User-specific database tables
user_models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI application with debug mode enabled
app = FastAPI(debug=True)

# Register API routers to include their endpoints in the application
app.include_router(dept_router)  # Include Department API endpoints
app.include_router(user_router)  # Include User API endpoints
app.include_router(user_apis.router)  # Include additional User API endpoints
app.include_router(auth.router)  # Include authentication API endpoints
app.include_router(grv_router)  # Include Grievances API endpoints
app.include_router(com_router)  # Include Comments API endpoints

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,  # Allow credentials (e.g., cookies) in requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers in requests
)
