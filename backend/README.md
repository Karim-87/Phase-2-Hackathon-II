# Todo Backend API

Backend API for the Multi-User Todo Web Application with JWT authentication and PostgreSQL database.

## Features

- Secure RESTful API for task management
- JWT-based authentication with token validation
- User isolation - users can only access their own tasks
- Full CRUD operations for tasks
- Eisenhower Matrix priority system
- Filtering, sorting, and pagination for task lists
- Comprehensive error handling

## Tech Stack

- Python 3.11+
- FastAPI - Modern, fast web framework
- SQLModel - SQL databases with Python objects
- Neon Serverless PostgreSQL - Cloud PostgreSQL database
- PyJWT - JSON Web Token implementation
- uv - Python package installer and resolver

## Getting Started

### Prerequisites

- Python 3.11+
- uv package manager
- Access to Neon Serverless PostgreSQL database

### Installation

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies:

```bash
uv pip install -r requirements.txt
```

Or if you're using standard pip:

```bash
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the backend root directory:

```env
NEON_DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
BETTER_AUTH_SECRET=your-jwt-secret-key-here
ENVIRONMENT=development
```

### Running the Application

```bash
# Using uv
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or using uvicorn directly
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Endpoints

All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token-here>
```

### Available Endpoints

- `POST /api/tasks` - Create a new task
- `GET /api/tasks` - Get all tasks for the authenticated user
- `GET /api/tasks/{taskId}` - Get a specific task
- `PUT /api/tasks/{taskId}` - Update a task
- `DELETE /api/tasks/{taskId}` - Delete a task
- `PATCH /api/tasks/{taskId}/complete` - Update task completion status
- `GET /health` - Health check endpoint

## Security

- JWT token validation on every request
- User isolation through user_id derived from JWT
- Input validation using Pydantic schemas
- Protection against SQL injection through SQLModel ORM
- CORS configured for secure cross-origin requests

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app entry point
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # Configuration and environment variables
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py              # Base SQLModel class
│   │   └── task.py              # Task model with all required fields
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py              # Pydantic schemas for API requests/responses
│   │   └── auth.py              # Authentication-related schemas
│   ├── database/
│   │   ├── __init__.py
│   │   └── session.py           # Database session management
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt_handler.py       # JWT token creation/validation
│   │   └── dependencies.py      # Authentication dependency for endpoints
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py              # Dependency injection for API routes
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── tasks.py         # Task API routes (POST, GET, PUT, DELETE, PATCH)
│   └── utils/
│       ├── __init__.py
│       └── helpers.py           # Utility functions
├── tests/
├── alembic/
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── README.md
```

## Testing

Run unit tests:
```bash
pytest tests/unit/
```

Run integration tests:
```bash
pytest tests/integration/
```

Run all tests:
```bash
pytest
```

## Database Migrations

This project uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Check current migration status
alembic current
```