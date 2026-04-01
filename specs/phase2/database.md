# Database Schema – Phase 2

## Table: users
- id (string, primary key)
- email (string, unique)
- created_at (timestamp)

## Table: tasks
- id (integer, primary key)
- user_id (string, foreign key -> users.id)
- title (string)
- description (text)
- completed (boolean)
- created_at (timestamp)
