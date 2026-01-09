# Data Model: Todo Frontend Application

## Task Entity

**Fields**:
- `id`: string (UUID) - Unique identifier for the task
- `title`: string (required) - Title of the task
- `description`: string (optional) - Detailed description of the task
- `due_datetime`: string (optional) - Due date and time in ISO format
- `priority`: string (required) - Priority level enum: "urgent_important", "urgent_not_important", "not_urgent_important", "not_urgent_not_important"
- `is_completed`: boolean (default: false) - Completion status of the task
- `created_at`: string - Creation timestamp in ISO format
- `updated_at`: string - Last update timestamp in ISO format
- `user_id`: string - Foreign key linking to the authenticated user

**Validation Rules**:
- Title must be 1-200 characters
- Description must be 0-1000 characters if provided
- Due datetime must be in valid ISO 8601 format if provided
- Priority must be one of the four allowed values
- User ID must match the authenticated user's ID for all operations

**State Transitions**:
- `is_completed` can transition from false to true (mark complete) or true to false (mark incomplete)
- All other fields can be modified when updating a task

## User Session Entity

**Fields**:
- `jwt_token`: string - JWT token for API authentication
- `user_id`: string - Current user's identifier
- `expires_at`: string - Token expiration timestamp
- `is_authenticated`: boolean - Authentication status

**Validation Rules**:
- JWT token must be present and valid for all API calls
- Token expiration must be checked before API requests
- User isolation must be maintained (user can only access their own data)

## API Response Format

**Success Response**:
```
{
  "success": true,
  "data": { /* entity data */ },
  "message": "optional message"
}
```

**Error Response**:
```
{
  "success": false,
  "error": {
    "code": "error_code",
    "message": "error message"
  }
}
```