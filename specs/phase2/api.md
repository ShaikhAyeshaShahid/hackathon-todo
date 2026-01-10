# REST API Specification

## Authentication
- JWT-based authentication
- All endpoints require Authorization header

## Endpoints

POST /auth/register
POST /auth/login

GET /tasks
POST /tasks
PUT /tasks/{id}
DELETE /tasks/{id}
PATCH /tasks/{id}/complete
