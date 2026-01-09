---
id: 5
title: todo-backend-api-spec
stage: spec
date: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-backend-api
branch: 001-todo-backend-api
user: Claude Sonnet
command: /sp.specify
labels: [specification, backend, api, todo-app, fastapi]
links:
  spec: ../todo-backend-api/1-todo-backend-api-spec.spec.prompt.md
  plan: null
  tasks: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-backend-api/spec.md
  - specs/001-todo-backend-api/checklists/requirements.md
tests:
  - specs/001-todo-backend-api/checklists/requirements.md
---

## Prompt

/sp.specify

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

Created comprehensive backend API specification for the Multi-User Todo Web Application following the user's requirements. The specification includes:

**User Stories**:
- User Story 1 (P1): Secure Task Management API for creating, reading, updating, and deleting tasks with strict user isolation
- User Story 2 (P2): Task completion and deletion functionality with proper access controls
- User Story 3 (P3): Secure authentication and error handling with JWT validation

**Functional Requirements**:
- 15 detailed functional requirements (FR-001 to FR-015) covering JWT validation, user isolation, API endpoints, data persistence, and security constraints
- All endpoints require JWT authentication and enforce user data isolation
- Task model includes all required fields: id, user_id, title, description, due_datetime, priority, is_completed, timestamps

**Success Criteria**:
- 5 measurable success criteria (SC-001 to SC-005) focusing on performance, security, and reliability
- Emphasis on 100% accuracy in user data isolation and JWT validation

**Quality Assurance**:
- Created requirements checklist to validate specification completeness
- All requirements are testable and unambiguous
- No implementation details leaked into the specification
- Edge cases identified and addressed

The specification strictly follows the provided constitution with non-negotiable user isolation requirements and JWT-based authentication.

## Outcome

- ✅ Impact: Complete backend API specification aligned with constitution
- 🧪 Tests: Requirements checklist created and validated
- 📁 Files: spec.md and requirements checklist created
- 🔁 Next prompts: Ready for backend API planning (/sp.plan)
- 🧠 Reflection: Specification balances comprehensive coverage with adherence to security requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to backend API planning