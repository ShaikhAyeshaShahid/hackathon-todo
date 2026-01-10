from sqlmodel import create_engine, SQLModel, Session
from typing import Generator
from .config import settings
# Import all models to register them with SQLModel.metadata
from .models import Task, User 

engine = create_engine(settings.DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session