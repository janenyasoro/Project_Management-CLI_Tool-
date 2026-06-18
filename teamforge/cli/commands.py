"""CLI command implementations"""

from typing import Optional
from rich.console import Console
from teamforge.services.data_manager import DataManager
from teamforge.models.user import User
from teamforge.models.project import Project
from teamforge.models.task import Task
from teamforge.cli.helpers import cli_command

console = Console()

class CommandHandler:
    """Handles all CLI commands"""
    
    def __init__(self):
        self.data_manager = DataManager()
    
    @cli_command
    def add_user(self, name: str, email: str, role: str = "developer") -> None:
        """Add a new user"""
        user = User(name, email, role)
        self.data_manager.save_user(user.to_dict())
        console.print(f"[green]✅ User '{name}' created with ID: {user.id}[/green]")
    
    @cli_command
    def list_users(self) -> None:
        """List all users"""
        from teamforge.utils.formatters import Formatters
        users = self.data_manager.get_users()
        Formatters.print_users(users)
    
    @cli_command
    def show_user(self, user_id: str) -> None:
        """Show user details"""
        from teamforge.utils.formatters import Formatters
        user_data = self.data_manager.find_user_by_id(user_id)
        if not user_data:
            console.print(f"[red]❌ User with ID '{user_id}' not found[/red]")
            return
        projects = self.data_manager.find_projects_by_user(user_id)
        Formatters.print_user_detail(user_data, projects)
    
    @cli_command
    def edit_user(self, user_id: str, name: Optional[str] = None, 
                  email: Optional[str] = None, role: Optional[str] = None,
                  active: Optional[bool] = None) -> None:
        """Edit a user"""
        user_data = self.data_manager.find_user_by_id(user_id)
        if not user_data:
            console.print(f"[red]❌ User with ID '{user_id}' not found[/red]")
            return
        if name:
            user_data["name"] = name
        if email:
            user_data["email"] = email
        if role:
            user_data["role"] = role
        if active is not None:
            user_data["is_active"] = active
        self.data_manager.save_user(user_data)
        console.print(f"[green]✅ User '{user_data['name']}' updated[/green]")
    
    @cli_command
    def delete_user(self, user_id: str) -> None:
        """Delete a user"""
        user_data = self.data_manager.find_user_by_id(user_id)
        if not user_data:
            console.print(f"[red]❌ User with ID '{user_id}' not found[/red]")
            return
        self.data_manager.delete_user(user_id)
        console.print(f"[green]✅ User '{user_data['name']}' deleted[/green]")
    
    @cli_command
    def add_project(self, user_id: str, title: str, description: str = "", due_date: str = "") -> None:
        """Add a new project"""
        user_data = self.data_manager.find_user_by_id(user_id)
        if not user_data:
            console.print(f"[red]❌ User with ID '{user_id}' not found[/red]")
            return
        project = Project(title, description, user_id, due_date)
        self.data_manager.save_project(project.to_dict())
        user = User.from_dict(user_data)
        user.add_project(project.id)
        self.data_manager.save_user(user.to_dict())
        console.print(f"[green]✅ Project '{title}' created with ID: {project.id}[/green]")
    
    @cli_command
    def list_projects(self, user_id: Optional[str] = None) -> None:
        """List all projects"""
        from teamforge.utils.formatters import Formatters
        if user_id:
            projects = self.data_manager.find_projects_by_user(user_id)
        else:
            projects = self.data_manager.get_projects()
        Formatters.print_projects(projects)
    
    @cli_command
    def show_project(self, project_id: str) -> None:
        """Show project details"""
        from teamforge.utils.formatters import Formatters
        project_data = self.data_manager.find_project_by_id(project_id)
        if not project_data:
            console.print(f"[red]❌ Project with ID '{project_id}' not found[/red]")
            return
        tasks = self.data_manager.find_tasks_by_project(project_id)
        Formatters.print_project_detail(project_data, tasks)
    
    @cli_command
    def edit_project(self, project_id: str, title: Optional[str] = None,
                     description: Optional[str] = None, due_date: Optional[str] = None,
                     status: Optional[str] = None) -> None:
        """Edit a project"""
        project_data = self.data_manager.find_project_by_id(project_id)
        if not project_data:
            console.print(f"[red]❌ Project with ID '{project_id}' not found[/red]")
            return
        if title:
            project_data["name"] = title
        if description is not None:
            project_data["description"] = description
        if due_date:
            project_data["due_date"] = due_date
        if status and status in Project.STATUSES:
            project_data["status"] = status
        self.data_manager.save_project(project_data)
        console.print(f"[green]✅ Project updated[/green]")
    
    @cli_command
    def delete_project(self, project_id: str) -> None:
        """Delete a project"""
        project_data = self.data_manager.find_project_by_id(project_id)
        if not project_data:
            console.print(f"[red]❌ Project with ID '{project_id}' not found[/red]")
            return
        self.data_manager.delete_project(project_id)
        console.print(f"[green]✅ Project deleted[/green]")
    
    @cli_command
    def add_task(self, project_id: str, title: str, description: str = "",
                 priority: str = "medium", due_date: str = "") -> None:
        """Add a new task"""
        project_data = self.data_manager.find_project_by_id(project_id)
        if not project_data:
            console.print(f"[red]❌ Project with ID '{project_id}' not found[/red]")
            return
        task = Task(title, description, project_id, priority)
        if due_date:
            task.set_due_date(due_date)
        self.data_manager.save_task(task.to_dict())
        project = Project.from_dict(project_data)
        project.add_task(task.id)
        self.data_manager.save_project(project.to_dict())
        console.print(f"[green]✅ Task '{title}' created with ID: {task.id}[/green]")
    
    @cli_command
    def list_tasks(self, project_id: Optional[str] = None) -> None:
        """List all tasks"""
        from teamforge.utils.formatters import Formatters
        if project_id:
            tasks = self.data_manager.find_tasks_by_project(project_id)
        else:
            tasks = self.data_manager.get_tasks()
        Formatters.print_tasks(tasks)
    
    @cli_command
    def show_task(self, task_id: str) -> None:
        """Show task details"""
        from teamforge.utils.formatters import Formatters
        task_data = self.data_manager.find_task_by_id(task_id)
        if not task_data:
            console.print(f"[red]❌ Task with ID '{task_id}' not found[/red]")
            return
        Formatters.print_task_detail(task_data)
    
    @cli_command
    def update_task(self, task_id: str, title: Optional[str] = None,
                    description: Optional[str] = None, status: Optional[str] = None,
                    priority: Optional[str] = None, due_date: Optional[str] = None) -> None:
        """Update a task"""
        task_data = self.data_manager.find_task_by_id(task_id)
        if not task_data:
            console.print(f"[red]❌ Task with ID '{task_id}' not found[/red]")
            return
        if title:
            task_data["title"] = title
        if description is not None:
            task_data["description"] = description
        if status and status in Task.STATUSES:
            task_data["status"] = status
        if priority and priority in Task.PRIORITIES:
            task_data["priority"] = priority
        if due_date:
            task_data["due_date"] = due_date
        self.data_manager.save_task(task_data)
        console.print(f"[green]✅ Task updated[/green]")
    
    @cli_command
    def assign_task(self, task_id: str, user_id: str) -> None:
        """Assign a task to a user"""
        task_data = self.data_manager.find_task_by_id(task_id)
        if not task_data:
            console.print(f"[red]❌ Task with ID '{task_id}' not found[/red]")
            return
        user_data = self.data_manager.find_user_by_id(user_id)
        if not user_data:
            console.print(f"[red]❌ User with ID '{user_id}' not found[/red]")
            return
        task = Task.from_dict(task_data)
        task.assign_to(user_id)
        self.data_manager.save_task(task.to_dict())
        console.print(f"[green]✅ Task assigned to {user_data['name']}[/green]")
    
    @cli_command
    def delete_task(self, task_id: str) -> None:
        """Delete a task"""
        task_data = self.data_manager.find_task_by_id(task_id)
        if not task_data:
            console.print(f"[red]❌ Task with ID '{task_id}' not found[/red]")
            return
        self.data_manager.delete_task(task_id)
        console.print(f"[green]✅ Task deleted[/green]")