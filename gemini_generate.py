from google import genai
from pathlib import Path
import os

# Configure client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Read spec files
base = Path("specs/phase1")

constitution = (base / "constitution.md").read_text(encoding="utf-8")
feature = (base / "feature-task-crud.md").read_text(encoding="utf-8")
acceptance = (base / "acceptance.md").read_text(encoding="utf-8")

# prompt = f"""
# You are an AI software developer.

# This project follows STRICT Spec-Driven Development.
# You must not invent features.

# ====================
# CONSTITUTION
# ====================
# {constitution}

# ====================
# FEATURE SPEC
# ====================
# {feature}

# ====================
# ACCEPTANCE CRITERIA
# ====================
# {acceptance}

# TASK:
# Generate a COMPLETE Python console-based Todo application.

# RULES:
# - Python standard library ONLY
# - Store tasks in memory only
# - NO files, NO database
# - Implement ONLY specified features
# - Output FULL runnable code
# - Output ONE file named main.py
# - Do NOT include explanations

# CRITICAL EXECUTION REQUIREMENTS:
# - The program MUST start running when executing: python main.py
# - You MUST include an interactive menu loop
# - You MUST print the menu to the console
# - You MUST accept user input using input()
# - You MUST include an entry point:
#   if __name__ == "__main__"
# - All logic must be reachable from the menu
# - Do NOT define unused functions


# Now generate the code.
# """

# prompt = f"""
# You are an AI backend engineer.

# Read and follow these specs strictly:

# - specs/phase2/constitution.md
# - specs/phase2/feature-task-crud.md
# - specs/phase2/api.md
# - specs/phase2/acceptance.md

# TASK:
# Generate a FastAPI backend application.

# REQUIREMENTS:
# - JWT authentication
# - CRUD APIs for tasks
# - PostgreSQL via SQLModel
# - Clear project structure
# - Database models and routes
# - Entry point must run with: uvicorn main:app

# OUTPUT:
# - Generate backend code only
# - Assume code lives in /backend
# - Do NOT include explanations



# ADDITIONAL REQUIREMENT (CRITICAL):

# You have referenced the following modules:
# - backend.auth
# - backend.database
# - backend.models
# - backend.schemas

# Generate COMPLETE code for EACH of these files.

# Output format MUST be:
# --- auth.py ---
# <code>

# --- database.py ---
# <code>

# --- models.py ---
# <code>

# --- schemas.py ---
# <code>

# Do NOT skip any referenced file.
# All imports must resolve correctly.

# """

prompt = f"""
You are a frontend engineer.

Read and follow these specifications strictly:

- specs/phase2/frontend.md
- specs/phase2/acceptance.md

TASK:
Generate a Next.js frontend application.

REQUIREMENTS:
- App Router
- Pages for login, register, and tasks
- Fetch API calls to FastAPI backend
- JWT token stored in localStorage
- Proper error handling
- No hardcoded data

OUTPUT:
- Generate frontend code only
- Assume code lives in /frontend/src
- Do NOT include explanations



CRITICAL AUTH FIX REQUIRED:

The backend fails to start due to a missing function.

You MUST generate a complete implementation for `backend/auth.py`
that includes at minimum:

- get_current_user dependency function
- JWT token extraction from Authorization header
- Token validation logic
- Return of the authenticated User object
- Compatibility with FastAPI Depends()

The function signature MUST be:

def get_current_user(...)

Do NOT leave this function undefined.
CRITICAL DATABASE FIX REQUIRED:

The backend fails to start because `get_session` is missing.

You MUST generate a complete implementation for `backend/database.py`
that includes:

- SQLModel engine creation
- SessionLocal / session factory
- get_session dependency function compatible with FastAPI Depends
- Proper session yield and close logic

The function signature MUST exist:

def get_session():

Do NOT leave this undefined.

"""


response = client.models.generate_content(
   model="models/gemini-2.5-flash",
    contents=prompt
)


print(response.text)


