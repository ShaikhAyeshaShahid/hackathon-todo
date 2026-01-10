from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# =====================
# TASK MODELS
# =====================
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

# 👇 Request schema for CREATE
class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None

# 👇 Request schema for UPDATE
class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


# =====================
# USER MODELS
# =====================
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# 👇 AUTH REQUEST SCHEMAS
class UserCreate(SQLModel):
    email: str
    password: str

class UserLogin(SQLModel):
    email: str
    password: str
