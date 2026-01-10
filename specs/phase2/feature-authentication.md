# Feature: Authentication – Phase 2

## User Stories
- User can sign up
- User can sign in
- User receives a JWT token after login
- User stays authenticated across requests

## Rules
- Authentication handled on frontend using Better Auth
- Backend verifies JWT token on every request
- Unauthorized requests must return 401
