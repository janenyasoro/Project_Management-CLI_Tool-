"""Unit tests for models"""

import pytest
from datetime import datetime
from teamforge.models.user import User
from teamforge.models.project import Project
from teamforge.models.task import Task

class TestUser:
    """Test User model"""
    
    def test_create_user(self):
        user = User("John Doe", "john@example.com", "developer")
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.role == "developer"
        assert len(user.id) == 8
        assert user.is_active is True
    
    def test_email_validation(self):
        user = User("Test", "test@example.com")
        
        with pytest.raises(ValueError):
            user.email = "invalid-email"
    
    def test_user_to_dict(self):
        user = User("Alice", "alice@example.com")
        data = user.to_dict()
        
        assert data["name"] == "Alice"
        assert data["email"] == "alice@example.com"
        assert "id" in data
        assert "created_at" in data
    
    def test_user_from_dict(self):
        data = {
            "id": "TEST123",
            "name": "Bob",
            "email": "bob@example.com",
            "role": "admin",
            "created_at": datetime.now().isoformat(),
            "is_active": True,
            "projects": []
        }
        
        user = User.from_dict(data)
        assert user.id == "TEST123"
        assert user.name == "Bob"
        assert user.email == "bob@example.com"
        assert user.role == "admin"
    
    def test_add_project(self):
        user = User("Test", "test@example.com")
        user.add_project("PROJ123")
        assert "PROJ123" in user.projects
        assert len(user.projects) == 1
        
        # Test duplicate
        user.add_project("PROJ123")
        assert len(user.projects) == 1
    
    def test_remove_project(self):
        user = User("Test", "test@example.com")
        user.add_project("PROJ123")
        
        result = user.remove_project("PROJ123")
        assert result is True
        assert "PROJ123" not in user.projects
        
        result = user.remove_project("NONEXISTENT")
        assert result is False

class TestProject:
    """Test Project model"""
    
    def test_create_project(self):
        project = Project("Test Project", "Description", "USER123", "2024-12-31")
        assert project.name == "Test Project"
        assert project.description == "Description"
        assert project.owner_id == "USER123"
        assert project.due_date == "2024-12-31"
        assert project.status == "planning"
        assert len(project.id) == 8
    
    def test_add_task(self):
        project = Project("Test")
        project.add_task("TASK123")
        assert "TASK123" in project.tasks
        assert len(project.tasks) == 1
    
    def test_remove_task(self):
        project = Project("Test")
        project.add_task("TASK123")
        
        result = project.remove_task("TASK123")
        assert result is True
        assert "TASK123" not in project.tasks
    
    def test_set_status(self):
        project = Project("Test")
        
        result = project.set_status("active")
        assert result is True
        assert project.status == "active"
        
        result = project.set_status("invalid")
        assert result is False
        assert project.status == "active"
    
    def test_add_member(self):
        project = Project("Test")
        project.add_member("USER123")
        assert "USER123" in project.team_members
    
    def test_project_to_dict(self):
        project = Project("Test")
        data = project.to_dict()
        
        assert data["name"] == "Test"
        assert "id" in data
        assert "tasks" in data

class TestTask:
    """Test Task model"""
    
    def test_create_task(self):
        task = Task("Test Task", "Description", "PROJ123", "high")
        assert task.title == "Test Task"
        assert task.description == "Description"
        assert task.project_id == "PROJ123"
        assert task.priority == "high"
        assert task.status == "todo"
        assert len(task.id) == 8
    
    def test_set_status(self):
        task = Task("Test")
        
        result = task.set_status("in_progress")
        assert result is True
        assert task.status == "in_progress"
        
        result = task.set_status("done")
        assert result is True
        assert task.status == "done"
        assert task.completed_at is not None
        
        result = task.set_status("invalid")
        assert result is False
    
    def test_set_priority(self):
        task = Task("Test")
        
        result = task.set_priority("critical")
        assert result is True
        assert task.priority == "critical"
        
        result = task.set_priority("invalid")
        assert result is False
    
    def test_assign_to(self):
        task = Task("Test")
        task.assign_to("USER123")
        assert "USER123" in task.assigned_to
        assert len(task.assigned_to) == 1
        
        # Test duplicate
        task.assign_to("USER123")
        assert len(task.assigned_to) == 1
    
    def test_unassign(self):
        task = Task("Test")
        task.assign_to("USER123")
        
        result = task.unassign("USER123")
        assert result is True
        assert "USER123" not in task.assigned_to
        
        result = task.unassign("NONEXISTENT")
        assert result is False
    
    def test_set_due_date(self):
        task = Task("Test")
        task.set_due_date("2024-12-31")
        assert task.due_date == "2024-12-31"
    
    def test_task_to_dict(self):
        task = Task("Test")
        data = task.to_dict()
        
        assert data["title"] == "Test"
        assert "id" in data
        assert "status" in data
    
    def test_task_from_dict(self):
        data = {
            "id": "TASK123",
            "title": "Test Task",
            "description": "Description",
            "project_id": "PROJ123",
            "status": "todo",
            "priority": "high",
            "assigned_to": [],
            "created_by": "",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "due_date": None,
            "completed_at": None
        }
        
        task = Task.from_dict(data)
        assert task.id == "TASK123"
        assert task.title == "Test Task"
        assert task.priority == "high"