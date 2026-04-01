from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..database import get_session
from ..models import Task, TaskCreate, TaskUpdate, User
from .auth import get_current_user

router = APIRouter(tags=["Tasks"])

# 1. READ TASKS
@router.get("/{user_id}/tasks", response_model=List[Task])
def read_tasks(
    user_id: int, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    statement = select(Task).where(Task.user_id == current_user.id)
    return session.exec(statement).all()

# 2. CREATE TASK
@router.post("/{user_id}/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: int, 
    task_input: TaskCreate, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    new_task = Task(**task_input.model_dump(), user_id=current_user.id)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task

# 3. UPDATE TASK
@router.put("/{user_id}/tasks/{id}", response_model=Task)
def update_task(
    user_id: int,
    id: int,
    task_input: TaskUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    if user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_task = session.get(Task, id)
    if not db_task or db_task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_input.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

# 4. DELETE TASK
@router.delete("/{user_id}/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: int,
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    if user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_task = session.get(Task, id)
    if not db_task or db_task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(db_task)
    session.commit()
    return None

# 5. MARK COMPLETE
@router.patch("/{user_id}/tasks/{id}/complete", response_model=Task)
def toggle_task_complete(
    user_id: int,
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    if user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db_task = session.get(Task, id)
    if not db_task or db_task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.completed = not db_task.completed
    session.commit()
    session.refresh(db_task)
    return db_task