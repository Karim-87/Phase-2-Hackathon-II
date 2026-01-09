# Quickstart Guide: Todo Backend API

**Date**: 2026-01-09
**Feature**: 001-todo-backend-api
**Related**: specs/001-todo-backend-api/spec.md

## Overview

Quickstart guide to set up, run, and test the Todo Backend API with JWT authentication and PostgreSQL integration.

## Prerequisites

- Python 3.11+
- uv (dependency manager)
- Neon Serverless PostgreSQL database
- Better Auth secret key

## Setup Steps

### 1. Clone and Navigate to Backend Directory
```bash
cd backend
```

### 2. Install Dependencies with uv
```bash
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt  # for development/testing
```

### 3. Environment Configuration
Create a `.env` file in the backend root directory:
```env
NEON_DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
BETTER_AUTH_SECRET=your-jwt-secret-key-here
ENVIRONMENT=development
```

### 4. Database Setup
```bash
# Run database migrations
alembic upgrade head
```

### 5. Run the Application
```bash
# Development mode
uv run python -m src.main

# Or using uvicorn directly
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token-here>
```

### Available Endpoints

1. **Create Task**
   ```
   POST /api/tasks
   Content-Type: application/json
   Authorization: Bearer <token>

   {
     "title": "Sample task",
     "description": "Task description",
     "due_datetime": "2023-12-31T23:59:59",
     "priority": "urgent_important"
   }
   ```

2. **Get All Tasks**
   ```
   GET /api/tasks
   Authorization: Bearer <token>
   ```

3. **Get Specific Task**
   ```
   GET /api/tasks/{taskId}
   Authorization: Bearer <token>
   ```

4. **Update Task**
   ```
   PUT /api/tasks/{taskId}
   Content-Type: application/json
   Authorization: Bearer <token>

   {
     "title": "Updated task title",
     "is_completed": true
   }
   ```

5. **Delete Task**
   ```
   DELETE /api/tasks/{taskId}
   Authorization: Bearer <token>
   ```

6. **Update Task Completion Status**
   ```
   PATCH /api/tasks/{taskId}/complete
   Content-Type: application/json
   Authorization: Bearer <token>

   {
     "completed": true
   }
   ```

## Testing the API

### Unit Tests
```bash
# Run all unit tests
uv run pytest tests/unit/

# Run specific test file
uv run pytest tests/unit/test_models.py
```

### Integration Tests
```bash
# Run all integration tests
uv run pytest tests/integration/
```

### Contract Tests
```bash
# Run contract tests to verify API compliance
uv run pytest tests/contract/
```

## Configuration Details

### Environment Variables
- `NEON_DATABASE_URL`: Connection string for Neon Serverless PostgreSQL
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing/validation
- `ENVIRONMENT`: Set to 'development', 'staging', or 'production'

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Check current migration status
alembic current
```

## Docker Deployment (Optional)

### Build and Run with Docker
```bash
# Build the image
docker build -t todo-backend .

# Run the container
docker run -d -p 8000:8000 \
  -e NEON_DATABASE_URL="..." \
  -e BETTER_AUTH_SECRET="..." \
  todo-backend
```

### Docker Compose
```bash
# Start the full stack
docker-compose up -d
```

## Troubleshooting

### Common Issues

1. **JWT Validation Failures**
   - Ensure the `BETTER_AUTH_SECRET` matches between frontend and backend
   - Verify the token is properly formatted with "Bearer " prefix

2. **Database Connection Issues**
   - Check the `NEON_DATABASE_URL` format and accessibility
   - Ensure the database has been migrated with `alembic upgrade head`

3. **User Isolation Not Working**
   - Verify that user_id is being extracted correctly from JWT
   - Check that all queries are filtered by user_id

### Health Checks
- API health endpoint: `GET /health` (doesn't require authentication)
- Database connectivity: `GET /health/db`
- JWT validation: `GET /health/auth`

## Next Steps

1. Implement the API endpoints according to the specification
2. Set up proper logging and monitoring
3. Add rate limiting for API endpoints
4. Implement comprehensive error handling
5. Add API documentation with Swagger/OpenAPI