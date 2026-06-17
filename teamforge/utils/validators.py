"""Input validation utilities"""

import re
from datetime import datetime
from typing import Optional

class Validators:
    """Collection of validation functions"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Validate date format (YYYY-MM-DD)"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_name(name: str) -> bool:
        """Validate name (non-empty, reasonable length)"""
        return bool(name.strip()) and len(name.strip()) <= 100
    
    @staticmethod
    def validate_priority(priority: str) -> bool:
        """Validate task priority"""
        return priority.lower() in ["low", "medium", "high", "critical"]
    
    @staticmethod
    def validate_status(status: str) -> bool:
        """Validate status"""
        return status.lower() in ["todo", "in_progress", "review", "done"]
    
    @staticmethod
    def validate_role(role: str) -> bool:
        """Validate user role"""
        return role.lower() in ["admin", "project_manager", "developer", "viewer"]
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize input string"""
        return text.strip()[:100]  # Limit length