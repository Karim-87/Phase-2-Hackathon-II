---
id: 6
title: todo-backend-api-plan
stage: plan
date: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-backend-api
branch: 001-todo-backend-api
user: Claude Sonnet
command: /sp.plan
labels: [planning, backend, api, todo-app, fastapi]
links:
  spec: ../todo-backend-api/1-todo-backend-api-spec.spec.prompt.md
  plan: ../todo-backend-api/2-todo-backend-api-plan.plan.prompt.md
  tasks: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-backend-api/plan.md
  - specs/001-todo-backend-api/research.md
  - specs/001-todo-backend-api/data-model.md
  - specs/001-todo-backend-api/quickstart.md
  - specs/001-todo-backend-api/contracts/task-api-contract.md
tests:
  - specs/001-todo-backend-api/checklists/requirements.md
---

## Prompt

/sp.plan

You are the Backend Agent for the "Multi-User Todo Web Application (Phase II Hackathon Project)".

You MUST strictly follow the Spec Constitution provided by the user (Last Updated: January 2026). This constitution is binding and non-negotiable.

SCOPE (Backend Only):
- FastAPI application
- SQLModel ORM
- Neon Serverless PostgreSQL
- JWT-based authentication (shared secret with frontend)
- uv for dependency & project management

CORE RESPONSIBILITIES:
1. Provide secure RESTful APIs for task management
2. Enforce strict per-user data isolation using JWT
3. Validate and verify JWT tokens for every request
4. Persist data in Neon PostgreSQL using SQLModel
5. Follow clean backend architecture and separation of concerns

API REQUIREMENTS:
Base path: /api

Endpoints (ALL require JWT auth):
- POST   /api/tasks
- GET    /api/tasks
- GET    /api/tasks/{taskId}
- PUT    /api/tasks/{taskId}
- DELETE /api/tasks/{taskId}
- PATCH  /api/tasks/{taskId}/complete

SECURITY REQUIREMENTS:
- JWT must be verified on every request
- Invalid, missing, or expired tokens → HTTP 401
- User identity must be derived ONLY from JWT
- user_id from JWT must be used to filter all DB queries
- No endpoint may accept user_id from URL or body

DATABASE REQUIREMENTS:
Task model must include:
- id
- user_id (from JWT)
- title
- description
- due_datetime
- priority (Eisenhower Matrix compatible)
- is_completed
- created_at
- updated_at

TECHNICAL CONSTRAINTS:
- Use environment variables:
  • NEON_DATABASE_URL
  • BETTER_AUTH_SECRET
- Use async FastAPI where appropriate
- No hardcoded secrets
- No frontend or UI logic
- No mock authentication

OUTPUT EXPECTATION:
- Project structure
- Database models
- JWT auth dependency/middleware
- CRUD API endpoints
- Input/output schemas
- Error handling
- Clear inline comments referencing this constitution

User isolation is NON-NEGOTIABLE.

## Response snapshot

Successfully created a comprehensive implementation plan for the Todo Backend API following the Spec Constitution requirements. The plan includes:

**Technical Context**:
- Python 3.11+ with FastAPI framework
- SQLModel ORM for Neon Serverless PostgreSQL
- JWT-based authentication with token validation
- pytest for testing framework
- uv for dependency management

**Project Structure**:
- Organized backend with proper separation of concerns
- Models, schemas, API routes, authentication, and utilities in separate modules
- Test organization by type (unit, integration, contract)
- Proper configuration and deployment files

**Constitution Compliance**:
- All security requirements validated
- User isolation mechanisms confirmed
- JWT authentication requirements verified
- Database requirements aligned

**Additional Artifacts**:
- Comprehensive research document covering technologies
- Detailed data model with proper indexing and constraints
- API contract documentation with all endpoints and security requirements
- Quickstart guide for setup and testing

The implementation plan provides a clear roadmap for developing the secure task management API with proper user isolation and JWT authentication.

## Outcome

- ✅ Impact: Complete backend API implementation plan with constitution compliance
- 🧪 Tests: Requirements checklist validated
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/ created
- 🔁 Next prompts: Ready for backend API task breakdown (/sp.tasks)
- 🧠 Reflection: Plan addresses all constitutional requirements with proper security

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to task breakdown for implementation