---
id: "0001"
title: "FastAPI Better-Auth Spec Creation"
stage: spec
date: 2026-02-03
surface: agent
model: claude-opus-4-5-20251101
feature: 003-fastapi-better-auth
branch: 003-fastapi-better-auth
user: user
command: /sp.specify
labels: ["fastapi", "better-auth", "authentication", "neon-postgresql", "rbac"]
links:
  spec: specs/003-fastapi-better-auth/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-fastapi-better-auth/spec.md
  - specs/003-fastapi-better-auth/checklists/requirements.md
tests:
  - null
---

## Prompt

I want to set up a production-ready FastAPI backend with the following requirements:

**Tech Stack:**
- FastAPI (latest with async patterns)
- Neon PostgreSQL (serverless database)
- Better-Auth for authentication (NOT traditional JWT)
- SQLAlchemy 2.0 (async ORM)
- Alembic for migrations
- Pydantic v2 for validation

**Authentication Requirements:**
- Use Better-Auth following our better-auth-best-practices skill
- Email/Password authentication
- OAuth providers (Google, GitHub)
- Session management with refresh tokens
- Role-based access control (RBAC)

**Project Structure:**
backend/
├── app/
│   ├── init.py
│   ├── main.py
│   ├── config.py (environment-based settings)
│   ├── database.py (Neon PostgreSQL setup)
│   ├── models/
│   │   ├── init.py
│   │   └── user.py (Better-Auth compatible schema)
│   ├── routers/
│   │   ├── init.py
│   │   ├── auth.py (Better-Auth endpoints)
│   │   └── users.py
│   ├── schemas/
│   │   ├── init.py
│   │   └── user.py (Pydantic models)
│   ├── services/
│   │   ├── init.py
│   │   └── auth.py (Better-Auth integration)
│   └── utils/
│       ├── init.py
│       └── dependencies.py
├── alembic/
├── tests/
├── .env.example
├── requirements.txt
├── pyproject.toml
└── README.md

**Critical Instructions for the Agent:**
1. **MUST use the backend-architect agent** for this task
2. **MUST read the better-auth-best-practices skill FIRST** before any implementation
3. Follow the exact patterns from the skill for Better-Auth setup
4. Use async/await throughout the codebase
5. Implement proper error handling and validation
6. Add comprehensive tests (pytest + pytest-asyncio)
7. Include Docker setup for local development
8. Document all Better-Auth flows and API endpoints

**Expected Deliverables:**
- Complete backend setup with all files
- Alembic migration for user schema

## Response snapshot

Created feature specification for production-ready FastAPI backend with Better-Auth integration:

1. **Branch created**: `003-fastapi-better-auth`
2. **Spec file**: `specs/003-fastapi-better-auth/spec.md`
3. **Checklist**: `specs/003-fastapi-better-auth/checklists/requirements.md`

The specification includes:
- 6 prioritized user stories (P1-P3) covering registration, authentication, OAuth, session management, RBAC, and password reset
- 18 functional requirements covering all auth flows
- 5 key entities (User, Session, Account, Role, UserRole)
- 10 measurable success criteria
- Edge cases and scope boundaries defined

All quality checklist items passed - ready for `/sp.plan` or `/sp.clarify`.

## Outcome

- ✅ Impact: Created comprehensive feature specification for FastAPI Better-Auth backend
- 🧪 Tests: N/A (specification phase)
- 📁 Files: 2 files created (spec.md, requirements.md checklist)
- 🔁 Next prompts: `/sp.plan` to generate implementation plan, or `/sp.clarify` if further clarification needed
- 🧠 Reflection: User provided detailed requirements making spec creation straightforward with no clarifications needed

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Spec quality checklist - PASS (16/16 items)
- Prompt variant (if applicable): Standard sp.specify workflow
- Next experiment (smallest change to try): None needed - successful execution
