from typing import List, Optional
from sqlmodel import Session, select
from .models import Task, User

# Tool 1: Add Task
def add_task_tool(session: Session, user_id: int, title: str, description: str = "") -> str:
    """Creates a new task for the user."""
    new_task = Task(title=title, description=description, user_id=user_id)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return f"Task created successfully: ID {new_task.id} - {new_task.title}"

# Tool 2: List Tasks
def list_tasks_tool(session: Session, user_id: int, status: str = "all") -> str:
    """Lists tasks filtered by status ('pending', 'completed', 'all')."""
    query = select(Task).where(Task.user_id == user_id)
    
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)
        
    tasks = session.exec(query).all()
    
    if not tasks:
        return "You have no tasks in this category."
        
    result = "Here are your tasks:\n"
    for t in tasks:
        status_icon = "[x]" if t.completed else "[ ]"
        result += f"{t.id}. {status_icon} {t.title}\n"
    return result

# Tool 3: Complete Task
def complete_task_tool(session: Session, user_id: int, task_id: int) -> str:
    """Marks a task as completed."""
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return f"Task {task_id} not found."
    
    task.completed = True
    session.add(task)
    session.commit()
    return f"Task {task_id} marked as complete."

# Tool 4: Delete Task
def delete_task_tool(session: Session, user_id: int, task_id: int) -> str:
    """Deletes a task."""
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return f"Task {task_id} not found."
    
    session.delete(task)
    session.commit()
    return f"Task {task_id} deleted."