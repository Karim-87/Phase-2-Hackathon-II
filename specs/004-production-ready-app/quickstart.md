# Quickstart: 004-production-ready-app

**Branch**: `004-production-ready-app`

## Prerequisites

- Python 3.11+
- Node.js 18+
- Access to Neon PostgreSQL instance (or local PostgreSQL for development)
- Git

## Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
pip install passlib[bcrypt]  # NEW: for bcrypt password hashing

# Copy environment file
cp .env.example .env
# Edit .env with your Neon database URL and secrets

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --port 8001
```

## Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file (if not exists)
# Ensure .env has:
#   NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
#   BETTER_AUTH_SECRET=<your-secret>

# Start development server
npm run dev
```

## Environment Variables

### Backend (.env)
```
NEON_DATABASE_URL=postgresql+asyncpg://user:password@host/dbname
BETTER_AUTH_SECRET=<64-char-hex-secret>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DELTA_HOURS=24
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
DEBUG=true
```

### Frontend (.env)
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
BETTER_AUTH_SECRET=<same-secret-as-backend>
```

## Verification Steps

1. **Backend health**: `curl http://localhost:8001/health`
2. **Database health**: `curl http://localhost:8001/health/db`
3. **API docs**: Open `http://localhost:8001/api/v1/docs`
4. **Frontend**: Open `http://localhost:3000`
5. **Sign up**: Create account → verify redirect to dashboard
6. **Create task**: From dashboard → verify task appears in list
7. **Responsive**: Test at 375px, 768px, 1440px viewports

## Running Tests

```bash
# Backend tests
cd backend
pytest -v --cov=app tests/

# Type checking
mypy app/

# Linting
ruff check app/
```
