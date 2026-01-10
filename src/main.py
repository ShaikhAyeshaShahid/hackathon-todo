"""
Task Management System - Phase 1: Task CRUD
This module implements the main application loop, 'Add Task', 'List Tasks', 
'Update Task', 'Delete Task', and 'Toggle Task Status' functionality.
"""

import sys

class TaskApplication:
    """Main application class handling the CLI loop and task storage."""

    def __init__(self):
        self.running = True
        # In-memory storage for tasks
        self.tasks = []
        # Counter for auto-generating unique task IDs
        self.next_id = 1

    def display_menu(self):
        """Prints the available commands to the console."""
        print("\n--- Task Management System ---")
        print("1. List Tasks")
        print("2. Add Task")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete/Incomplete")
        print("6. Exit")
        print("------------------------------")

    def handle_list_tasks(self):
        """
        Implements TASK T-003: List Tasks.
        Displays all tasks in the system with their ID, title, and status.
        """
        if not self.tasks:
            print("\n[Info] No tasks found. Your task list is currently empty.")
            return

        print("\n--- Current Tasks ---")
        # Formatting headers for a clean table-like view
        print(f"{'ID':<5} | {'Title':<25} | {'Status':<10}")
        print("-" * 45)
        
        for task in self.tasks:
            task_id = task.get("id")
            title = task.get("title")
            status = task.get("status", "Pending")
            
            # Truncate title if it is too long for the display table
            display_title = (title[:22] + '...') if len(title) > 25 else title
            
            print(f"{task_id:<5} | {display_title:<25} | {status:<10}")

    def handle_add_task(self):
        """
        Implements TASK T-002: Add Task.
        Collects title and description from the user and stores the task.
        """
        print("\n--- Add New Task ---")
        
        # Title is required
        title = ""
        while not title:
            title = input("Enter task title (required): ").strip()
            if not title:
                print("[Error] Title cannot be empty.")

        # Description is optional
        description = input("Enter task description (optional): ").strip()

        # Create task object with default "Pending" status
        new_task = {
            "id": self.next_id,
            "title": title,
            "description": description,
            "status": "Pending"
        }

        # Store task and increment ID counter
        self.tasks.append(new_task)
        print(f"\n[Success] Task added successfully with ID: {self.next_id}")
        self.next_id += 1

    def handle_update_task(self):
        """
        Implements TASK T-004: Update Task.
        Finds a task by ID and allows updating its title and/or description.
        """
        if not self.tasks:
            print("\n[Error] No tasks available to update.")
            return

        try:
            task_id_input = input("\nEnter the ID of the task to update: ").strip()
            task_id = int(task_id_input)
        except ValueError:
            print(f"[Error] '{task_id_input}' is not a valid numeric ID.")
            return

        # Find the task in the list
        task_to_update = next((t for t in self.tasks if t["id"] == task_id), None)

        if not task_to_update:
            print(f"[Error] Task with ID {task_id} not found.")
            return

        print(f"\nUpdating Task ID: {task_id}")
        print("Leave blank and press Enter to keep the current value.")

        # Update Title
        new_title = input(f"New title [{task_to_update['title']}]: ").strip()
        if new_title:
            task_to_update["title"] = new_title

        # Update Description
        new_description = input(f"New description [{task_to_update['description']}]: ").strip()
        if new_description:
            task_to_update["description"] = new_description

        print(f"\n[Success] Task {task_id} updated successfully.")

    def handle_delete_task(self):
        """
        Implements TASK T-005: Delete Task.
        Finds a task by ID and removes it from the list.
        """
        if not self.tasks:
            print("\n[Error] No tasks available to delete.")
            return

        try:
            task_id_input = input("\nEnter the ID of the task to delete: ").strip()
            task_id = int(task_id_input)
        except ValueError:
            print(f"[Error] '{task_id_input}' is not a valid numeric ID.")
            return

        # Find the index of the task to delete
        task_index = -1
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                task_index = i
                break

        if task_index == -1:
            print(f"[Error] Task with ID {task_id} not found.")
            return

        # Remove task from memory
        self.tasks.pop(task_index)
        print(f"\n[Success] Task {task_id} deleted successfully.")

    def handle_toggle_task_status(self):
        """
        Implements TASK T-006: Mark Task Complete / Incomplete.
        Finds a task by ID and toggles its status between 'Pending' and 'Completed'.
        """
        if not self.tasks:
            print("\n[Error] No tasks available.")
            return

        try:
            task_id_input = input("\nEnter the ID of the task to toggle status: ").strip()
            task_id = int(task_id_input)
        except ValueError:
            print(f"[Error] '{task_id_input}' is not a valid numeric ID.")
            return

        # Find the task in the list
        task = next((t for t in self.tasks if t["id"] == task_id), None)

        if not task:
            print(f"[Error] Task with ID {task_id} not found.")
            return

        # Toggle status
        if task["status"] == "Completed":
            task["status"] = "Pending"
        else:
            task["status"] = "Completed"

        print(f"\n[Success] Task {task_id} status updated to: {task['status']}")

    def handle_exit(self):
        """Gracefully shuts down the application."""
        print("\nExiting application. Goodbye!")
        self.running = False

    def run(self):
        """Main application loop."""
        while self.running:
            self.display_menu()
            choice = input("Select an option (1-6): ").strip()

            if choice == "1":
                self.handle_list_tasks()
            elif choice == "2":
                self.handle_add_task()
            elif choice == "3":
                self.handle_update_task()
            elif choice == "4":
                self.handle_delete_task()
            elif choice == "5":
                self.handle_toggle_task_status()
            elif choice == "6":
                self.handle_exit()
            else:
                print(f"\n[Error] '{choice}' is not a valid option. Please try again.")

def main():
    """Entry point of the script."""
    app = TaskApplication()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()