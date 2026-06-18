"""CLI helper functions and decorators"""

import functools
from typing import Callable
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()

def cli_command(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled[/yellow]")
            return
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
            return
    return wrapper

def print_banner():
    """Print application banner"""
    try:
        from pyfiglet import figlet_format
        banner = figlet_format("TeamForge", font="small")
        console.print(Panel(banner, style="bold cyan", border_style="blue"))
    except ImportError:
        console.print("[bold cyan]═══════════════════════════════════[/bold cyan]")
        console.print("[bold yellow]         TeamForge CLI[/bold yellow]")
        console.print("[bold cyan]═══════════════════════════════════[/bold cyan]")
    
    console.print("[dim]Project Management System v1.0[/dim]\n")

def print_help():
    """Print help menu"""
    from rich.table import Table
    
    table = Table(title="📚 Available Commands", box=box.ROUNDED)
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    table.add_column("Example", style="yellow")
    
    commands = [
        ("add-user", "Add a new user", "add-user --name \"Alice\" --email \"alice@example.com\""),
        ("list-users", "List all users", "list-users"),
        ("show-user", "Show user details", "show-user --id USER123"),
        ("edit-user", "Edit a user", "edit-user --id USER123 --name \"New Name\""),
        ("delete-user", "Delete a user", "delete-user --id USER123"),
        ("add-project", "Add a new project", "add-project --user-id USER123 --title \"API\" --due \"2024-12-31\""),
        ("list-projects", "List all projects", "list-projects"),
        ("show-project", "Show project details", "show-project --id PROJ456"),
        ("edit-project", "Edit a project", "edit-project --id PROJ456 --status completed"),
        ("delete-project", "Delete a project", "delete-project --id PROJ456"),
        ("add-task", "Add a new task", "add-task --project-id PROJ456 --title \"Implement auth\" --priority high"),
        ("list-tasks", "List all tasks", "list-tasks"),
        ("show-task", "Show task details", "show-task --id TASK789"),
        ("update-task", "Update a task", "update-task --id TASK789 --status done"),
        ("assign-task", "Assign task to user", "assign-task --id TASK789 --user-id USER123"),
        ("delete-task", "Delete a task", "delete-task --id TASK789"),
        ("help", "Show this help", "help"),
    ]
    
    for cmd, desc, example in commands:
        table.add_row(cmd, desc, example)
    
    console.print(table)