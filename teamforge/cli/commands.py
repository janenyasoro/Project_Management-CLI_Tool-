"""CLI command implementations"""

from typing import Optional, Dict
from rich.console import Console
from teamforge.services.data_manager import DataManager
from teamforge.models.user import User
from teamforge.models.project import Project
from teamforge.models.task import Task
from teamforge.utils.validators import Validators
from teamforge.utils.formatters import Formatters
from teamforge.cli.helpers import cli_command, require_confirmation, get_input, get_choice

console = Console()

class CommandHandler:
    """Handles all CLI commands"""
    
    def __init__(self):
        self.data_manager = DataManager()
    
    @cli_command
    def add_user(self, name: str, email: str, role: str = "developer") -> None:
        """Add a new user"""
        # Validate inputs
        if not Validators.validate_name(name):
            console.print("[red]❌ Invalid name[/red]")
            return
        
        if not Validators.validate_email(email):
            console.print("[red]❌ Invalid email format[/red]")
            return
        
        if not Validators.validate_role(role):
            console.print(f"[red]❌ Invalid role. Must be one of: admin, project_manager, developer, viewer[/red]")
            return
        
        # Check if user already exists
        existing = self.data_manager.find_user_by_name(name)
        if existing:
            console.print(f"[red]❌ User '{name}' already exists[/red]")
            return
        
        # Create user
        user = User(name, email, role)
        self.data_manager.save_user(user.to_dict())
        console.print(f"[green]✅ User '{name}' created with ID: {user.id}[/green]")
    
    @cli_command
    def list_users(self) -> None:
        """List all users"""
        users = self.data_manager.get_users()
        Formatters.print_users(users)
    
    @cli_command
    def show_user(self, user_id: str) -> None:
        """Show user details"""
        user_data = self.data_manager.find_user_by_id(user_id)
        if not user_data:
            console.print(f"[red]❌ User with ID '{user_id}' not found[/red]")
            return
        
        # Get user's projects
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
        
        # Update fields
        if name and Validators.validate_name(name):
            user_data["name"] = name
        if email and Validators.validate_email(email):
            user_data["email"] = email
        if role and Validators.validate_role(role):
            user_data["role"] = role
        if active is not None:
            user_data["is_active"] = active
        
        self.data_manager.save_user(user_data)
        console.print(f"[green]✅ User '{user_data['name']}' updated successfully[/green]")
    
    @cli_command
    @require_confirmation("Delete this user?")
    def delete_user(self, user_id: str) -> None:
        """Delete a user"""
        user_data = self.data_manager.find_user_by_id(user_id)
        if not user_data:
            console.print(f"[red]❌ User with ID '{user_id}' not found[/red]")
            return
        
        # Remove user from projects
        projects = self.data_manager.find_projects_by_user(user_id)
        for project in projects:
            if user_id in project.get("team_members", []):
                project["team_members"].remove(user_id)
                self.data_manager.save_project(project)
        
        # Delete user
        if self.data_manager.delete_user(user_id):
            console.print(f"[green]✅ User '{user_data['name']}' deleted successfully[/green]")
    
    @cli_command
    def add_project(self, user_id: str, title: str, description: str = "", due_date: str = "") -> None:
        """Add a new project"""
        # Validate user exists
        user_data = self.data_manager.find_user_by_id(user_id)
        if not user_data:
            console.print(f"[red]❌ User with ID '{user_id}' not found[/red]")
            return
        
        if due_date and not Validators.validate_date(due_date):
            console.print("[red]❌ Invalid date format. Use YYYY-MM-DD[/red]")
            return
        
        # Create project
        project = Project(title, description, user_id, due_date)
        self.data_manager.save_project(project.to_dict())
        
        # Add project to user
        user = User.from_dict(user_data)
        user.add_project(project.id)
        self.data_manager.save_user(user.to_dict())
        
        console.print(f"[green]✅ Project '{title}' created with ID: {project.id}[/green]")
    
    @cli_command
    def list_projects(self, user_id: Optional[str] = None) -> None:
        """List all projects or projects for a specific user"""
        if user_id:
            user_data = self.data_manager.find_user_by_id(user_id)
            if not user_data:
                console.print(f"[red]❌ User with ID '{user_id}' not found[/red]")
                return
            
            projects = self.data_manager.find_projects_by_user(user_id)
            console.print(f"[cyan]Projects for {user_data['name']}:[/cyan]")
            Formatters.print_projects(projects)
        else:
            projects = self.data_manager.get_projects()
            Formatters.print_projects(projects)
    
    @cli_command
    def show_project(self, project_id: str) -> None:
        """Show project details"""
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
        
        # Update fields
        if title:
            project_data["name"] = title
        if description is not None:
            project_data["description"] = description
        if due_date and Validators.validate_date(due_date):
            project_data["due_date"] = due_date
        if status and status in Project.STATUSES:
            project_data["status"] = status
        
        self.data_manager.save_project(project_data)
        console.print(f"[green]✅ Project '{project_data['name']}' updated successfully[/green]")
    
    @cli_command
    @require_confirmation("Delete this project?")
    def delete_project(self, project_id: str) -> None:
        """Delete a project"""
        project_data = self.data_manager.find_project_by_id(project_id)
        if not project_data:
            console.print(f"[red]❌ Project with ID '{project_id}' not found[/red]")
            return
        
        # Remove project from users
        for user in self.data_manager.get_users():
            if project_id in user.get("projects", []):
                user["projects"].remove(project_id)
                self.data_manager.save_user(user)
        
        # Delete project
        if self.data_manager.delete_project(project_id):
            console.print(f"[green]✅ Project '{project_data['name']}' deleted successfully[/green]")
    
    @cli_command
    def add_task(self, project_id: str, title: str, description: str = "",
                 priority: str = "medium", due_date: str = "") -> None:
        """Add a new task"""
        # Validate project exists
        project_data = self.data_manager.find_project_by_id(project_id)
        if not project_data:
            console.print(f"[red]❌ Project with ID '{project_id}' not found[/red]")
            return
        
        if not Validators.validate_priority(priority):
            console.print("[red]❌ Invalid priority. Must be: low, medium, high, critical[/red]")
            return
        
        if due_date and not Validators.validate_date(due_date):
            console.print("[red]❌ Invalid date format. Use YYYY-MM-DD[/red]")
            return
        
        # Create task
        task = Task(title, description, project_id, priority)
        if due_date:
            task.set_due_date(due_date)
        
        self.data_manager.save_task(task.to_dict())
        
        # Add task to project
        project = Project.from_dict(project_data)
        project.add_task(task.id)
        self.data_manager.save_project(project.to_dict())
        
        console.print(f"[green]✅ Task '{title}' created with ID: {task.id}[/green]")
    
    @cli_command
    def list_tasks(self, project_id: Optional[str] = None) -> None:
        """List all tasks or tasks for a specific project"""
        if project_id:
            project_data = self.data_manager.find_project_by_id(project_id)
            if not project_data:
                console.print(f"[red]❌ Project with ID '{project_id}' not found[/red]")
                return
            
            tasks = self.data_manager.find_tasks_by_project(project_id)
            console.print(f"[cyan]Tasks for project '{project_data['name']}':[/cyan]")
            Formatters.print_tasks(tasks)
        else:
            tasks = self.data_manager.get_tasks()
            Formatters.print_tasks(tasks)
    
    @cli_command
    def show_task(self, task_id: str) -> None:
        """Show task details"""
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
        
        # Update fields
        if title:
            task_data["title"] = title
        if description is not None:
            task_data["description"] = description
        if status and Validators.validate_status(status):
            task_data["status"] = status
            if status == "done":
                from datetime import datetime
                task_data["completed_at"] = datetime.now().isoformat()
        if priority and Validators.validate_priority(priority):
            task_data["priority"] = priority
        if due_date and Validators.validate_date(due_date):
            task_data["due_date"] = due_date
        
        self.data_manager.save_task(task_data)
        console.print(f"[green]✅ Task '{task_data['title']}' updated successfully[/green]")
    
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
        
        # Assign task
        task = Task.from_dict(task_data)
        task.assign_to(user_id)
        self.data_manager.save_task(task.to_dict())
        
        console.print(f"[green]✅ Task '{task.title}' assigned to {user_data['name']}[/green]")
    
    @cli_command
    @require_confirmation("Delete this task?")
    def delete_task(self, task_id: str) -> None:
        """Delete a task"""
        task_data = self.data_manager.find_task_by_id(task_id)
        if not task_data:
            console.print(f"[red]❌ Task with ID '{task_id}' not found[/red]")
            return
        
        # Remove task from project
        project_id = task_data.get("project_id")
        if project_id:
            project_data = self.data_manager.find_project_by_id(project_id)
            if project_data:
                if task_id in project_data.get("tasks", []):
                    project_data["tasks"].remove(task_id)
                    self.data_manager.save_project(project_data)
        
        # Delete task
        if self.data_manager.delete_task(task_id):
            console.print(f"[green]✅ Task '{task_data['title']}' deleted successfully[/green]")