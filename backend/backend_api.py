from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from backend.auth import get_current_user
from backend.database import get_session
from backend.models import Task, User
from backend.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Task:
    """
    Creates a new task for the current authenticated user.
    """
    task = Task.model_validate(task_create, update={"owner_id": current_user.id})
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/", response_model=List[TaskRead])
def read_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> List[Task]:
    """
    Retrieves all tasks belonging to the current authenticated user.
    """
    tasks = session.exec(select(Task).where(Task.owner_id == current_user.id)).all()
    return tasks


@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Task:
    """
    Retrieves a single task by its ID, ensuring it belongs to the current user.
    """
    task = session.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.owner_id == current_user.id)
    ).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or not owned by user")
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Task:
    """
    Updates an existing task by its ID, ensuring it belongs to the current user.
    """
    task = session.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.owner_id == current_user.id)
    ).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or not owned by user")

    hero_data = task_update.model_dump(exclude_unset=True)
    task.sqlmodel_update(hero_data)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> None:
    """
    Deletes a task by its ID, ensuring it belongs to the current user.
    """
    task = session.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.owner_id == current_user.id)
    ).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or not owned by user")

    session.delete(task)
    session.commit()