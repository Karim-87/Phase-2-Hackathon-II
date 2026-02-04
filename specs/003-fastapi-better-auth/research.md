# Research: FastAPI Backend with Better-Auth Integration

**Feature Branch**: `003-fastapi-better-auth`
**Date**: 2026-02-03
**Status**: Complete

## Executive Summary

Better-Auth is a **TypeScript-first** authentication framework that is NOT directly usable in Python/FastAPI. However, it can be integrated with a Python backend through its **JWT plugin** and **JWKS endpoints** for token verification. This document outlines the architectural approach for integrating Better-Auth with a FastAPI backend.

## Research Findings

### 1. Better-Auth Architecture Understanding

**Decision**: Use Better-Auth as the authentication server (TypeScript/Node.js) with FastAPI as the API backend that validates JWT tokens.

**Rationale**:
- Better-Auth is exclusively a TypeScript library with no Python SDK
- Better-Auth exposes JWKS endpoints (`/api/auth/jwks`) for JWT verification
- Better-Auth's JWT plugin provides standard JWT tokens that can be verified by any JWT library
- This architecture separates authentication concerns from business logic

**Alternatives Considered**:
1. **Pure FastAPI JWT implementation** - Rejected because user explicitly requested Better-Auth
2. **AuthX (Python native)** - Rejected as it doesn't align with Better-Auth requirement
3. **Proxy pattern through Better-Auth** - Considered but adds complexity; JWT verification is cleaner

### 2. Integration Architecture Pattern

**Decision**: Adopt a **JWT-based API Gateway Pattern** where:
- Better-Auth (Node.js) handles all authentication flows (registration, login, OAuth, sessions)
- FastAPI validates JWTs using Better-Auth's JWKS endpoint
- Database is shared between Better-Auth and FastAPI (Neon PostgreSQL)

**Rationale**:
- Better-Auth manages user sessions and tokens natively
- FastAPI focuses on business logic and API endpoints
- Shared database enables FastAPI to read user/session data for RBAC
- JWT verification is stateless and scalable

**Reference**: [Better-Auth with Different Backend](https://www.answeroverflow.com/m/1404248316824518656)

### 3. Better-Auth Database Schema (Compatible with FastAPI)

**Decision**: Use Better-Auth's standard database schema for users, sessions, and accounts.

**Schema (PostgreSQL)**:

```sql
-- User table
CREATE TABLE "user" (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    email_verified BOOLEAN DEFAULT false NOT NULL,
    name TEXT,
    image TEXT,
    role TEXT DEFAULT 'user',
    banned BOOLEAN DEFAULT false,
    ban_reason TEXT,
    ban_expires TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);

-- Session table
CREATE TABLE "session" (
    id TEXT PRIMARY KEY,
    expires_at TIMESTAMP NOT NULL,
    token TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW() NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE
);
CREATE INDEX session_user_id_idx ON session(user_id);

-- Account table (OAuth providers)
CREATE TABLE "account" (
    id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    provider_id TEXT NOT NULL,
    user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    access_token TEXT,
    refresh_token TEXT,
    id_token TEXT,
    access_token_expires_at TIMESTAMP,
    refresh_token_expires_at TIMESTAMP,
    scope TEXT,
    password TEXT,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);
CREATE INDEX account_user_id_idx ON account(user_id);

-- Verification table (email verification, password reset)
CREATE TABLE "verification" (
    id TEXT PRIMARY KEY,
    identifier TEXT NOT NULL,
    value TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Rationale**: Using Better-Auth's native schema ensures compatibility and allows FastAPI to read user/session data directly.

### 4. JWT Verification in FastAPI

**Decision**: Use `python-jose` with JWKS fetching for JWT verification.

**Implementation Pattern**:
```python
from jose import jwt, JWTError
import httpx
from functools import lru_cache

BETTER_AUTH_JWKS_URL = "http://localhost:3000/api/auth/jwks"

@lru_cache(maxsize=1)
async def get_jwks():
    async with httpx.AsyncClient() as client:
        response = await client.get(BETTER_AUTH_JWKS_URL)
        return response.json()

async def verify_jwt(token: str):
    jwks = await get_jwks()
    # Extract key and verify token
    payload = jwt.decode(token, jwks, algorithms=["RS256"])
    return payload
```

**Rationale**:
- Standard JWT verification using JWKS
- JWKS caching reduces latency
- Compatible with Better-Auth's JWT plugin configuration

### 5. OAuth Provider Configuration

**Decision**: Configure OAuth in Better-Auth (TypeScript), not in FastAPI.

**Better-Auth Configuration**:
```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID,
      clientSecret: process.env.GITHUB_CLIENT_SECRET,
    },
  },
  // ... other config
});
```

**Rationale**: OAuth flows require redirect handling which Better-Auth manages natively.

### 6. RBAC Implementation

**Decision**: Store roles in Better-Auth's user table, enforce in FastAPI.

**Implementation**:
- Better-Auth stores `role` field in user table (default: "user", options: "admin", "user")
- FastAPI reads role from JWT claims or database
- FastAPI enforces role-based access via dependencies

**FastAPI Dependency Pattern**:
```python
from fastapi import Depends, HTTPException, status

