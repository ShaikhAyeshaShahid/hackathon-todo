from fastapi import FastAPI
from .database import init_db
from .routes import tasks, auth

app = FastAPI(title="Hackathon Todo API")

@app.on_event("startup")
def on_startup():
    init_db()

# Prefixes fixed:
app.include_router(auth.router, prefix="/api/auth") # Result: /api/auth/register
app.include_router(tasks.router, prefix="/api")     # Result: /api/{user_id}/tasks

@app.get("/health")
def health():
    return {"status": "ok"}