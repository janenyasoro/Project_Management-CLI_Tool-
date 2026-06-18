"""Project model with tasks and team"""

import uuid
from datetime import datetime
from typing import List, Optional

class Project:
    """Project class with tasks and team members"""
    
    STATUSES = ["planning", "active", "on_hold", "completed", "archived"]
    
    def __init__(self, name: str, description: str = "", owner_id: str = "", due_date: str = ""):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.due_date = due_date
        self.status = "planning"
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.tasks = []
        self.team_members = []
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "due_date": self.due_date,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "tasks": self.tasks,
            "team_members": self.team_members
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        project = cls(
            data["name"],
            data.get("description", ""),
            data.get("owner_id", ""),
            data.get("due_date", "")
        )
        project.id = data["id"]
        project.status = data["status"]
        project.created_at = data["created_at"]
        project.updated_at = data["updated_at"]
        project.tasks = data.get("tasks", [])
        project.team_members = data.get("team_members", [])
        return project
    
    def add_task(self, task_id: str) -> None:
        if task_id not in self.tasks:
            self.tasks.append(task_id)
            self.updated_at = datetime.now().isoformat()
    
    def remove_task(self, task_id: str) -> bool:
        if task_id in self.tasks:
            self.tasks.remove(task_id)
            self.updated_at = datetime.now().isoformat()
            return True
        return False
    
    def add_member(self, user_id: str) -> None:
        if user_id not in self.team_members:
            self.team_members.append(user_id)
            self.updated_at = datetime.now().isoformat()
    
    def remove_member(self, user_id: str) -> bool:
        if user_id in self.team_members:
            self.team_members.remove(user_id)
            self.updated_at = datetime.now().isoformat()
            return True
        return False
    
    def set_status(self, status: str) -> bool:
        if status in self.STATUSES:
            self.status = status
            self.updated_at = datetime.now().isoformat()
            return True
        return False
    
    def get_task_count(self) -> int:
        return len(self.tasks)
    
    def __str__(self) -> str:
        return f"📁 {self.name} [{self.status}] - {len(self.tasks)} tasks"
    
    def __repr__(self) -> str:
        return f"Project(id='{self.id}', name='{self.name}', status='{self.status}')"