async def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
```

### 7. Session Management Strategy

**Decision**: Use Better-Auth's session-based authentication with JWT tokens for API access.

**Flow**:
1. User authenticates via Better-Auth (email/password or OAuth)
2. Better-Auth creates session and optionally issues JWT (via JWT plugin)
3. Client sends JWT to FastAPI for API requests
4. FastAPI validates JWT and extracts user info
5. Logout invalidates session in Better-Auth

**Rationale**: Separates session management (Better-Auth) from API authentication (JWT).

### 8. Technology Stack Decisions

| Component | Technology | Version | Rationale |
|-----------|------------|---------|-----------|
| API Framework | FastAPI | 0.109+ | User requirement, async support |
| Database | Neon PostgreSQL | Latest | User requirement, serverless |
| ORM | SQLAlchemy 2.0 | 2.0+ | Async support, Better-Auth schema compat |
| JWT Library | python-jose[cryptography] | 3.3+ | JWKS support, RS256 verification |
| HTTP Client | httpx | 0.26+ | Async JWKS fetching |
| Validation | Pydantic v2 | 2.5+ | User requirement, FastAPI compat |
| Migrations | Alembic | 1.13+ | User requirement |
| Testing | pytest-asyncio | 0.23+ | Async test support |
| Auth Server | Better-Auth | 1.3+ | User requirement |

### 9. Project Structure Decision

**Decision**: Restructure backend to `backend/app/` pattern as specified by user.

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # Better-Auth compatible
│   │   ├── session.py       # Better-Auth compatible
│   │   └── account.py       # Better-Auth compatible (OAuth)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # Proxy/wrapper for Better-Auth
│   │   └── users.py         # User management endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── auth.py          # JWT verification service
│   └── utils/
│       ├── __init__.py
│       └── dependencies.py  # FastAPI dependencies
├── alembic/
├── tests/
├── .env.example
├── requirements.txt
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

## Architectural Decision Records (ADR) Suggestions

The following architecturally significant decisions were identified:

1. **ADR-001: Better-Auth + FastAPI Integration Pattern**
   - Decision: JWT-based API gateway with Better-Auth as auth server
   - Impact: Requires running two services (Node.js + Python)

2. **ADR-002: Shared Database Architecture**
   - Decision: Better-Auth and FastAPI share the same Neon PostgreSQL database
   - Impact: Schema must be compatible with Better-Auth's expectations

3. **ADR-003: JWKS-based JWT Verification**
   - Decision: Use Better-Auth's JWKS endpoint for token verification
   - Impact: Requires network call for JWKS (cacheable)

## Open Questions Resolved

| Question | Resolution |
|----------|------------|
| Can Better-Auth work with Python? | Not directly, but via JWT verification |
| How to share user data? | Shared database with Better-Auth schema |
| How to handle OAuth? | Better-Auth handles OAuth flows natively |
| How to implement RBAC? | Role stored in Better-Auth, enforced in FastAPI |

## References

- [Better-Auth Documentation](https://www.better-auth.com/docs)
- [Better-Auth JWT Plugin](https://www.better-auth.com/docs/plugins/jwt)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Better-Auth with Different Backend Discussion](https://www.answeroverflow.com/m/1404248316824518656)
