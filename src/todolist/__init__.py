"""
ToDoList Package
A simple ToDo List application using Python OOP with In-Memory storage.

Features:
- Project management (create, edit, delete, list)
- Task management (add, update, delete, change status) 
- In-Memory storage with cascade delete
- Command Line Interface
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .models import Project, Task
from .services import ProjectService, TaskService
from .storage import InMemoryStorage
from .cli import ToDoListCLI, main

__all__ = [
    "Project", 
    "Task",
    "ProjectService", 
    "TaskService",
    "InMemoryStorage",
    "ToDoListCLI", 
    "main"
]
