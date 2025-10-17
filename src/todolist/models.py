"""
ToDoList Models Module
Contains Project and Task models with validation logic.
"""

from datetime import datetime
from typing import Optional

# Constants
MAX_PROJECT_NAME_LENGTH = 30
MAX_PROJECT_DESCRIPTION_LENGTH = 150
MAX_TASK_TITLE_LENGTH = 30
MAX_TASK_DESCRIPTION_LENGTH = 150
TASK_STATUSES = ["todo", "doing", "done"]
DEFAULT_TASK_STATUS = "todo"


class Project:
    """Project model"""
    
    def __init__(self, name: str, description: str):
        self._validate_name(name)
        self._validate_description(description)
        
        self.id = id(self)
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.tasks = []
    
    def _validate_name(self, name: str):
        if not name or not name.strip():
            raise ValueError("Project name cannot be empty")
        if len(name) > MAX_PROJECT_NAME_LENGTH:
            raise ValueError(f"Project name cannot exceed {MAX_PROJECT_NAME_LENGTH} characters")
    
    def _validate_description(self, description: str):
        if not description or not description.strip():
            raise ValueError("Project description cannot be empty")
        if len(description) > MAX_PROJECT_DESCRIPTION_LENGTH:
            raise ValueError(f"Project description cannot exceed {MAX_PROJECT_DESCRIPTION_LENGTH} characters")
    
    def update(self, name: str, description: str):
        self._validate_name(name)
        self._validate_description(description)
        self.name = name
        self.description = description
    
    def __str__(self):
        return f"Project: {self.name} (Tasks: {len(self.tasks)})"


class Task:
    """Task model"""
    
    def __init__(self, title: str, description: str, deadline: Optional[str] = None):
        self._validate_title(title)
        self._validate_description(description)
        self._validate_deadline(deadline)
        
        self.id = id(self)
        self.title = title
        self.description = description
        self.status = DEFAULT_TASK_STATUS
        self.created_at = datetime.now()
        self.deadline = deadline
        self.project_id = None
    
    def _validate_title(self, title: str):
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        if len(title) > MAX_TASK_TITLE_LENGTH:
            raise ValueError(f"Task title cannot exceed {MAX_TASK_TITLE_LENGTH} characters")
    
    def _validate_description(self, description: str):
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")
        if len(description) > MAX_TASK_DESCRIPTION_LENGTH:
            raise ValueError(f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters")
    
    def _validate_deadline(self, deadline: Optional[str]):
        if deadline:
            try:
                datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Deadline must be in YYYY-MM-DD format")
    
    def change_status(self, new_status: str):
        if new_status not in TASK_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(TASK_STATUSES)}")
        self.status = new_status
    
    def update(self, title: str, description: str, deadline: Optional[str], status: str):
        self._validate_title(title)
        self._validate_description(description)
        self._validate_deadline(deadline)
        
        if status not in TASK_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(TASK_STATUSES)}")
        
        self.title = title
        self.description = description
        self.deadline = deadline
        self.status = status
    
    def __str__(self):

        return f"Task: {self.title} ({self.status})"
