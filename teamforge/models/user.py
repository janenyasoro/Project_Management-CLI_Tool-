"""User model with project relationships"""

import uuid
from datetime import datetime
from typing import List, Optional

class User:
    """User class representing a system user"""
    
    def __init__(self, name: str, email: str, role: str = "developer"):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self._email = email  # Protected for property
        self.role = role  # admin, project_manager, developer, viewer
        self.created_at = datetime.now().isoformat()
        self.is_active = True
        self.projects = []  # List of project IDs
    
    @property
    def email(self) -> str:
        """Get email with validation"""
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        """Set email with validation"""
        import re
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            self._email = value
        else:
            raise ValueError("Invalid email format")
    
    def to_dict(self) -> dict:
        """Convert user to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self._email,
            "role": self.role,
            "created_at": self.created_at,
            "is_active": self.is_active,
            "projects": self.projects
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary"""
        user = cls(data["name"], data["email"], data.get("role", "developer"))
        user.id = data["id"]
        user.created_at = data["created_at"]
        user.is_active = data.get("is_active", True)
        user.projects = data.get("projects", [])
        return user
    
    def add_project(self, project_id: str) -> None:
        """Add a project to user's list"""
        if project_id not in self.projects:
            self.projects.append(project_id)
    
    def remove_project(self, project_id: str) -> bool:
        """Remove a project from user's list"""
        if project_id in self.projects:
            self.projects.remove(project_id)
            return True
        return False
    
    def get_project_count(self) -> int:
        """Get number of projects assigned"""
        return len(self.projects)
    
    def __str__(self) -> str:
        return f"👤 {self.name} ({self.email}) - {self.role} [{len(self.projects)} projects]"
    
    def __repr__(self) -> str:
        return f"User(id='{self.id}', name='{self.name}', email='{self._email}')"