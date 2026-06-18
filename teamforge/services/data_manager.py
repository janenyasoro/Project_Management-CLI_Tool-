"""Data persistence manager using JSON"""

import json
import os
from typing import Dict, List, Any, Optional

class DataManager:
    """Handles JSON file I/O for all data"""
    
    DATA_FILE = "data/data.json"
    
    def __init__(self):
        self.data = {
            "users": [],
            "projects": [],
            "tasks": []
        }
        self._ensure_data_directory()
        self.load()
    
    def _ensure_data_directory(self) -> None:
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
    
    def load(self) -> None:
        try:
            if os.path.exists(self.DATA_FILE):
                with open(self.DATA_FILE, 'r') as f:
                    loaded_data = json.load(f)
                    self.data.update(loaded_data)
            else:
                self.save()
        except (json.JSONDecodeError, FileNotFoundError):
            self.data = {"users": [], "projects": [], "tasks": []}
            self.save()
    
    def save(self) -> None:
        try:
            with open(self.DATA_FILE, 'w') as f:
                json.dump(self.data, f, indent=2)
            return True
        except Exception:
            return False
    
    def get_users(self) -> List[Dict]:
        return self.data.get("users", [])
    
    def get_projects(self) -> List[Dict]:
        return self.data.get("projects", [])
    
    def get_tasks(self) -> List[Dict]:
        return self.data.get("tasks", [])
    
    def save_user(self, user_dict: Dict) -> None:
        users = self.get_users()
        for i, u in enumerate(users):
            if u["id"] == user_dict["id"]:
                users[i] = user_dict
                break
        else:
            users.append(user_dict)
        self.save()
    
    def save_project(self, project_dict: Dict) -> None:
        projects = self.get_projects()
        for i, p in enumerate(projects):
            if p["id"] == project_dict["id"]:
                projects[i] = project_dict
                break
        else:
            projects.append(project_dict)
        self.save()
    
    def save_task(self, task_dict: Dict) -> None:
        tasks = self.get_tasks()
        for i, t in enumerate(tasks):
            if t["id"] == task_dict["id"]:
                tasks[i] = task_dict
                break
        else:
            tasks.append(task_dict)
        self.save()
    
    def delete_user(self, user_id: str) -> bool:
        users = self.get_users()
        for i, u in enumerate(users):
            if u["id"] == user_id:
                users.pop(i)
                self.save()
                return True
        return False
    
    def delete_project(self, project_id: str) -> bool:
        projects = self.get_projects()
        for i, p in enumerate(projects):
            if p["id"] == project_id:
                projects.pop(i)
                self.save()
                return True
        return False
    
    def delete_task(self, task_id: str) -> bool:
        tasks = self.get_tasks()
        for i, t in enumerate(tasks):
            if t["id"] == task_id:
                tasks.pop(i)
                self.save()
                return True
        return False
    
    def find_user_by_id(self, user_id: str) -> Optional[Dict]:
        for user in self.get_users():
            if user["id"] == user_id:
                return user
        return None
    
    def find_project_by_id(self, project_id: str) -> Optional[Dict]:
        for project in self.get_projects():
            if project["id"] == project_id:
                return project
        return None
    
    def find_task_by_id(self, task_id: str) -> Optional[Dict]:
        for task in self.get_tasks():
            if task["id"] == task_id:
                return task
        return None
    
    def find_user_by_name(self, name: str) -> Optional[Dict]:
        for user in self.get_users():
            if user["name"].lower() == name.lower():
                return user
        return None
    
    def find_projects_by_user(self, user_id: str) -> List[Dict]:
        user = self.find_user_by_id(user_id)
        if not user:
            return []
        project_ids = user.get("projects", [])
        return [p for p in self.get_projects() if p["id"] in project_ids]
    
    def find_tasks_by_project(self, project_id: str) -> List[Dict]:
        project = self.find_project_by_id(project_id)
        if not project:
            return []
        task_ids = project.get("tasks", [])
        return [t for t in self.get_tasks() if t["id"] in task_ids]