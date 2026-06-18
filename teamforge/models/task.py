"""Task model with assignments and status"""

import uuid
from datetime import datetime
from typing import List, Optional

class Task:
    """Task class with assignments and tracking"""
    
    STATUSES = ["todo", "in_progress", "review", "done"]
    PRIORITIES = ["low", "medium", "high", "critical"]
    
    def __init__(self, title: str, description: str = "", project_id: str = "", priority: str = "medium"):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.project_id = project_id
        self.status = "todo"
        self.priority = priority
        self.assigned_to = []
        self.created_by = ""
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.due_date = None
        self.completed_at = None
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "project_id": self.project_id,
            "status": self.status,
            "priority": self.priority,
            "assigned_to": self.assigned_to,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "due_date": self.due_date,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        task = cls(
            data["title"],
            data.get("description", ""),
            data.get("project_id", ""),
            data.get("priority", "medium")
        )
        task.id = data["id"]
        task.status = data["status"]
        task.assigned_to = data.get("assigned_to", [])
        task.created_by = data.get("created_by", "")
        task.created_at = data["created_at"]
        task.updated_at = data["updated_at"]
        task.due_date = data.get("due_date")
        task.completed_at = data.get("completed_at")
        return task
    
    def assign_to(self, user_id: str) -> None:
        if user_id not in self.assigned_to:
            self.assigned_to.append(user_id)
            self.updated_at = datetime.now().isoformat()
    
    def unassign(self, user_id: str) -> bool:
        if user_id in self.assigned_to:
            self.assigned_to.remove(user_id)
            self.updated_at = datetime.now().isoformat()
            return True
        return False
    
    def set_status(self, status: str) -> bool:
        if status in self.STATUSES:
            self.status = status
            self.updated_at = datetime.now().isoformat()
            if status == "done":
                self.completed_at = datetime.now().isoformat()
            else:
                self.completed_at = None
            return True
        return False
    
    def set_priority(self, priority: str) -> bool:
        if priority in self.PRIORITIES:
            self.priority = priority
            self.updated_at = datetime.now().isoformat()
            return True
        return False
    
    def set_due_date(self, due_date: str) -> None:
        self.due_date = due_date
        self.updated_at = datetime.now().isoformat()
    
    def is_overdue(self) -> bool:
        if not self.due_date or self.status == "done":
            return False
        try:
            due = datetime.fromisoformat(self.due_date)
            return datetime.now() > due
        except:
            return False
    
    def __str__(self) -> str:
        status_icon = {
            "todo": "⭕",
            "in_progress": "🔄",
            "review": "👀",
            "done": "✅"
        }.get(self.status, "❓")
        
        priority_icon = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🟠",
            "critical": "🔴"
        }.get(self.priority, "⚪")
        
        overdue = " ⚠️" if self.is_overdue() else ""
        return f"{status_icon} {self.title} [{self.status}]{overdue} - {priority_icon} {self.priority}"
    
    def __repr__(self) -> str:
        return f"Task(id='{self.id}', title='{self.title}', status='{self.status}')"