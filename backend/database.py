from sqlmodel import create_engine, SQLModel, Session
from typing import Generator

# Database URL configuration
# For a production app, use environment variables (e.g., os.getenv("DATABASE_URL"))
DATABASE_URL = "sqlite:///./database.db"
# connect_args={"check_same_thread": False} is needed for SQLite to allow multiple threads
# to interact with the database, which FastAPI typically does.
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """
    Creates all database tables defined in SQLModel models.
    """
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.
    Yields a session and ensures it's closed afterwards.
    """
    with Session(engine) as session:
        yield session
