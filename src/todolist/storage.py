"""
In-memory storage for ToDoList application
"""
from typing import Dict, List, Optional
from .models import Project, Task


class InMemoryStorage:
    """Simple in-memory storage"""
    
    def __init__(self):
        self.projects: Dict[int, Project] = {}
        self.tasks: Dict[int, Task] = {}
        self.project_tasks: Dict[int, List[int]] = {}  # project_id -> task_ids
    
    # Project methods
    def get_all_projects(self) -> List[Project]:
        return list(self.projects.values())
    
    def get_project(self, project_id: int) -> Optional[Project]:
        return self.projects.get(project_id)
    
    def get_project_by_name(self, name: str) -> Optional[Project]:
        for project in self.projects.values():
            if project.name == name:
                return project
        return None
    
    def add_project(self, project: Project):
        self.projects[project.id] = project
        self.project_tasks[project.id] = []
    
    def update_project(self, project: Project):
        if project.id not in self.projects:
            raise ValueError("Project not found")
        self.projects[project.id] = project
    
    def delete_project(self, project_id: int):
        """Delete project and all its tasks (Cascade Delete)"""
        if project_id in self.projects:
            # Delete all project tasks
            task_ids = self.project_tasks.get(project_id, [])
            for task_id in task_ids:
                if task_id in self.tasks:
                    del self.tasks[task_id]
            
            # Delete project
            del self.projects[project_id]
            del self.project_tasks[project_id]
    
    def project_count(self) -> int:
        return len(self.projects)
    
    # Task methods
    def get_task(self, task_id: int) -> Optional[Task]:
        return self.tasks.get(task_id)
    
    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        task_ids = self.project_tasks.get(project_id, [])
        return [self.tasks[task_id] for task_id in task_ids if task_id in self.tasks]
    
    def add_task_to_project(self, project_id: int, task: Task):
        if project_id not in self.projects:
            raise ValueError("Project not found")
        
        task.project_id = project_id
        self.tasks[task.id] = task
        self.project_tasks[project_id].append(task.id)
    
    def update_task(self, task: Task):
        if task.id not in self.tasks:
            raise ValueError("Task not found")
        self.tasks[task.id] = task
    
    def delete_task(self, task_id: int):
        if task_id in self.tasks:
            task = self.tasks[task_id]
            if task.project_id and task.project_id in self.project_tasks:
                # Remove task from project's task list
                self.project_tasks[task.project_id] = [
                    tid for tid in self.project_tasks[task.project_id] 
                    if tid != task_id
                ]
            del self.tasks[task_id]
    
    def task_count_in_project(self, project_id: int) -> int:
        return len(self.project_tasks.get(project_id, []))