from fastapi import FastAPI
from .database import init_db
from .routes import tasks, auth

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(tasks.router)
app.include_router(auth.router)

@app.get("/health")
def health():
    return {"status": "ok"}
