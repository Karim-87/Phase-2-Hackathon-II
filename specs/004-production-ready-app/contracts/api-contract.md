# API Contract: 004-production-ready-app

**Date**: 2026-02-08
**Base URL**: `{API_BASE_URL}/api/v1`
**Auth**: Bearer JWT token in `Authorization` header

## Common Response Envelope

All responses use a consistent envelope:

```json
// Success
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { ... }
}

// Error
{
  "success": false,
  "error": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE",
  "details": { ... }  // Optional field-level errors
}
```

## Authentication Endpoints

### POST /auth/signup

**Purpose**: Register a new user account (FR-001, FR-002)

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass1",
  "name": "John Doe"
}
```

**Validation**:
- `email`: required, valid email format, max 255 chars
- `password`: required, min 8 chars, 1 uppercase, 1 lowercase, 1 number
- `name`: optional, max 100 chars

**Response 201**:
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user_id": "01HRX...",
    "expires_at": "2026-02-09T12:00:00Z"
  }
}
```

**Error 400** (duplicate email):
```json
{
  "success": false,
  "error": "An account with this email already exists",
  "error_code": "EMAIL_EXISTS"
}
```

**Error 422** (validation):
```json
{
  "success": false,
  "error": "Validation failed",
  "error_code": "VALIDATION_ERROR",
  "details": {
    "password": "Password must be at least 8 characters with 1 uppercase, 1 lowercase, and 1 number"
  }
}
```

---

### POST /auth/signin

**Purpose**: Authenticate existing user (FR-003)

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass1"
}
```

**Validation**:
- `email`: required, valid email format
- `password`: required, non-empty

**Response 200**:
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user_id": "01HRX...",
    "expires_at": "2026-02-09T12:00:00Z"
  }
}
```

**Error 401** (bad credentials):
```json
{
  "success": false,
  "error": "Invalid email or password",
  "error_code": "INVALID_CREDENTIALS"
}
```

**Error 403** (banned):
```json
{
  "success": false,
  "error": "Account is banned",
  "error_code": "ACCOUNT_BANNED"
}
```

**Side effect**: If password is stored in legacy SHA-256 format, re-hash to bcrypt after successful verification.

---

### GET /auth/me

**Purpose**: Get current authenticated user profile

**Headers**: `Authorization: Bearer <token>`

**Response 200**:
```json
{
  "success": true,
  "data": {
    "id": "01HRX...",
    "email": "user@example.com",
    "email_verified": false,
    "name": "John Doe",
    "image": null,
    "role": "user",
    "created_at": "2026-02-08T10:00:00Z",
    "updated_at": "2026-02-08T10:00:00Z"
  }
}
```

**Error 401**: Invalid or expired token

---

### GET /auth/session

**Purpose**: Validate current session and return session info

**Headers**: `Authorization: Bearer <token>`

**Response 200**:
```json
{
  "success": true,
  "data": {
    "session": {
      "id": "sess_...",
      "expires_at": "2026-02-09T12:00:00Z"
    },
    "user": {
      "id": "01HRX...",
      "email": "user@example.com",
      "name": "John Doe",
      "role": "user"
    }
  }
}
```

**Error 401**: Invalid or expired token

---

## Task Endpoints (NEW)

All task endpoints require authentication and scope to the authenticated user.

### GET /tasks

**Purpose**: List authenticated user's tasks with optional filtering (FR-007, FR-008, FR-010)

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Default | Description |
| ----- | ---- | ------- | ----------- |
| priority | string | (all) | Filter by priority enum value |
| is_completed | boolean | (all) | Filter by completion status |
| sort_by | string | "created_at" | Sort field: created_at, updated_at, due_datetime, priority, title |
| sort_order | string | "desc" | "asc" or "desc" |
| limit | integer | 50 | Max items per page (1-100) |
| offset | integer | 0 | Pagination offset |

**Response 200**:
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": "task_01HRX...",
        "user_id": "01HRX...",
        "title": "Complete project report",
        "description": "Finish the Q4 report",
        "due_datetime": "2026-02-15T17:00:00Z",
        "priority": "urgent_important",
        "is_completed": false,
        "created_at": "2026-02-08T10:00:00Z",
        "updated_at": "2026-02-08T10:00:00Z"
      }
    ],
    "total_count": 25,
    "limit": 50,
    "offset": 0
  }
}
```

**Error 401**: Unauthenticated

---

### POST /tasks

**Purpose**: Create a new task (FR-007, FR-010)

**Headers**: `Authorization: Bearer <token>`

**Request**:
```json
{
  "title": "Complete project report",
  "description": "Finish the Q4 report",
  "due_datetime": "2026-02-15T17:00:00Z",
  "priority": "urgent_important"
}
```

**Validation**:
- `title`: required, max 255 chars, non-empty after trim
- `description`: optional, max 5000 chars
- `due_datetime`: optional, valid ISO 8601 datetime
- `priority`: required, one of: `urgent_important`, `not_urgent_important`, `urgent_not_important`, `not_urgent_not_important`

**Response 201**:
```json
{
  "success": true,
  "data": {
    "id": "task_01HRX...",
    "user_id": "01HRX...",
    "title": "Complete project report",
    "description": "Finish the Q4 report",
    "due_datetime": "2026-02-15T17:00:00Z",
    "priority": "urgent_important",
    "is_completed": false,
    "created_at": "2026-02-08T10:00:00Z",
    "updated_at": "2026-02-08T10:00:00Z"
  }
}
```

**Error 422**: Validation errors

---

### GET /tasks/{task_id}

**Purpose**: Get a single task by ID (FR-007, FR-010)

**Headers**: `Authorization: Bearer <token>`

**Response 200**: Single task object in data envelope

**Error 404**: Task not found or does not belong to user

---

### PATCH /tasks/{task_id}

**Purpose**: Update a task (FR-007, FR-010)

**Headers**: `Authorization: Bearer <token>`

**Request** (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "due_datetime": "2026-02-20T17:00:00Z",
  "priority": "not_urgent_important",
  "is_completed": true
}
```

**Response 200**: Updated task object in data envelope

**Error 404**: Task not found or does not belong to user
**Error 422**: Validation errors

---

### DELETE /tasks/{task_id}

**Purpose**: Delete a task (FR-007, FR-010)

**Headers**: `Authorization: Bearer <token>`

**Response 200**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

**Error 404**: Task not found or does not belong to user

---

## Error Codes Reference

| Code | HTTP Status | Description |
| ---- | ----------- | ----------- |
| EMAIL_EXISTS | 400 | Email already registered |
| VALIDATION_ERROR | 422 | Request validation failed |
| INVALID_CREDENTIALS | 401 | Wrong email or password |
| ACCOUNT_BANNED | 403 | User account is banned |
| TOKEN_EXPIRED | 401 | JWT token has expired |
| TOKEN_INVALID | 401 | JWT token is malformed or tampered |
| NOT_FOUND | 404 | Resource not found |
| FORBIDDEN | 403 | Insufficient permissions |
| SERVER_ERROR | 500 | Internal server error (details logged server-side only) |

## CORS Configuration

**Development**:
- Origins: `http://localhost:3000`, `http://127.0.0.1:3000`

**Production**:
- Origins: Set via `ALLOWED_ORIGINS` env var (must NOT contain localhost)
- Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
- Headers: Content-Type, Authorization, Accept, Origin, X-Requested-With
- Credentials: true
- Max-Age: 600s
