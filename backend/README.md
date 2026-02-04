# FastAPI Better-Auth Backend

FastAPI backend with Better-Auth JWT integration for authentication, role-based access control, and user management.

## Features

- **JWT Authentication**: Validates tokens from Better-Auth via JWKS endpoint
- **Role-Based Access Control**: Admin and user roles with protected endpoints
- **User Management**: CRUD operations, role assignment, ban/unban functionality
- **Session Management**: List and revoke active sessions
- **OAuth Account Support**: View linked OAuth providers (Google, GitHub)
- **Async Throughout**: Built on async SQLAlchemy for optimal performance with Neon PostgreSQL

## Tech Stack

- **Python 3.11+**
- **FastAPI 0.109+**: Modern async web framework
- **SQLAlchemy 2.0+**: Async ORM with native async support
- **asyncpg**: Async PostgreSQL driver
- **python-jose**: JWT verification with JWKS support
- **httpx**: Async HTTP client for JWKS fetching
- **Pydantic v2**: Data validation and settings management
- **Alembic**: Database migrations

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   Frontend      │         │   Better-Auth   │
│   (Next.js)     │────────▶│   (Node.js)     │
└────────┬────────┘         └────────┬────────┘
         │ JWT Token                 │ JWKS
         ▼                           ▼
┌─────────────────────────────────────────────┐
│              FastAPI Backend                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────────┐ │
│  │ Auth    │  │ Users   │  │ Sessions    │ │
│  │ Router  │  │ Router  │  │ Service     │ │
│  └────┬────┘  └────┬────┘  └──────┬──────┘ │
│       └────────────┴───────────────┘        │
│                     │                        │
│              ┌──────┴──────┐                │
│              │  SQLAlchemy │                │
│              │   (Async)   │                │
│              └──────┬──────┘                │
└─────────────────────┼───────────────────────┘
                      ▼
         ┌────────────────────────┐
         │   Neon PostgreSQL      │
         │   (Shared Database)    │
         └────────────────────────┘
```

## Getting Started

### Prerequisites

- Python 3.11+
- Neon PostgreSQL database (or local PostgreSQL)
- Better-Auth server running (for authentication)

### Installation

```bash
# Clone and navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

### Environment Configuration

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Configure the following variables:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
DATABASE_URL_SYNC=postgresql://user:pass@host:5432/db

# Better-Auth
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret

# JWT
JWT_ALGORITHM=RS256  # or HS256 for shared secret
```

### Database Migrations

```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

### Running the Application

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

API available at: http://localhost:8000
- Docs: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/auth/session` | Get current session | Required |
| GET | `/api/v1/auth/me` | Get current user | Required |
| GET | `/api/v1/auth/accounts` | Get linked OAuth accounts | Required |
| POST | `/api/v1/auth/verify` | Verify token validity | Required |

### User Management

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/users` | List all users | Admin |
| GET | `/api/v1/users/{id}` | Get user by ID | Admin/Self |
| PATCH | `/api/v1/users/{id}` | Update user profile | Admin/Self |
| PUT | `/api/v1/users/{id}/role` | Update user role | Admin |
| POST | `/api/v1/users/{id}/ban` | Ban user | Admin |
| DELETE | `/api/v1/users/{id}/ban` | Unban user | Admin |

### Session Management

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/users/{id}/sessions` | List user sessions | Admin/Self |
| DELETE | `/api/v1/users/{id}/sessions` | Revoke all sessions | Admin/Self |
| DELETE | `/api/v1/users/{id}/sessions/{sid}` | Revoke session | Admin/Self |

### Health Checks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Basic health check |
| GET | `/health/db` | Database connectivity |

## Project Structure

```
backend/
├── app/                      # New application package
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Pydantic settings
│   ├── database.py          # Async SQLAlchemy
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py          # Better-Auth compatible
│   │   ├── session.py
│   │   ├── account.py
│   │   └── verification.py
│   ├── routers/             # API endpoints
│   │   ├── auth.py
│   │   └── users.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── user.py
│   │   ├── session.py
│   │   └── common.py
│   ├── services/            # Business logic
│   │   ├── auth.py          # JWT/JWKS verification
│   │   ├── user.py
│   │   ├── session.py
│   │   └── account.py
│   └── utils/
│       ├── dependencies.py  # Auth dependencies
│       └── exceptions.py    # Error handlers
├── alembic/                 # Database migrations
├── tests/                   # Test suite
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=term-missing

# Specific test file
pytest tests/test_auth.py -v
```

## Docker

```bash
# Build image
docker build -t fastapi-backend .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f api
```

## Security

- JWT tokens verified via JWKS (RS256) or shared secret (HS256)
- Role-based access control (admin/user)
- User ban/unban with expiration support
- Session management with revocation
- CORS configured for allowed origins
- No hardcoded secrets (environment variables only)

## License

MIT
