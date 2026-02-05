from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <--- 1. Import This
from .database import init_db
from .routes import tasks, auth, chat

app = FastAPI(title="Hackathon Todo API")

# 2. Add CORS Middleware (Ye security gate khol dega)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Frontend URL
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, etc)
    allow_headers=["*"], # Allow all headers
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(auth.router, prefix="/api/auth")
app.include_router(tasks.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}