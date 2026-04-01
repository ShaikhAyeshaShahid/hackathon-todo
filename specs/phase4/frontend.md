# Phase 4: Frontend UI

## Objective
Build a simple, responsive web interface for the AI Todo App.

## Tech Stack
- **Framework**: Next.js (App Router) or Pure HTML/JS (for simplicity)
- **Styling**: Tailwind CSS
- **State Management**: React Hooks

## Pages
1.  **Login/Register**: Simple form to get JWT token.
2.  **Dashboard**:
    -   **Left Panel**: Task List (Auto-updates).
    -   **Right Panel**: Chat Interface (User vs AI).

## Integration
-   Must connect to `http://localhost:8000/api`.
-   Must store `access_token` in localStorage.
-   Chat window appends messages and sends to `POST /api/chat`.