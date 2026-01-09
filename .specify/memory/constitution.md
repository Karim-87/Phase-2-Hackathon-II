<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles:
- Principle 1: General → Full-Stack Development Mandate
- Principle 2: CLI Interface → RESTful API Standard
- Principle 3: Test-First → Authentication-First Security
- Principle 4: Integration Testing → User Isolation Compliance
- Principle 5: Observability → JWT Token Security
- Added Principle 6: Frontend-Backend Separation
Added sections: Technology Stack Requirements, Development Workflow
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
Follow-up TODOs: None
-->

# Multi-User Todo Web Application Constitution

## Core Principles

### Full-Stack Development Mandate
Every feature must span both frontend and backend components; Both frontend (Next.js) and backend (FastAPI) must be developed in parallel; Clear separation of concerns required - frontend handles presentation, backend handles business logic and data persistence.

### RESTful API Standard
Every backend service exposes functionality via RESTful API endpoints; API contracts must follow the specified endpoint patterns: POST /api/tasks, GET /api/tasks, GET /api/tasks/:taskId, PUT /api/tasks/:taskId, DELETE /api/tasks/:taskId, PATCH /api/tasks/:taskId/complete; Support JSON request/response formats with proper HTTP status codes.

### Authentication-First Security
Security through authentication must be implemented before core features; All API endpoints must require valid JWT tokens; User isolation must be enforced - never allow access to other users' data.

### User Isolation Compliance
Every data operation must filter by authenticated user only; Database queries must always include user_id in WHERE clauses; Cross-user data access is strictly prohibited.

### JWT Token Security
JWT verification must reject invalid/expired/missing tokens with 401 Unauthorized responses; All API requests must include Authorization: Bearer <token> header; Backend middleware must verify JWT signatures using shared secret.

### Frontend-Backend Separation
Frontend (Next.js) and backend (FastAPI) must be developed as separate applications; Frontend communicates with backend only through RESTful API calls; Environment variables must be used separately for frontend and backend configuration.

## Technology Stack Requirements

Technology stack is fixed and must be followed precisely:
- Frontend: Next.js 16+ (App Router) created via: `npx create-next-app@16.0.10`
- Backend: Python FastAPI with SQLModel ORM
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT tokens
- Dependency management: uv for Python project management
- All operations must be per authenticated user (user isolation)

## Development Workflow

Development follows Spec-Driven Development using Claude Code + Spec-Kit Plus with agentic dev stack workflow:
1. Write detailed spec
2. Generate implementation plan
3. Break into concrete tasks
4. Implement via Claude Code (iterative prompting)
All generated code/files must reference this constitution, frontend must be responsive (mobile + desktop), use modern Next.js patterns (Server Components where possible, Client Components when needed), prioritization should be visual (colored badges/labels).

## Governance

This constitution supersedes all other practices and must be followed for all development activities.
Amendments require documentation and approval before implementation.
All PRs/reviews must verify compliance with constitution principles.
Complexity must be justified with clear rationale.
Use this constitution file for runtime development guidance.

**Version**: 1.1.0 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-01-09