# Quickstart: FastAPI Better-Auth Backend

**Feature Branch**: `003-fastapi-better-auth`
**Date**: 2026-02-03

## Prerequisites

- Python 3.11+
- Node.js 18+ (for Better-Auth server)
- Docker & Docker Compose
- Neon PostgreSQL account (or local PostgreSQL)

## Architecture Overview

This project uses a **dual-service architecture**:

```
┌─────────────────────┐     ┌─────────────────────┐
│   Better-Auth       │     │    FastAPI          │
│   (Node.js)         │     │    (Python)         │
│   Port: 3000        │     │    Port: 8000       │
│                     │     │                     │
│   - Registration    │     │   - API Endpoints   │
│   - Login           │────▶│   - JWT Validation  │
│   - OAuth           │     │   - RBAC            │
│   - Session Mgmt    │     │   - Business Logic  │
└─────────────────────┘     └─────────────────────┘
          │                           │
          └───────────┬───────────────┘
                      ▼
             ┌─────────────────┐
             │ Neon PostgreSQL │
             │   (Shared DB)   │
             └─────────────────┘
```

## Quick Setup

### 1. Clone and Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create `.env` file in the `backend/` directory:

```env
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql+asyncpg://user:password@host/dbname?sslmode=require
DATABASE_URL_SYNC=postgresql://user:password@host/dbname?sslmode=require

# Better-Auth Configuration
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_JWKS_URL=http://localhost:3000/api/auth/jwks
BETTER_AUTH_SECRET=your-secret-key-min-32-chars

# JWT Configuration
JWT_ALGORITHM=RS256
JWT_ISSUER=http://localhost:3000

# Application
ENVIRONMENT=development
DEBUG=true
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# OAuth (Configure in Better-Auth, referenced here for docs)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

### 3. Database Setup

```bash
# Run migrations
alembic upgrade head

# Verify tables created
alembic current
```

### 4. Start the Server

**Development mode (with auto-reload):**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. Docker Setup (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f fastapi

# Stop services
docker-compose down
```

## API Documentation

Once running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Run async tests
pytest tests/ -v --asyncio-mode=auto
```

## Authentication Flow

### 1. User Registration (via Better-Auth)

Users register through the Better-Auth frontend SDK:

```typescript
// Frontend (Next.js/React)
import { authClient } from "./auth-client";

await authClient.signUp.email({
  email: "user@example.com",
  password: "securepassword123",
  name: "John Doe"
});
```

### 2. User Login (via Better-Auth)

```typescript
// Frontend
const session = await authClient.signIn.email({
  email: "user@example.com",
  password: "securepassword123"
});

// Get JWT token
const { token } = await authClient.getSession({
  fetchOptions: {
    onSuccess: (ctx) => {
      const jwt = ctx.response.headers.get("set-auth-jwt");
      // Use this JWT for FastAPI requests
    }
  }
});
```

### 3. API Requests (to FastAPI)

```typescript
// Frontend - Making authenticated API request
const response = await fetch("http://localhost:8000/api/v1/users/me", {
  headers: {
    "Authorization": `Bearer ${jwtToken}`,
    "Content-Type": "application/json"
  }
});
```

## Common Tasks

### Create Admin User

```python
# Run in Python shell or create a script
from app.database import get_session
from app.models.user import User
from sqlalchemy import update

async def promote_to_admin(email: str):
    async with get_session() as session:
        stmt = update(User).where(User.email == email).values(role="admin")
        await session.execute(stmt)
        await session.commit()
```

### Verify JWT Token (for debugging)

```python
from app.services.auth import verify_jwt_token

token = "eyJhbGciOiJSUzI1NiIs..."
payload = await verify_jwt_token(token)
print(payload)
# {'sub': 'user-id', 'email': 'user@example.com', 'role': 'user', ...}
```

## Troubleshooting

### JWKS Fetch Fails
- Verify Better-Auth is running on configured URL
- Check `BETTER_AUTH_JWKS_URL` in `.env`
- Ensure CORS allows requests between services

### Database Connection Issues
- Verify Neon PostgreSQL is accessible
- Check connection string format (asyncpg vs psycopg2)
- Ensure SSL mode is correct for Neon

### JWT Validation Errors
- Ensure JWT_ALGORITHM matches Better-Auth config
- Check token expiration
- Verify issuer matches BETTER_AUTH_URL

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Settings and configuration
│   ├── database.py          # Database connection
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── session.py
│   │   └── account.py
│   ├── routers/             # API endpoints
│   │   ├── auth.py
│   │   └── users.py
│   ├── schemas/             # Pydantic schemas
│   │   └── user.py
│   ├── services/            # Business logic
│   │   └── auth.py
│   └── utils/
│       └── dependencies.py  # FastAPI dependencies
├── alembic/                 # Database migrations
├── tests/                   # Test suite
├── .env.example
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```
