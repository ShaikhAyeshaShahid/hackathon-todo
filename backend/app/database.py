import os
from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Please set it in your environment variables.")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,     # checks connection before using it
    pool_recycle=1800,      # recycle every 30 mins
    pool_size=5,
    max_overflow=10,
    connect_args={
        # TCP keep-alives help prevent sudden drops
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    },
)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
