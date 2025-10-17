"""
Command Line Interface for ToDoList application
"""
import sys
from .storage import InMemoryStorage
from .services import ProjectService, TaskService


class ToDoListCLI:
    """Simple CLI for the application"""
    
    def __init__(self):
        self.storage = InMemoryStorage()
        self.project_service = ProjectService(self.storage)
        self.task_service = TaskService(self.storage)
        self.running = True
    
    def display_menu(self):
        print("\n" + "="*50)
        print("🎯 ToDo List Application - CLI")
        print("="*50)
        print("1. 📋 Create Project")
        print("2. ✏️  Edit Project")
        print("3. 🗑️  Delete Project")
        print("4. 📂 List All Projects")
        print("5. ➕ Add Task to Project")
        print("6. 🔄 Change Task Status")
        print("7. ✏️  Edit Task")
        print("8. 🗑️  Delete Task")
        print("9. 📋 List Tasks in Project")
        print("0. ❌ Exit")
        print("="*50)
    
    def get_input(self, prompt):
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            sys.exit(0)
    
    def run(self):
        print("🚀 Welcome to ToDoList Application!")
        
        while self.running:
            self.display_menu()
            choice = self.get_input("\nEnter your choice: ")
            
            try:
                if choice == "1":
                    self.create_project()
                elif choice == "2":
                    self.edit_project()
                elif choice == "3":
                    self.delete_project()
                elif choice == "4":
                    self.list_projects()
                elif choice == "5":
                    self.add_task()
                elif choice == "6":
                    self.change_task_status()
                elif choice == "7":
                    self.edit_task()
                elif choice == "8":
                    self.delete_task()
                elif choice == "9":
                    self.list_tasks()
                elif choice == "0":
                    print("👋 Thank you!")
                    self.running = False
                else:
                    print("❌ Invalid choice!")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def create_project(self):
        print("\n--- Create Project ---")
        name = self.get_input("Project name: ")
        desc = self.get_input("Project description: ")
        
        project = self.project_service.create_project(name, desc)
        print(f"✅ Project '{project.name}' created!")
    
    def edit_project(self):
        print("\n--- Edit Project ---")
        self.list_projects()
        
        try:
            project_id = int(self.get_input("Project ID: "))
            name = self.get_input("New name: ")
            desc = self.get_input("New description: ")
            
            project = self.project_service.update_project(project_id, name, desc)
            print(f"✅ Project '{project.name}' updated!")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def delete_project(self):
        print("\n--- Delete Project ---")
        self.list_projects()
        
        try:
            project_id = int(self.get_input("Project ID: "))
            confirm = self.get_input("Are you sure? This will delete ALL tasks! (y/n): ")
            
            if confirm.lower() == 'y':
                self.project_service.delete_project(project_id)
                print("✅ Project deleted!")
            else:
                print("❌ Deletion cancelled.")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def list_projects(self):
        projects = self.project_service.get_all_projects()
        if not projects:
            print("📭 No projects found")
            return
        
        print("\n--- Your Projects ---")
        for project in projects:
            task_count = len(self.storage.get_tasks_by_project(project.id))
            print(f"ID: {project.id} | 📁 {project.name} | 📝 {project.description} | Tasks: {task_count}")
    
    def add_task(self):
        print("\n--- Add Task ---")
        self.list_projects()
        
        try:
            project_id = int(self.get_input("Project ID: "))
            title = self.get_input("Task title: ")
            desc = self.get_input("Task description: ")
            deadline = self.get_input("Deadline (YYYY-MM-DD, optional): ") or None
            
            task = self.task_service.create_task(project_id, title, desc, deadline)
            print(f"✅ Task '{task.title}' added!")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def change_task_status(self):
        print("\n--- Change Task Status ---")
        
        try:
            task_id = int(self.get_input("Task ID: "))
            print("Status options: todo, doing, done")
            status = self.get_input("New status: ")
            
            task = self.task_service.change_task_status(task_id, status)
            print(f"✅ Task '{task.title}' status changed to '{task.status}'!")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def edit_task(self):
        print("\n--- Edit Task ---")
        
        try:
            task_id = int(self.get_input("Task ID: "))
            title = self.get_input("New title: ")
            desc = self.get_input("New description: ")
            deadline = self.get_input("New deadline (optional): ") or None
            status = self.get_input("New status (todo/doing/done): ")
            
            task = self.task_service.update_task(task_id, title, desc, deadline, status)
            print(f"✅ Task '{task.title}' updated!")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def delete_task(self):
        print("\n--- Delete Task ---")
        
        try:
            task_id = int(self.get_input("Task ID: "))
            confirm = self.get_input("Are you sure? (y/n): ")
            
            if confirm.lower() == 'y':
                self.task_service.delete_task(task_id)
                print("✅ Task deleted!")
            else:
                print("❌ Deletion cancelled.")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def list_tasks(self):
        print("\n--- List Tasks ---")
        self.list_projects()
        
        try:
            project_id = int(self.get_input("Project ID: "))
            tasks = self.task_service.get_tasks_by_project(project_id)
            
            if not tasks:
                print("📭 No tasks found")
                return
            
            print(f"\n--- Project Tasks ---")
            for task in tasks:
                deadline_str = task.deadline if task.deadline else "No deadline"
                print(f"ID: {task.id} | 📌 {task.title} | 🎯 {task.status} | 📅 {deadline_str}")
                print(f"   📝 {task.description}")
        except ValueError as e:
            print(f"❌ Error: {e}")


def main():
    cli = ToDoListCLI()
    cli.run()


if __name__ == "__main__":
    main()