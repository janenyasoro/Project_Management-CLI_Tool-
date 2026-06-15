
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

## Project Structure
