# API Contract: Todo Backend API

**Date**: 2026-01-09
**Feature**: 001-todo-backend-api
**Related**: specs/001-todo-backend-api/spec.md

## Overview

This document defines the API contract for the Todo Backend API, specifying the endpoints, request/response formats, and authentication requirements.

## Base URL

`http://localhost:8000/api` (or appropriate domain in production)

## Authentication

All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

Invalid, missing, or expired tokens result in HTTP 401 Unauthorized responses.

## Common Response Formats

### Success Responses
```json
{
  "success": true,
  "data": { /* response data */ }
}
```

### Error Responses
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

## API Endpoints

### 1. Create Task
- **Endpoint**: `POST /api/tasks`
- **Authentication**: Required
- **Description**: Creates a new task for the authenticated user

**Request Body**:
```json
{
  "title": "String, required, max 255 characters",
  "description": "String, optional",
  "due_datetime": "ISO 8601 datetime string, optional",
  "priority": "String, required, one of: urgent_important, not_urgent_important, urgent_not_important, not_urgent_not_important",
  "is_completed": "Boolean, optional, default false"
}
```

**Success Response** (HTTP 201):
```json
{
  "success": true,
  "data": {
    "id": "UUID string",
    "user_id": "UUID string (from JWT)",
    "title": "String",
    "description": "String or null",
    "due_datetime": "ISO 8601 datetime string or null",
    "priority": "String",
    "is_completed": "Boolean",
    "created_at": "ISO 8601 datetime string",
    "updated_at": "ISO 8601 datetime string"
  }
}
```

**Error Responses**:
- 400: Bad Request (validation errors)
- 401: Unauthorized (invalid/missing JWT)
- 500: Internal Server Error

---

### 2. Get All Tasks
- **Endpoint**: `GET /api/tasks`
- **Authentication**: Required
- **Description**: Retrieves all tasks belonging to the authenticated user

**Query Parameters**:
- `limit`: Integer, optional, default 50, maximum 100
- `offset`: Integer, optional, default 0
- `priority`: String, optional, filter by priority level
- `completed`: Boolean, optional, filter by completion status
- `sort_by`: String, optional, default "created_at", options: created_at, updated_at, due_datetime, priority
- `sort_order`: String, optional, default "desc", options: asc, desc

**Success Response** (HTTP 200):
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": "UUID string",
        "user_id": "UUID string (from JWT)",
        "title": "String",
        "description": "String or null",
        "due_datetime": "ISO 8601 datetime string or null",
        "priority": "String",
        "is_completed": "Boolean",
        "created_at": "ISO 8601 datetime string",
        "updated_at": "ISO 8601 datetime string"
      }
    ],
    "total_count": "Integer",
    "limit": "Integer",
    "offset": "Integer"
  }
}
```

**Error Responses**:
- 401: Unauthorized (invalid/missing JWT)
- 500: Internal Server Error

---

### 3. Get Specific Task
- **Endpoint**: `GET /api/tasks/{taskId}`
- **Authentication**: Required
- **Description**: Retrieves a specific task belonging to the authenticated user

**Path Parameter**:
- `taskId`: UUID string, required

**Success Response** (HTTP 200):
```json
{
  "success": true,
  "data": {
    "id": "UUID string",
    "user_id": "UUID string (from JWT)",
    "title": "String",
    "description": "String or null",
    "due_datetime": "ISO 8601 datetime string or null",
    "priority": "String",
    "is_completed": "Boolean",
    "created_at": "ISO 8601 datetime string",
    "updated_at": "ISO 8601 datetime string"
  }
}
```

**Error Responses**:
- 401: Unauthorized (invalid/missing JWT)
- 404: Not Found (task doesn't exist OR belongs to another user)
- 500: Internal Server Error

---

### 4. Update Task
- **Endpoint**: `PUT /api/tasks/{taskId}`
- **Authentication**: Required
- **Description**: Updates an existing task belonging to the authenticated user

**Path Parameter**:
- `taskId`: UUID string, required

**Request Body**:
```json
{
  "title": "String, optional, max 255 characters",
  "description": "String, optional",
  "due_datetime": "ISO 8601 datetime string, optional",
  "priority": "String, optional, one of: urgent_important, not_urgent_important, urgent_not_important, not_urgent_not_important",
  "is_completed": "Boolean, optional"
}
```

**Success Response** (HTTP 200):
```json
{
  "success": true,
  "data": {
    "id": "UUID string",
    "user_id": "UUID string (from JWT)",
    "title": "String",
    "description": "String or null",
    "due_datetime": "ISO 8601 datetime string or null",
    "priority": "String",
    "is_completed": "Boolean",
    "created_at": "ISO 8601 datetime string",
    "updated_at": "ISO 8601 datetime string"
  }
}
```

**Error Responses**:
- 400: Bad Request (validation errors)
- 401: Unauthorized (invalid/missing JWT)
- 404: Not Found (task doesn't exist OR belongs to another user)
- 500: Internal Server Error

---

### 5. Delete Task
- **Endpoint**: `DELETE /api/tasks/{taskId}`
- **Authentication**: Required
- **Description**: Deletes a task belonging to the authenticated user

**Path Parameter**:
- `taskId`: UUID string, required

**Success Response** (HTTP 204):
```
No content returned
```

**Error Responses**:
- 401: Unauthorized (invalid/missing JWT)
- 404: Not Found (task doesn't exist OR belongs to another user)
- 500: Internal Server Error

---

### 6. Update Task Completion Status
- **Endpoint**: `PATCH /api/tasks/{taskId}/complete`
- **Authentication**: Required
- **Description**: Updates only the completion status of a task belonging to the authenticated user

**Path Parameter**:
- `taskId`: UUID string, required

**Request Body**:
```json
{
  "completed": "Boolean, required"
}
```

**Success Response** (HTTP 200):
```json
{
  "success": true,
  "data": {
    "id": "UUID string",
    "user_id": "UUID string (from JWT)",
    "title": "String",
    "description": "String or null",
    "due_datetime": "ISO 8601 datetime string or null",
    "priority": "String",
    "is_completed": "Boolean",
    "created_at": "ISO 8601 datetime string",
    "updated_at": "ISO 8601 datetime string"
  }
}
```

**Error Responses**:
- 400: Bad Request (validation errors)
- 401: Unauthorized (invalid/missing JWT)
- 404: Not Found (task doesn't exist OR belongs to another user)
- 500: Internal Server Error

## Security Requirements

1. **JWT Validation**: All endpoints require valid JWT token
2. **User Isolation**: Users can only access their own tasks
3. **Token Expiration**: Expired tokens result in 401 responses
4. **Privacy**: When a user attempts to access another user's task, return 404 instead of 403 to prevent user enumeration

## Data Validation

### Priority Enum
Valid values for priority field:
- `urgent_important` - Do First: Important and urgent tasks
- `not_urgent_important` - Schedule: Important but not urgent tasks
- `urgent_not_important` - Delegate: Urgent but not important tasks
- `not_urgent_not_important` - Eliminate: Neither urgent nor important tasks

### Field Length Limits
- Title: Maximum 255 characters
- Description: No specific limit (database TEXT type)

## Error Codes

- `INVALID_JWT_TOKEN`: JWT token is invalid, missing, or expired
- `TASK_NOT_FOUND`: Task doesn't exist or belongs to another user
- `VALIDATION_ERROR`: Request data fails validation
- `INTERNAL_ERROR`: Unexpected server error occurred
- `INSUFFICIENT_PERMISSIONS`: User doesn't have permission for the action