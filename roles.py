# roles.py
# Defines an enumeration for user roles in the application

from enum import Enum  # Import Enum class for creating enumerations

# Define a string-based enumeration for user roles
class RoleEnum(str, Enum):
    user = "user"  # Regular user role
    employee = "employee"  # Employee role
    admin = "admin"  # Administrator role
    super_admin = "super_admin"  # Super administrator role with elevated privileges
