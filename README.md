
# Project Management Tool

A command-line project management system for development teams that enables administrators to manage users, projects, and tasks with data persistence and relationship mapping.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
  - [Getting Started](#getting-started)
  - [User Management](#user-management)
  - [Project Management](#project-management)
  - [Task Management](#task-management)
- [Command Reference](#command-reference)
- [Data Relationships](#data-relationships)
- [Data Persistence](#data-persistence)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Extending the Tool](#extending-the-tool)
- [Contributing](#contributing)
- [License](#license)

## Overview

This Project Management Tool is a CLI-based application designed for development teams to organize their work efficiently. It provides a structured way to manage:

- **Users** - Team members and contributors
- **Projects** - Work initiatives owned by specific users
- **Tasks** - Actionable items within projects with multiple contributors

The tool implements proper data relationships (one-to-many and many-to-many) and persists all data to a JSON file for long-term storage.

## Features

### Core Features
- ✅ **User Management** - Create and list team members
- ✅ **Project Management** - Add projects to specific users, view user projects
- ✅ **Task Management** - Create tasks, assign contributors, mark tasks complete
- ✅ **Data Persistence** - Automatic saving to JSON file, manual save option
- ✅ **Relationship Mapping** - One-to-many (User → Projects) and many-to-many (Projects ↔ Tasks with contributors)

### Technical Features
- Modular code structure with separation of concerns
- Input validation and error handling
- Intuitive CLI with help system
- Extensible design for future enhancements

## Installation

# Clone repository
cd Project_Management-CLI_Tool-

# Install dependencies
pip install -r requirements.txt

# Run the tool
python main.py

Usage Examples
# User Management
python main.py add-user --name "Alice Johnson" --email "alice@example.com"
python main.py list-users
python main.py show-user --id USER123

# Project Management
python main.py add-project --user-id USER123 --title "API Development" --description "Build REST API" --due "2024-12-31"
python main.py list-projects --user-id USER123
python main.py show-project --id PROJ456

# Task Management
python main.py add-task --project-id PROJ456 --title "Design database schema" --priority high
python main.py list-tasks --project-id PROJ456
python main.py update-task --id TASK789 --status done
Testing
bash
pytest tests/ -v


License
MIT

---

## File 2: `requirements.txt`
```txt
rich==13.7.0
tabulate==0.9.0
python-dateutil==2.8.2
colorama==0.4.6
pyfiglet==0.8.post1
pytest==7.4.3
pytest-cov==4.1.0
