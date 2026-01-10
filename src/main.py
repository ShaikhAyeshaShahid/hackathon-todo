tasks = []
next_id = 1

def display_menu():
    """Prints the main menu options to the console."""
    print("\n--- Todo Application Menu ---")
    print("1. Add Task (add)")
    print("2. List Tasks (list)")
    print("3. Update Task (update)")
    print("4. Delete Task (delete)")
    print("5. Complete Task (complete)")
    print("6. Exit (exit)")
    print("---------------------------")

def find_task_by_id(task_id):
    """Finds a task by its ID."""
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

def add_task():
    """Prompts the user for task details and adds a new task."""
    global next_id
    title = input("Enter task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return

    description = input("Enter task description (optional): ").strip()

    new_task = {
        'id': next_id,
        'title': title,
        'description': description if description else None,
        'completed': False
    }
    tasks.append(new_task)
    next_id += 1
    print(f"Task '{title}' (ID: {new_task['id']}) added successfully.")

def list_tasks():
    """Displays all tasks, indicating completed ones."""
    if not tasks:
        print("No tasks found.")
        return

    print("\n--- Your Tasks ---")
    for task in tasks:
        status = "✔" if task['completed'] else " "
        desc_display = f" - {task['description']}" if task['description'] else ""
        print(f"[{status}] ID: {task['id']} | Title: {task['title']}{desc_display}")
    print("------------------")

def update_task():
    """Allows the user to update the title or description of an existing task."""
    task_id_input = input("Enter the ID of the task to update: ").strip()
    if not task_id_input.isdigit():
        print("Invalid ID. Please enter a number.")
        return

    task_id = int(task_id_input)
    task = find_task_by_id(task_id)

    if task:
        print(f"Current Title: {task['title']}")
        print(f"Current Description: {task['description'] if task['description'] else '[None]'}")

        new_title = input("Enter new title (leave blank to keep current): ").strip()
        new_description = input("Enter new description (leave blank to keep current, type 'none' to clear): ").strip()

        if new_title:
            task['title'] = new_title

        if new_description.lower() == 'none':
            task['description'] = None
        elif new_description:
            task['description'] = new_description

        print(f"Task ID {task_id} updated successfully.")
    else:
        print(f"Task with ID {task_id} not found.")

def delete_task():
    """Removes a task by its ID."""
    task_id_input = input("Enter the ID of the task to delete: ").strip()
    if not task_id_input.isdigit():
        print("Invalid ID. Please enter a number.")
        return

    task_id = int(task_id_input)
    task_found = False
    global tasks
    # Recreate tasks list without the deleted task
    initial_task_count = len(tasks)
    tasks = [task for task in tasks if task['id'] != task_id]

    if len(tasks) < initial_task_count:
        print(f"Task with ID {task_id} deleted successfully.")
    else:
        print(f"Task with ID {task_id} not found.")

def complete_task():
    """Marks a task as completed by its ID."""
    task_id_input = input("Enter the ID of the task to complete: ").strip()
    if not task_id_input.isdigit():
        print("Invalid ID. Please enter a number.")
        return

    task_id = int(task_id_input)
    task = find_task_by_id(task_id)

    if task:
        task['completed'] = True
        print(f"Task '{task['title']}' (ID: {task_id}) marked as completed.")
    else:
        print(f"Task with ID {task_id} not found.")

def main():
    """Main function to run the Todo application."""
    while True:
        display_menu()
        choice = input("Enter your choice (command or number): ").strip().lower()

        if choice == 'add' or choice == '1':
            add_task()
        elif choice == 'list' or choice == '2':
            list_tasks()
        elif choice == 'update' or choice == '3':
            update_task()
        elif choice == 'delete' or choice == '4':
            delete_task()
        elif choice == 'complete' or choice == '5':
            complete_task()
        elif choice == 'exit' or choice == '6':
            print("Exiting Todo application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()