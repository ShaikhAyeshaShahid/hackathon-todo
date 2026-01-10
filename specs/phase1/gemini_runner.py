import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

prompt = """
You are an AI software engineer.

Read and strictly follow the following specifications:

1) Constitution: specs/phase1/constitution.md
2) Feature Spec: specs/phase1/feature-task-crud.md
3) Acceptance Criteria: specs/phase1/acceptance.md
4) Technical Plan: specs/phase1/plan.md

Implement ONLY the following task:

TASK: Create the basic console menu and main application loop.
- Do not implement task logic yet (add, update, delete).
- Show menu options based on defined commands.
- Use Python standard library only.
- Code must be clean and readable.

Return a complete Python file.
"""

response = model.generate_content(prompt)
print(response.text)
