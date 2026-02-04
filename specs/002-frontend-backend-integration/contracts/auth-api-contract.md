# Authentication API Contract

## Overview
RESTful API endpoints for user authentication and registration following JWT-based security patterns.

## Base URL
`/api/v1/auth`

## Endpoints

### POST /api/v1/auth/signup
Register a new user account.

#### Request
- **Method**: POST
- **Path**: `/api/v1/auth/signup`
- **Content-Type**: `application/json`

##### Request Body
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Fields**:
- `email` (string, required): User's email address
- `password` (string, required): User's password (min 8 characters recommended)
- `name` (string, optional): User's full name

#### Response
- **Success**: `201 Created`
- **Content-Type**: `application/json`

```json
{
  "success": true,
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input data
- `409 Conflict`: Email already exists

### POST /api/v1/auth/signin
Authenticate an existing user and return JWT token.

#### Request
- **Method**: POST
- **Path**: `/api/v1/auth/signin`
- **Content-Type**: `application/json`

##### Request Body
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Fields**:
- `email` (string, required): User's email address
- `password` (string, required): User's password

#### Response
- **Success**: `200 OK`
- **Content-Type**: `application/json`

```json
{
  "success": true,
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid credentials

### POST /api/v1/auth/signout
Invalidate the user's session (client-side only).

#### Request
- **Method**: POST
- **Path**: `/api/v1/auth/signout`
- **Headers**: `Authorization: Bearer <token>`

#### Response
- **Success**: `200 OK`
- **Content-Type**: `application/json`

```json
{
  "success": true,
  "message": "Successfully signed out"
}
```

### GET /api/v1/auth/me
Retrieve current user's profile information.

#### Request
- **Method**: GET
- **Path**: `/api/v1/auth/me`
- **Headers**: `Authorization: Bearer <token>`

#### Response
- **Success**: `200 OK`
- **Content-Type**: `application/json`

```json
{
  "success": true,
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2023-01-01T00:00:00Z"
  }
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing token

## Authentication Headers
All protected endpoints require the following header:
```
Authorization: Bearer <jwt_token>
```

## Common Response Format
All API responses follow this format:

```json
{
  "success": true/false,
  "data": {...}, // Optional - present on success
  "message": "..." // Optional - additional info
}
```

## Error Response Format
Error responses follow this format:

```json
{
  "success": false,
  "message": "Human-readable error message",
  "error_code": "ERROR_CODE" // Optional
}
```

## Security Requirements
- All authentication endpoints must use HTTPS in production
- Passwords must be hashed using BCrypt or similar
- JWT tokens must have appropriate expiration times
- Rate limiting should be applied to authentication endpoints