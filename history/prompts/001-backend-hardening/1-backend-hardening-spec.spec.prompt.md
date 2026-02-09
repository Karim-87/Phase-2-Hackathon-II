---
id: 1
title: backend-hardening-spec
stage: spec
date: 2026-01-17
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-backend-hardening
branch: 001-backend-hardening
user: Claude Sonnet
command: /sp.specify
labels: [specification, backend, hardening, postgresql, jwt, fastapi]
links:
  spec: specs/001-backend-hardening/spec.md
  plan: null
  tasks: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-backend-hardening/spec.md
  - specs/001-backend-hardening/checklists/requirements.md
tests:
  - specs/001-backend-hardening/spec.md
---

## Prompt

/sp.specify Upgrade and harden existing FastAPI backend using predefined Backend Skills

Target audience:
- Production users
- Frontend consuming REST APIs

Focus:
- Database reliability
- Authentication security
- Maintainability and scalability

Success criteria:
- Fully migrated to Neon PostgreSQL
- Alembic migrations configured and used
- Secure JWT authentication with refresh tokens
- Environment-based configuration (.env)
- Clear service, router, and model separation
- Production-safe logging and startup

Constraints:
- Framework: FastAPI only
- Database: Neon PostgreSQL
- ORM: SQLModel / SQLAlchemy
- Auth: JWT-based (no full Better Auth migration)
- Format: Modular backend structure

Not building:
- Frontend code
- UI or SSR
- Third-party auth UI
- Unrelated microservices

Instructions:
- Use Backend Skills documentation as source of truth
- Refactor, do not rewrite unnecessarily
- Keep backward compatibility for API contracts
- Ensure production-readiness

## Response snapshot

Successfully created specification for backend hardening and modernization feature (001-backend-hardening). The specification includes:

**User Stories:**
- User Story 1: Secure User Authentication (P1) - JWT-based auth with refresh tokens
- User Story 2: Reliable Database Operations (P1) - Neon PostgreSQL with Alembic migrations
- User Story 3: Production-Ready Configuration Management (P2) - Environment-based config
- User Story 4: Structured Service Architecture (P2) - Modular service/router/model separation

**Functional Requirements (12 total):**
- JWT authentication with access/refresh tokens
- Neon PostgreSQL connectivity with SQLModel/SQLAlchemy
- Alembic migration management
- Environment variable configuration loading
- Secure password hashing
- Production logging
- Transaction management
- Token validation and refresh
- Service layer separation
- Router layer separation
- SQLModel data modeling
- Error handling

**Success Criteria (6 measurable outcomes):**
- 99.9% uptime for authentication endpoints
- Database operations complete within 500ms for 95% of requests
- Zero-downtime deployments with proper migrations
- 99.9% token validation/refresh success rate
- Safe migration rollbacks without data loss
- Error rates below 0.1% in production

Quality checklist completed and validated all requirements.

## Outcome

- ✅ Impact: Complete specification for backend hardening feature
- 🧪 Tests: Specification validated against quality criteria
- 📁 Files: spec.md and requirements checklist created
- 🔁 Next prompts: Ready for /sp.plan to create implementation plan
- 🧠 Reflection: Specification covers all required aspects with clear priorities

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with planning phase