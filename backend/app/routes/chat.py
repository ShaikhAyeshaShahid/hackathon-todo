import os
import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

from ..database import get_session
from ..models import User, Conversation, Message
from ..routes.auth import get_current_user
from ..ai_tools import add_task_tool, list_tasks_tool, complete_task_tool, delete_task_tool

router = APIRouter(tags=["Chat"])

# 1. Setup Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Fallback for safety if env var is missing
    print("WARNING: GEMINI_API_KEY not found.")

genai.configure(api_key=api_key)

# 2. Tool Definitions for Gemini (Simple Functions)
# Hum "dummy" functions banate hain taake Gemini ko sirf parameters nazar ayain
# (Asal execution hum neeche manual karenge taake session inject kar saken)
def add_task(title: str, description: str = ""):
    """Add a new task to the user's todo list."""
    pass

def list_tasks(status: str = "all"):
    """List tasks. Status can be 'all', 'pending', or 'completed'."""
    pass

def complete_task(task_id: int):
    """Mark a task as completed by providing its ID."""
    pass

def delete_task(task_id: int):
    """Delete a task permanently by providing its ID."""
    pass

# Initialize Model with Tools
tools_list = [add_task, list_tasks, complete_task, delete_task]
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash', # Fast and Free
    tools=tools_list
)

class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None

@router.post("/chat")
def chat_endpoint(
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # --- A. Context Setup (Same as before) ---
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=current_user.id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # Save User Message
    session.add(Message(conversation_id=conversation.id, role="user", content=request.message))
    session.commit()

    # --- B. Build History for Gemini ---
    # Gemini requires specific history format: [{'role': 'user', 'parts': [...]}, ...]
    history_msgs = session.exec(
        select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at)
    ).all()

    gemini_history = []
    for m in history_msgs:
        role = "user" if m.role == "user" else "model"
        gemini_history.append({"role": role, "parts": [m.content]})

    # Start Chat Session
    chat_session = model.start_chat(history=gemini_history[:-1]) # Exclude last msg to send it freshly
    
    # --- C. Send Message to Gemini ---
    response = chat_session.send_message(request.message)
    
    final_text = "I couldn't process that."

    # --- D. Handle Tool Calls (The Agentic Part) ---
    # Gemini returns a "function_call" part if it wants to use a tool
    try:
        part = response.candidates[0].content.parts[0]
        
        if part.function_call:
            fc = part.function_call
            tool_name = fc.name
            args = fc.args
            
            tool_result = "Error: Unknown tool"
            
            # Execute Python Function manually
            if tool_name == "add_task":
                tool_result = add_task_tool(session, current_user.id, args.get("title"), args.get("description", ""))
            elif tool_name == "list_tasks":
                tool_result = list_tasks_tool(session, current_user.id, args.get("status", "all"))
            elif tool_name == "complete_task":
                tool_result = complete_task_tool(session, current_user.id, int(args.get("task_id")))
            elif tool_name == "delete_task":
                tool_result = delete_task_tool(session, current_user.id, int(args.get("task_id")))

            # Send result back to Gemini
            # We must send the result so Gemini can generate the natural language confirmation
            final_response = chat_session.send_message(
                content.Content(
                    parts=[content.Part(
                        function_response=content.FunctionResponse(
                            name=tool_name,
                            response={'result': tool_result}
                        )
                    )]
                )
            )
            final_text = final_response.text
        else:
            # No tool called, just normal text
            final_text = response.text

    except Exception as e:
        final_text = f"Something went wrong processing the AI response: {str(e)}"

    # --- E. Save Assistant Response ---
    session.add(Message(conversation_id=conversation.id, role="assistant", content=final_text))
    session.commit()

    return {
        "conversation_id": conversation.id,
        "response": final_text
    }