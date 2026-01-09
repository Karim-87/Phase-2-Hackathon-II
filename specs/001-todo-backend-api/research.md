# Research: Todo Backend API Implementation

**Date**: 2026-01-09
**Feature**: 001-todo-backend-api
**Related**: specs/001-todo-backend-api/plan.md

## Overview

Research for implementing a secure FastAPI-based RESTful API for task management with JWT-based authentication and SQLModel ORM for Neon Serverless PostgreSQL.

## Technology Deep Dive

### FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. Key features:
- Fast: Very high performance, on par with NodeJS and Go
- Fast to code: Increase the speed of development features by 200% to 300%
- Fewer bugs: Reduce about 40% of human (developer) induced errors
- Intuitive: Great editor support. Completion everywhere. Less time debugging
- Easy: Designed to be easy to use and learn
- Short: Minimize code duplication
- Robust: Get production-ready code with automatic interactive documentation
- Standards-based: Based on (and fully compatible with) the open standards for APIs

### SQLModel

SQLModel is a library for interacting with SQL databases from Python code, with Python objects. It's designed to provide a simple, straightforward way to work with SQL databases, with a focus on type hints and a minimal, intuitive API.

Key features:
- SQLAlchemy integration: Built on top of SQLAlchemy
- Pydantic integration: Uses Pydantic for data validation
- Type hints: Fully typed for great editor support
- Designed for FastAPI: Works seamlessly with FastAPI

### Neon Serverless PostgreSQL

Neon is a serverless PostgreSQL, configured to scale to zero. It provides:
- Serverless architecture: Automatically scales compute separately from storage
- Branching: Create instant branches of your database
- Separated storage and compute: Store data separately from compute resources
- PostgreSQL compatibility: Full PostgreSQL compatibility

### JWT Authentication

JSON Web Tokens (JWT) are an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. For this implementation:
- Tokens will be signed with a secret key shared between backend and frontend
- User identity will be extracted from the token's payload
- All API endpoints will require a valid JWT token in the Authorization header

## Implementation Approach

### 1. Project Setup
- Use uv for dependency management
- Set up FastAPI application with proper configuration
- Configure environment variables for database URL and JWT secret

### 2. Database Models
- Create Task model with required fields (id, user_id, title, description, due_datetime, priority, is_completed, created_at, updated_at)
- Ensure user_id comes from JWT token, not request body
- Set up proper indexes for performance

### 3. Authentication System
- Implement JWT token validation dependency
- Create middleware to extract user_id from token
- Ensure all endpoints require authentication

### 4. API Endpoints
- POST /api/tasks: Create new task for authenticated user
- GET /api/tasks: Retrieve all tasks for authenticated user
- GET /api/tasks/{taskId}: Retrieve specific task for authenticated user
- PUT /api/tasks/{taskId}: Update task for authenticated user
- DELETE /api/tasks/{taskId}: Delete task for authenticated user
- PATCH /api/tasks/{taskId}/complete: Update completion status for authenticated user

### 5. Security Measures
- Validate JWT on every request
- Ensure user isolation by filtering by user_id from JWT
- Return 401 for invalid/missing tokens
- Return 404 for tasks that exist but belong to other users

## Security Considerations

### JWT Validation
- Verify token signature using the shared secret
- Check token expiration
- Extract user_id from claims and use for query filtering

### User Isolation
- Never accept user_id in URL parameters or request body
- Always use user_id from JWT for database queries
- Implement proper database query filtering

### Input Validation
- Use Pydantic schemas for request validation
- Sanitize and validate all inputs
- Prevent SQL injection through ORM usage

## Error Handling

### HTTP Status Codes
- 200: Successful GET, PUT, PATCH requests
- 201: Successful POST request
- 204: Successful DELETE request
- 400: Bad request (malformed JSON, validation errors)
- 401: Unauthorized (invalid/missing JWT)
- 404: Not found (resource doesn't exist or belongs to another user)
- 422: Unprocessable entity (validation errors)
- 500: Internal server error

## Performance Considerations

### Database Optimization
- Index user_id column for efficient filtering
- Use connection pooling for database connections
- Optimize queries to avoid N+1 problems

### API Optimization
- Implement pagination for GET /api/tasks
- Use async/await patterns throughout
- Cache JWT validation results if needed