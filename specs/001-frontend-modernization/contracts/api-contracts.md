# API Contracts: Frontend Modernization

## Overview
This frontend modernization feature does not modify any existing API contracts. All backend API endpoints and request/response schemas remain unchanged.

## Unchanged Endpoints

### Task Management
- `POST /api/tasks` - Create a new task
- `GET /api/tasks` - Retrieve user's tasks
- `GET /api/tasks/:taskId` - Retrieve specific task
- `PUT /api/tasks/:taskId` - Update a task
- `DELETE /api/tasks/:taskId` - Delete a task
- `PATCH /api/tasks/:taskId/complete` - Toggle task completion

### Authentication
- `POST /api/auth/sign-in` - User sign-in
- `POST /api/auth/sign-up` - User sign-up
- `GET /api/auth/me` - Get current user info

## Request/Response Schemas
All request and response schemas remain identical to the existing implementation. The frontend modernization only affects UI/UX presentation, not data structures.

## Headers
All required headers (Authorization: Bearer <token>) remain unchanged.

## Error Handling
All existing error response formats and status codes remain unchanged.