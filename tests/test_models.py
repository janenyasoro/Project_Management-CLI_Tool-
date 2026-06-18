"""Unit tests for models"""

from teamforge.models.user import User
from teamforge.models.project import Project
from teamforge.models.task import Task

class TestUser:
    def test_create_user(self):
        user = User("John Doe", "john@example.com")
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert len(user.id) == 8

class TestProject:
    def test_create_project(self):
        project = Project("Test Project")
        assert project.name == "Test Project"
        assert project.status == "planning"

class TestTask:
    def test_create_task(self):
        task = Task("Test Task", priority="high")
        assert task.title == "Test Task"
        assert task.priority == "high"