# Quickstart Guide: Backend Hardening & Modernization

## Prerequisites

- Python 3.11+
- PostgreSQL database (Neon recommended for production)
- Poetry or pip for dependency management
- Environment variables configured (see .env.example)

## Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd backend
```

### 2. Install Dependencies
Using Poetry (recommended):
```bash
poetry install
poetry shell
```

Or using pip:
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy the example environment file:
```bash
cp .env.example .env
```

Configure the following required variables in `.env`:
```env
NEON_DATABASE_URL=postgresql://username:password@host:port/database_name
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
ENVIRONMENT=development  # or "production"
```

### 4. Initialize Database and Migrations
```bash
# Create initial migration if this is the first time
alembic revision --autogenerate -m "Initial migration"

# Apply all migrations to the database
alembic upgrade head
```

## Running the Application

### Development
```bash
# Using uvicorn directly
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or using the run script if available
python -m src.main
```

### Production
```bash
# Using uvicorn with production settings
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4

# Or using gunicorn (if installed)
gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Endpoints

### Health Checks
- `GET /health` - Basic health check
- `GET /health/db` - Database connectivity check
- `GET /health/auth` - Authentication system check

### Task Management (requires authentication)
- `POST /api/tasks` - Create new task
- `GET /api/tasks` - List tasks with filters
- `GET /api/tasks/{task_id}` - Get specific task
- `PUT /api/tasks/{task_id}` - Update task
- `PATCH /api/tasks/{task_id}/complete` - Toggle task completion
- `DELETE /api/tasks/{task_id}` - Delete task

### Authentication
- `POST /api/auth/login` - Login and get JWT tokens
- `POST /api/auth/refresh` - Refresh access token using refresh token
- `POST /api/auth/logout` - Revoke refresh token

## Environment Variables

Required:
- `NEON_DATABASE_URL` - PostgreSQL database connection string
- `BETTER_AUTH_SECRET` - Secret key for JWT signing/verification
- `JWT_ALGORITHM` - Algorithm for JWT (default: HS256)

Optional:
- `ENVIRONMENT` - Environment name (default: development)
- `JWT_EXPIRATION_DELTA_HOURS` - Hours until JWT expiration (default: 24)
- `ALLOWED_ORIGINS` - Comma-separated list of allowed origins for CORS (default: http://localhost:3000,http://127.0.0.1:3000)

## Running Migrations

### Create New Migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Last Migration
```bash
alembic downgrade -1
```

## Testing

Run the test suite:
```bash
pytest
```

Run specific tests:
```bash
pytest tests/test_api.py
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Verify `NEON_DATABASE_URL` is correctly set
   - Ensure PostgreSQL server is running and accessible
   - Check firewall settings if connecting remotely

2. **JWT Authentication Issues**:
   - Verify `BETTER_AUTH_SECRET` is set and not empty
   - Ensure frontend sends Authorization header with Bearer token

3. **Migration Failures**:
   - Run `alembic current` to check current migration state
   - Check migration files for syntax errors
   - Ensure database is accessible

### Environment Validation
The application validates required environment variables on startup and fails gracefully with clear error messages if any required variables are missing.

## Security Best Practices

- Store `BETTER_AUTH_SECRET` securely, never commit to version control
- Use strong, randomly generated secrets
- Rotate JWT secrets periodically in production
- Monitor authentication endpoints for suspicious activity
- Use HTTPS in production environments