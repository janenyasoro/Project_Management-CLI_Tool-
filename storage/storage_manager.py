import json
import os
from models import User, Project, Task

class Storage:
    def __init__(self, filename):
        self.filename = filename
        self.users = []
        self.projects = []
        self.tasks = []
        self.next_ids = {"user": 1, "project": 1, "task": 1}
        self.load()

    def load(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.users = [User.from_dict(u) for u in data.get("users", [])]
                self.projects = [Project.from_dict(p) for p in data.get("projects", [])]
                self.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
                self.next_ids = data.get("next_ids", {"user": 1, "project": 1, "task": 1})
        except Exception as e:
            print(f"Error loading data: {e}")

    def save(self):
        data = {
            "users": [u.to_dict() for u in self.users],
            "projects": [p.to_dict() for p in self.projects],
            "tasks": [t.to_dict() for t in self.tasks],
            "next_ids": self.next_ids,
        }
        try:
            with open(self.filename, "w") as f:
                json.dump(data, f, indent=2)
            print("Data saved.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def get_next_id(self, entity):
        next_id = self.next_ids[entity]
        self.next_ids[entity] += 1
        return next_id

    def find_user_by_id(self, user_id):
        return next((u for u in self.users if u.id == user_id), None)

    def find_project_by_id(self, project_id):
        return next((p for p in self.projects if p.id == project_id), None)

    def find_task_by_id(self, task_id):
        return next((t for t in self.tasks if t.id == task_id), None)

    def get_projects_by_user(self, user_id):
        return [p for p in self.projects if p.user_id == user_id]

    def get_tasks_by_project(self, project_id):
        return [t for t in self.tasks if t.project_id == project_id]