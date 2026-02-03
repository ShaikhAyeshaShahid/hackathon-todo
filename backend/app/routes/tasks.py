from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import Task, TaskCreate, TaskUpdate, User
from .auth import get_current_user


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[Task])
def read_tasks(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    statement = select(Task).where(Task.user_id == current_user.id)
    return session.exec(statement).all()


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_input: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    new_task = Task(
        title=task_input.title,
        description=task_input.description,
        user_id=current_user.id,
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@router.put("/{id}", response_model=Task)
def update_task(
    id: int,
    task_input: TaskUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    db_task = session.get(Task, id)
    if not db_task or db_task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_input.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.patch("/{id}/complete", response_model=Task)
def toggle_task_complete(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    db_task = session.get(Task, id)
    if not db_task or db_task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.completed = not db_task.completed
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    db_task = session.get(Task, id)
    if not db_task or db_task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(db_task)
    session.commit()
    return None
