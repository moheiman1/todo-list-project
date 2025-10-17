"""
Business logic services for ToDoList application
"""
from typing import List, Optional
from .models import Project, Task
from .storage import InMemoryStorage


class ProjectService:
    """Project management service"""
    
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage
        self.max_projects = 10
    
    def create_project(self, name: str, description: str) -> Project:
        # Check project limit
        if self.storage.project_count() >= self.max_projects:
            raise ValueError(f"Cannot create more than {self.max_projects} projects")
        
        # Check for duplicate name
        if self.storage.get_project_by_name(name):
            raise ValueError(f"Project with name '{name}' already exists")
        
        project = Project(name, description)
        self.storage.add_project(project)
        return project
    
    def get_all_projects(self) -> List[Project]:
        return self.storage.get_all_projects()
    
    def get_project(self, project_id: int) -> Optional[Project]:
        return self.storage.get_project(project_id)
    
    def update_project(self, project_id: int, name: str, description: str) -> Project:
        project = self.storage.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        
        # Check for duplicate name (excluding current project)
        existing = self.storage.get_project_by_name(name)
        if existing and existing.id != project_id:
            raise ValueError(f"Project with name '{name}' already exists")
        
        project.update(name, description)
        self.storage.update_project(project)
        return project
    
    def delete_project(self, project_id: int):
        if not self.storage.get_project(project_id):
            raise ValueError("Project not found")
        self.storage.delete_project(project_id)


class TaskService:
    """Task management service"""
    
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage
        self.max_tasks_per_project = 50
    
    def create_task(self, project_id: int, title: str, description: str, deadline: Optional[str] = None) -> Task:
        # Check if project exists
        if not self.storage.get_project(project_id):
            raise ValueError("Project not found")
        
        # Check task limit for project
        if self.storage.task_count_in_project(project_id) >= self.max_tasks_per_project:
            raise ValueError(f"Cannot create more than {self.max_tasks_per_project} tasks in a project")
        
        task = Task(title, description, deadline)
        self.storage.add_task_to_project(project_id, task)
        return task
    
    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        if not self.storage.get_project(project_id):
            raise ValueError("Project not found")
        return self.storage.get_tasks_by_project(project_id)
    
    def get_task(self, task_id: int) -> Optional[Task]:
        return self.storage.get_task(task_id)
    
    def change_task_status(self, task_id: int, new_status: str) -> Task:
        task = self.storage.get_task(task_id)
        if not task:
            raise ValueError("Task not found")
        
        task.change_status(new_status)
        self.storage.update_task(task)
        return task
    
    def update_task(self, task_id: int, title: str, description: str, deadline: Optional[str], status: str) -> Task:
        task = self.storage.get_task(task_id)
        if not task:
            raise ValueError("Task not found")
        
        task.update(title, description, deadline, status)
        self.storage.update_task(task)
        return task
    
    def delete_task(self, task_id: int):
        if not self.storage.get_task(task_id):
            raise ValueError("Task not found")
        self.storage.delete_task(task_id)