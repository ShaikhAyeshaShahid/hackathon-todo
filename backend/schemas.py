from typing import Optional
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    email: str
    password: str


class UserRead(SQLModel):
    id: int
    email: str


class TaskCreate(SQLModel):
    title: str


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class TaskRead(SQLModel):
    id: int
    title: str
    completed: bool
    owner_id: int
