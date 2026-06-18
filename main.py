#!/usr/bin/env python3
"""TeamForge - Main CLI Entry Point"""

import argparse
import sys
from teamforge.cli.commands import CommandHandler
from teamforge.cli.helpers import print_banner, print_help
from teamforge.utils.formatters import console

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="TeamForge - Project Management CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # User commands
    add_user = subparsers.add_parser("add-user", help="Add a new user")
    add_user.add_argument("--name", required=True, help="User name")
    add_user.add_argument("--email", required=True, help="User email")
    add_user.add_argument("--role", default="developer", help="User role (admin, project_manager, developer, viewer)")
    
    list_users = subparsers.add_parser("list-users", help="List all users")
    
    show_user = subparsers.add_parser("show-user", help="Show user details")
    show_user.add_argument("--id", required=True, help="User ID")
    
    edit_user = subparsers.add_parser("edit-user", help="Edit a user")
    edit_user.add_argument("--id", required=True, help="User ID")
    edit_user.add_argument("--name", help="New name")
    edit_user.add_argument("--email", help="New email")
    edit_user.add_argument("--role", help="New role")
    edit_user.add_argument("--active", action="store_true", help="Set active")
    edit_user.add_argument("--inactive", action="store_true", help="Set inactive")
    
    delete_user = subparsers.add_parser("delete-user", help="Delete a user")
    delete_user.add_argument("--id", required=True, help="User ID")
    
    # Project commands
    add_project = subparsers.add_parser("add-project", help="Add a new project")
    add_project.add_argument("--user-id", required=True, help="User ID (project owner)")
    add_project.add_argument("--title", required=True, help="Project title")
    add_project.add_argument("--description", default="", help="Project description")
    add_project.add_argument("--due", default="", help="Due date (YYYY-MM-DD)")
    
    list_projects = subparsers.add_parser("list-projects", help="List projects")
    list_projects.add_argument("--user-id", help="Filter by user ID")
    
    show_project = subparsers.add_parser("show-project", help="Show project details")
    show_project.add_argument("--id", required=True, help="Project ID")
    
    edit_project = subparsers.add_parser("edit-project", help="Edit a project")
    edit_project.add_argument("--id", required=True, help="Project ID")
    edit_project.add_argument("--title", help="New title")
    edit_project.add_argument("--description", help="New description")
    edit_project.add_argument("--due", help="New due date (YYYY-MM-DD)")
    edit_project.add_argument("--status", help="New status (planning, active, on_hold, completed, archived)")
    
    delete_project = subparsers.add_parser("delete-project", help="Delete a project")
    delete_project.add_argument("--id", required=True, help="Project ID")
    
    # Task commands
    add_task = subparsers.add_parser("add-task", help="Add a new task")
    add_task.add_argument("--project-id", required=True, help="Project ID")
    add_task.add_argument("--title", required=True, help="Task title")
    add_task.add_argument("--description", default="", help="Task description")
    add_task.add_argument("--priority", default="medium", help="Priority (low, medium, high, critical)")
    add_task.add_argument("--due", default="", help="Due date (YYYY-MM-DD)")
    
    list_tasks = subparsers.add_parser("list-tasks", help="List tasks")
    list_tasks.add_argument("--project-id", help="Filter by project ID")
    
    show_task = subparsers.add_parser("show-task", help="Show task details")
    show_task.add_argument("--id", required=True, help="Task ID")
    
    update_task = subparsers.add_parser("update-task", help="Update a task")
    update_task.add_argument("--id", required=True, help="Task ID")
    update_task.add_argument("--title", help="New title")
    update_task.add_argument("--description", help="New description")
    update_task.add_argument("--status", help="New status (todo, in_progress, review, done)")
    update_task.add_argument("--priority", help="New priority (low, medium, high, critical)")
    update_task.add_argument("--due", help="New due date (YYYY-MM-DD)")
    
    assign_task = subparsers.add_parser("assign-task", help="Assign task to user")
    assign_task.add_argument("--id", required=True, help="Task ID")
    assign_task.add_argument("--user-id", required=True, help="User ID")
    
    delete_task = subparsers.add_parser("delete-task", help="Delete a task")
    delete_task.add_argument("--id", required=True, help="Task ID")
    
    # Help command
    subparsers.add_parser("help", help="Show help")
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no command, show help
    if not args.command:
        print_banner()
        print_help()
        return
    
    # Initialize command handler
    handler = CommandHandler()
    
    # Execute command
    if args.command == "add-user":
        handler.add_user(args.name, args.email, args.role)
    elif args.command == "list-users":
        handler.list_users()
    elif args.command == "show-user":
        handler.show_user(args.id)
    elif args.command == "edit-user":
        active = None
        if args.active:
            active = True
        elif args.inactive:
            active = False
        handler.edit_user(args.id, args.name, args.email, args.role, active)
    elif args.command == "delete-user":
        handler.delete_user(args.id)
    elif args.command == "add-project":
        handler.add_project(args.user_id, args.title, args.description, args.due)
    elif args.command == "list-projects":
        handler.list_projects(args.user_id)
    elif args.command == "show-project":
        handler.show_project(args.id)
    elif args.command == "edit-project":
        handler.edit_project(args.id, args.title, args.description, args.due, args.status)
    elif args.command == "delete-project":
        handler.delete_project(args.id)
    elif args.command == "add-task":
        handler.add_task(args.project_id, args.title, args.description, args.priority, args.due)
    elif args.command == "list-tasks":
        handler.list_tasks(args.project_id)
    elif args.command == "show-task":
        handler.show_task(args.id)
    elif args.command == "update-task":
        handler.update_task(args.id, args.title, args.description, args.status, args.priority, args.due)
    elif args.command == "assign-task":
        handler.assign_task(args.id, args.user_id)
    elif args.command == "delete-task":
        handler.delete_task(args.id)
    elif args.command == "help":
        print_help()
    else:
        print(f"Unknown command: {args.command}")
        print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)