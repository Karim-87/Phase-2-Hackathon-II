# Implementation Plan: FastAPI Better-Auth Backend

**Branch**: `003-fastapi-better-auth` | **Date**: 2026-02-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-fastapi-better-auth/spec.md`

## Summary

Implement a production-ready FastAPI backend integrated with Better-Auth for authentication. Better-Auth (TypeScript) serves as the authentication server handling registration, login, OAuth, and session management, while FastAPI validates JWT tokens and implements business logic with role-based access control (RBAC). Both services share a Neon PostgreSQL database with Better-Auth's schema.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.109+, SQLAlchemy 2.0+, python-jose[cryptography], httpx, Pydantic v2
**Storage**: Neon PostgreSQL (serverless, shared with Better-Auth)
**Testing**: pytest, pytest-asyncio, pytest-cov
**Target Platform**: Linux server (Docker), Windows development
**Project Type**: Web application (backend API only)
**Performance Goals**: 500ms p95 latency, 100 concurrent users
**Constraints**: JWT validation via JWKS, async throughout, Better-Auth schema compatibility
**Scale/Scope**: 10k users, single service deployment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Test-First | PENDING | Will implement pytest suite with async support |
| Library-First | PASS | Using established libraries (FastAPI, SQLAlchemy, python-jose) |
| Observability | PASS | Structured logging, health endpoints included |
| Simplicity | PASS | Single service pattern, standard REST API |
| Security | PASS | JWT verification, RBAC, environment-based secrets |

**Gate Status**: PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/003-fastapi-better-auth/
├── plan.md              # This file
├── research.md          # Phase 0 output - Better-Auth integration research
├── data-model.md        # Phase 1 output - Entity definitions
├── quickstart.md        # Phase 1 output - Developer guide
├── contracts/           # Phase 1 output - API specifications
│   └── openapi.yaml     # OpenAPI 3.1 specification
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Pydantic Settings configuration
│   ├── database.py          # Async SQLAlchemy engine and session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py          # SQLAlchemy Base class
│   │   ├── user.py          # User model (Better-Auth compatible)
│   │   ├── session.py       # Session model (Better-Auth compatible)
│   │   ├── account.py       # Account model (OAuth providers)
│   │   └── verification.py  # Verification tokens
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # Auth endpoints (JWT validation)
│   │   └── users.py         # User management endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # User Pydantic schemas
│   │   └── common.py        # Shared schemas (pagination, responses)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py          # JWT verification service
│   │   └── user.py          # User CRUD operations
│   └── utils/
│       ├── __init__.py
│       ├── dependencies.py  # FastAPI dependencies (auth, db)
│       └── exceptions.py    # Custom exception handlers
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/            # Migration files
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_auth.py         # Auth endpoint tests
│   ├── test_users.py        # User endpoint tests
│   └── test_services.py     # Service layer tests
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

**Structure Decision**: Backend-only API following user's specified structure with `backend/app/` layout. Models align with Better-Auth database schema for shared database compatibility.

## Complexity Tracking

| Aspect | Complexity | Justification |
|--------|------------|---------------|
| Dual-service architecture | Medium | Better-Auth is TypeScript-only; required for user requirement |
| JWT/JWKS verification | Low | Standard pattern with python-jose |
| Shared database | Low | Schema defined by Better-Auth, FastAPI reads |
| Async throughout | Medium | Required for performance with Neon PostgreSQL |

## Implementation Phases

### Phase 1: Core Infrastructure (P1 Priority)

**Objective**: Set up project structure, database connection, and configuration.

#### Tasks:
1. **Restructure backend directory** to match specified layout (`backend/app/`)
2. **Configure Pydantic Settings** with environment variable loading
3. **Set up async SQLAlchemy** with Neon PostgreSQL connection
4. **Create base models** following Better-Auth schema
5. **Set up Alembic** for async migrations
6. **Create FastAPI application** with CORS, middleware

#### Deliverables:
- `app/config.py` - Environment configuration
- `app/database.py` - Async database engine
- `app/models/*.py` - SQLAlchemy models
- `alembic/` - Migration configuration
- `app/main.py` - FastAPI application

### Phase 2: Authentication Layer (P1 Priority)

**Objective**: Implement JWT verification and authentication dependencies.

#### Tasks:
1. **Implement JWKS fetching** from Better-Auth with caching
2. **Create JWT verification service** using python-jose
3. **Build auth dependencies** (get_current_user, require_role)
4. **Add session validation** against database
5. **Implement rate limiting** on auth endpoints

#### Deliverables:
- `app/services/auth.py` - JWT verification
- `app/utils/dependencies.py` - FastAPI dependencies
- `app/routers/auth.py` - Auth endpoints

### Phase 3: User Management (P2 Priority)

**Objective**: Implement user CRUD and role management endpoints.

#### Tasks:
1. **Create user service** with CRUD operations
2. **Implement user endpoints** (list, get, update)
3. **Add role management** (admin only)
4. **Implement ban/unban** functionality
5. **Add session management** (list, revoke)

#### Deliverables:
- `app/services/user.py` - User business logic
- `app/routers/users.py` - User endpoints
- `app/schemas/user.py` - Pydantic schemas

### Phase 4: Testing & Documentation (P2 Priority)

**Objective**: Comprehensive test suite and developer documentation.

#### Tasks:
1. **Set up pytest** with async support and fixtures
2. **Write unit tests** for services
3. **Write integration tests** for endpoints
4. **Add API documentation** (OpenAPI, docstrings)
5. **Create developer quickstart** guide

#### Deliverables:
- `tests/` - Test suite with >80% coverage
- `README.md` - Project documentation
- `quickstart.md` - Developer guide

### Phase 5: Docker & DevOps (P3 Priority)

**Objective**: Containerization and local development environment.

#### Tasks:
1. **Create Dockerfile** for FastAPI
2. **Set up docker-compose** with all services
3. **Add health check endpoints**
4. **Configure logging** (structured, JSON format)

#### Deliverables:
- `Dockerfile` - Multi-stage build
- `docker-compose.yml` - Full stack setup
- Health endpoints

## Key Architecture Decisions

### 1. Better-Auth + FastAPI Integration Pattern

**Decision**: JWT-based API gateway with Better-Auth as auth server

**Rationale**:
- Better-Auth is TypeScript-only, no Python SDK available
- JWT verification via JWKS is a standard, well-supported pattern
- Separates authentication concerns from business logic
- Allows independent scaling of auth and API services

**Trade-offs**:
- Requires running two services (increased operational complexity)
- JWKS fetching adds latency (mitigated by caching)
- Better-Auth manages user registration, FastAPI cannot modify auth flows

### 2. Shared Database Architecture

**Decision**: Better-Auth and FastAPI share the same Neon PostgreSQL database

**Rationale**:
- Eliminates data synchronization issues
- FastAPI can read user/session data for RBAC
- Single source of truth for user state

**Trade-offs**:
- Schema must match Better-Auth expectations exactly
- Migration conflicts possible if both services modify schema

### 3. Async-First Design

**Decision**: Use async/await throughout the codebase

**Rationale**:
- Neon PostgreSQL serverless benefits from async connections
- FastAPI is optimized for async operations
- Better handling of concurrent requests

**Trade-offs**:
- All libraries must support async
- More complex testing setup

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Better-Auth schema changes | Pin Better-Auth version, monitor releases |
| JWKS endpoint unavailable | Implement fallback caching, circuit breaker |
| Database connection limits | Use connection pooling, Neon's built-in pooling |
| Token expiration edge cases | Implement proper refresh token handling guidance |

## Dependencies

### External Services
- **Better-Auth Server**: Must be running for auth operations
- **Neon PostgreSQL**: Database must be accessible
- **OAuth Providers**: Google, GitHub apps configured in Better-Auth

### Python Packages
```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sqlalchemy[asyncio]>=2.0.25
asyncpg>=0.29.0
python-jose[cryptography]>=3.3.0
httpx>=0.26.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
alembic>=1.13.0
python-dotenv>=1.0.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
pytest-cov>=4.1.0
```

## Success Metrics

| Metric | Target | Validation Method |
|--------|--------|-------------------|
| API Response Time | p95 < 500ms | Load testing with locust |
| Test Coverage | > 80% | pytest-cov report |
| Auth Success Rate | > 99% | Monitoring, error tracking |
| JWT Validation Time | < 50ms | Performance tests |

## Next Steps

1. **Run `/sp.tasks`** to generate detailed task breakdown
2. **Review ADR suggestions** from research phase
3. **Set up Better-Auth server** (separate TypeScript project)
4. **Begin Phase 1** implementation

---

## Appendix: Related Documents

- [Research](./research.md) - Better-Auth integration research
- [Data Model](./data-model.md) - Entity definitions and schema
- [API Contracts](./contracts/openapi.yaml) - OpenAPI specification
- [Quickstart](./quickstart.md) - Developer guide
