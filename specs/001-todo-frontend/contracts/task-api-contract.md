# API Contract: Task Management

## Base Path
`/api`

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Endpoints

### Create Task
- **Method**: `POST`
- **Path**: `/api/tasks`
- **Description**: Create a new task for the authenticated user
- **Request Headers**:
  - `Authorization: Bearer <jwt_token>`
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "title": "string (required, 1-200 chars)",
    "description": "string (optional, 0-1000 chars)",
    "due_datetime": "string (optional, ISO 8601 format)",
    "priority": "string (required, enum: urgent_important, urgent_not_important, not_urgent_important, not_urgent_not_important)"
  }
  ```
- **Success Response (201)**:
  ```json
  {
    "id": "string (UUID)",
    "title": "string",
    "description": "string",
    "due_datetime": "string (ISO 8601) or null",
    "priority": "string (enum)",
    "is_completed": "boolean (default: false)",
    "created_at": "string (ISO 8601)",
    "updated_at": "string (ISO 8601)",
    "user_id": "string"
  }
  ```
- **Error Responses**:
  - `401`: Unauthorized (invalid/missing JWT)
  - `422`: Validation error

### Get All Tasks
- **Method**: `GET`
- **Path**: `/api/tasks`
- **Description**: Retrieve all tasks for the authenticated user
- **Request Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Query Parameters**:
  - `priority`: Filter by priority level (optional)
  - `completed`: Filter by completion status (optional)
  - `sortBy`: Sort by field (created_at, updated_at, due_datetime, priority) (optional)
  - `sortOrder`: Sort order (asc, desc) (optional)
- **Success Response (200)**:
  ```json
  [
    {
      "id": "string (UUID)",
      "title": "string",
      "description": "string",
      "due_datetime": "string (ISO 8601) or null",
      "priority": "string (enum)",
      "is_completed": "boolean",
      "created_at": "string (ISO 8601)",
      "updated_at": "string (ISO 8601)",
      "user_id": "string"
    }
  ]
  ```
- **Error Responses**:
  - `401`: Unauthorized (invalid/missing JWT)

### Get Single Task
- **Method**: `GET`
- **Path**: `/api/tasks/{taskId}`
- **Description**: Retrieve a specific task for the authenticated user
- **Request Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Path Parameter**:
  - `taskId`: Task ID (UUID)
- **Success Response (200)**:
  ```json
  {
    "id": "string (UUID)",
    "title": "string",
    "description": "string",
    "due_datetime": "string (ISO 8601) or null",
    "priority": "string (enum)",
    "is_completed": "boolean",
    "created_at": "string (ISO 8601)",
    "updated_at": "string (ISO 8601)",
    "user_id": "string"
  }
  ```
- **Error Responses**:
  - `401`: Unauthorized (invalid/missing JWT)
  - `404`: Task not found

### Update Task
- **Method**: `PUT`
- **Path**: `/api/tasks/{taskId}`
- **Description**: Update an existing task for the authenticated user
- **Request Headers**:
  - `Authorization: Bearer <jwt_token>`
  - `Content-Type: application/json`
- **Path Parameter**:
  - `taskId`: Task ID (UUID)
- **Request Body**:
  ```json
  {
    "title": "string (required, 1-200 chars)",
    "description": "string (optional, 0-1000 chars)",
    "due_datetime": "string (optional, ISO 8601 format)",
    "priority": "string (required, enum: urgent_important, urgent_not_important, not_urgent_important, not_urgent_not_important)",
    "is_completed": "boolean"
  }
  ```
- **Success Response (200)**:
  ```json
  {
    "id": "string (UUID)",
    "title": "string",
    "description": "string",
    "due_datetime": "string (ISO 8601) or null",
    "priority": "string (enum)",
    "is_completed": "boolean",
    "created_at": "string (ISO 8601)",
    "updated_at": "string (ISO 8601)",
    "user_id": "string"
  }
  ```
- **Error Responses**:
  - `401`: Unauthorized (invalid/missing JWT)
  - `404`: Task not found
  - `422`: Validation error

### Delete Task
- **Method**: `DELETE`
- **Path**: `/api/tasks/{taskId}`
- **Description**: Delete a task for the authenticated user
- **Request Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Path Parameter**:
  - `taskId`: Task ID (UUID)
- **Success Response (204)**: No content
- **Error Responses**:
  - `401`: Unauthorized (invalid/missing JWT)
  - `404`: Task not found

### Toggle Task Completion
- **Method**: `PATCH`
- **Path**: `/api/tasks/{taskId}/complete`
- **Description**: Toggle the completion status of a task
- **Request Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Path Parameter**:
  - `taskId`: Task ID (UUID)
- **Request Body**:
  ```json
  {
    "is_completed": "boolean (optional, will toggle if not provided)"
  }
  ```
- **Success Response (200)**:
  ```json
  {
    "id": "string (UUID)",
    "title": "string",
    "description": "string",
    "due_datetime": "string (ISO 8601) or null",
    "priority": "string (enum)",
    "is_completed": "boolean",
    "created_at": "string (ISO 8601)",
    "updated_at": "string (ISO 8601)",
    "user_id": "string"
  }
  ```
- **Error Responses**:
  - `401`: Unauthorized (invalid/missing JWT)
  - `404`: Task not found

## Error Handling
- `401 Unauthorized`: Invalid or expired JWT token
- `404 Not Found`: Requested resource doesn't exist
- `422 Unprocessable Entity`: Validation error in request body
- `500 Internal Server Error`: Unexpected server error