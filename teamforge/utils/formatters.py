"""Pretty printing and formatting utilities"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from typing import List, Dict
from datetime import datetime

console = Console()

class Formatters:
    """Collection of formatting functions"""
    
    @staticmethod
    def print_users(users: List[Dict]) -> None:
        """Print users in a nice table"""
        if not users:
            console.print("[yellow]No users found[/yellow]")
            return
        
        table = Table(title="👥 Users", box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="green")
        table.add_column("Email", style="blue")
        table.add_column("Role", style="yellow")
        table.add_column("Projects", style="magenta")
        table.add_column("Status", style="white")
        
        for user in users:
            status = "🟢 Active" if user.get("is_active", True) else "🔴 Inactive"
            table.add_row(
                user["id"],
                user["name"],
                user["email"],
                user.get("role", "developer"),
                str(len(user.get("projects", []))),
                status
            )
        
        console.print(table)
    
    @staticmethod
    def print_projects(projects: List[Dict]) -> None:
        """Print projects in a nice table"""
        if not projects:
            console.print("[yellow]No projects found[/yellow]")
            return
        
        table = Table(title="📁 Projects", box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Tasks", style="magenta")
        table.add_column("Due Date", style="blue")
        
        for project in projects:
            status_icon = {
                "planning": "📋",
                "active": "🔄",
                "on_hold": "⏸️",
                "completed": "✅",
                "archived": "📦"
            }.get(project["status"], "❓")
            
            table.add_row(
                project["id"],
                project["name"],
                f"{status_icon} {project['status']}",
                str(len(project.get("tasks", []))),
                project.get("due_date", "N/A")
            )
        
        console.print(table)
    
    @staticmethod
    def print_tasks(tasks: List[Dict]) -> None:
        """Print tasks in a nice table"""
        if not tasks:
            console.print("[yellow]No tasks found[/yellow]")
            return
        
        table = Table(title="✅ Tasks", box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Priority", style="red")
        table.add_column("Assigned To", style="blue")
        table.add_column("Due Date", style="magenta")
        
        for task in tasks:
            priority_colors = {
                "low": "🟢 low",
                "medium": "🟡 medium",
                "high": "🟠 high",
                "critical": "🔴 critical"
            }
            
            status_icons = {
                "todo": "⭕ todo",
                "in_progress": "🔄 in_progress",
                "review": "👀 review",
                "done": "✅ done"
            }
            
            assigned_count = len(task.get("assigned_to", []))
            table.add_row(
                task["id"],
                task["title"][:30] + ("..." if len(task["title"]) > 30 else ""),
                status_icons.get(task["status"], task["status"]),
                priority_colors.get(task["priority"], task["priority"]),
                f"{assigned_count} user(s)" if assigned_count > 0 else "Unassigned",
                task.get("due_date", "N/A")
            )
        
        console.print(table)
    
    @staticmethod
    def print_user_detail(user: Dict, projects: List[Dict]) -> None:
        """Print detailed user information"""
        panel = Panel(
            f"[bold]Name:[/bold] {user['name']}\n"
            f"[bold]Email:[/bold] {user['email']}\n"
            f"[bold]Role:[/bold] {user.get('role', 'developer')}\n"
            f"[bold]Status:[/bold] {'🟢 Active' if user.get('is_active', True) else '🔴 Inactive'}\n"
            f"[bold]Created:[/bold] {user.get('created_at', 'N/A')[:10]}\n"
            f"[bold]Projects:[/bold] {len(projects)}",
            title="👤 User Details",
            border_style="cyan"
        )
        console.print(panel)
        
        if projects:
            Formatters.print_projects(projects)
    
    @staticmethod
    def print_project_detail(project: Dict, tasks: List[Dict]) -> None:
        """Print detailed project information"""
        status_icons = {
            "planning": "📋",
            "active": "🔄",
            "on_hold": "⏸️",
            "completed": "✅",
            "archived": "📦"
        }
        
        panel = Panel(
            f"[bold]Name:[/bold] {project['name']}\n"
            f"[bold]Description:[/bold] {project.get('description', 'N/A')}\n"
            f"[bold]Status:[/bold] {status_icons.get(project['status'], '❓')} {project['status']}\n"
            f"[bold]Due Date:[/bold] {project.get('due_date', 'N/A')}\n"
            f"[bold]Tasks:[/bold] {len(tasks)}\n"
            f"[bold]Team Members:[/bold] {len(project.get('team_members', []))}",
            title="📁 Project Details",
            border_style="green"
        )
        console.print(panel)
        
        if tasks:
            Formatters.print_tasks(tasks)
    
    @staticmethod
    def print_task_detail(task: Dict) -> None:
        """Print detailed task information"""
        status_icons = {
            "todo": "⭕",
            "in_progress": "🔄",
            "review": "👀",
            "done": "✅"
        }
        
        priority_colors = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🟠",
            "critical": "🔴"
        }
        
        panel = Panel(
            f"[bold]Title:[/bold] {task['title']}\n"
            f"[bold]Description:[/bold] {task.get('description', 'N/A')}\n"
            f"[bold]Status:[/bold] {status_icons.get(task['status'], '❓')} {task['status']}\n"
            f"[bold]Priority:[/bold] {priority_colors.get(task['priority'], '⚪')} {task['priority']}\n"
            f"[bold]Assigned To:[/bold] {len(task.get('assigned_to', []))} user(s)\n"
            f"[bold]Due Date:[/bold] {task.get('due_date', 'N/A')}\n"
            f"[bold]Created:[/bold] {task.get('created_at', 'N/A')[:19]}\n"
            f"[bold]Completed:[/bold] {task.get('completed_at', 'Not completed')[:19] if task.get('completed_at') else 'Not completed'}",
            title="✅ Task Details",
            border_style="yellow"
        )
        console.print(panel)