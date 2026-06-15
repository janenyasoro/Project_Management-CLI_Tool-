#!/usr/bin/env python3
"""
Project Management Tool - Main Entry Point
"""

from cli.commands import ProjectManagerCLI

def main():
    app = ProjectManagerCLI()
    app.run()

if __name__ == "__main__":
    main()