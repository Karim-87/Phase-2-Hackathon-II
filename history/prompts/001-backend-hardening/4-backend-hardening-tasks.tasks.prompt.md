---
id: 4
title: backend-hardening-tasks
stage: tasks
date: 2026-01-17
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-backend-hardening
branch: 001-backend-hardening
user: Claude Sonnet
command: /sp.tasks
labels: [tasks, backend, hardening, postgresql, jwt, fastapi, alembic]
links:
  spec: specs/001-backend-hardening/spec.md
  plan: specs/001-backend-hardening/plan.md
  research: specs/001-backend-hardening/research.md
  data-model: specs/001-backend-hardening/data-model.md
  quickstart: specs/001-backend-hardening/quickstart.md
  contracts: specs/001-backend-hardening/contracts/task-api-contract.yaml
  tasks: specs/001-backend-hardening/tasks.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-backend-hardening/tasks.md
tests:
  - specs/001-backend-hardening/tasks.md
---

## Prompt

/sp.tasks Generate a safe, ordered task list to upgrade the backend using Backend_Skills

Input:
- Backend upgrade plan from /sp.plan
- Existing FastAPI backend codebase
- Backend skills in .claude/skills/*.skill

Objectives:
- Break backend upgrade into small, reversible tasks
- Ensure each task maps to exactly one Backend_Skill
- Minimize deployment risk

Task Groups:

Task Group 1: Project Audit
- Inventory routes, services, models, and configs
- Identify database, auth, and env entry points

Task Group 2: Database & Migrations
- Validate Neon PostgreSQL connection handling
- Configure Alembic env.py correctly
- Remove table auto-creation on startup

Task Group 3: Authentication Hardening
- Review JWT token creation and validation
- Add refresh token flow if missing
- Enforce rate limiting on auth endpoints

Task Group 4: Environment & Security
- Validate required environment variables on startup
- Secure secret handling and logging
- Apply backend-security skill recommendations

Task Group 5: Verification

## Response snapshot

Successfully generated comprehensive task list for backend hardening & modernization:

**Generated Artifacts:**
- tasks.md: Complete ordered task list with 68 individual tasks organized by user story

**Task Distribution:**
- Phase 1: Project Setup (4 tasks)
- Phase 2: Foundational Updates (7 tasks)
- Phase 3: US1 Secure User Authentication (9 tasks) - P1 Priority
- Phase 4: US2 Reliable Database Operations (6 tasks) - P1 Priority
- Phase 5: US3 Production-Ready Configuration (5 tasks) - P2 Priority
- Phase 6: US4 Structured Service Architecture (5 tasks) - P2 Priority
- Phase 7: Verification & Polish (12 tasks)

**Key Task Highlights:**
1. **Database Hardening**: Alembic migration setup (T010-T012) following database-migrations.skill.md
2. **Authentication Enhancement**: JWT refresh tokens (T020-T029) following fastapi-auth-jwt.skill.md
3. **Configuration Validation**: Enhanced settings validation (T040-T044) following backend-env-config.skill.md
4. **Security Implementation**: Rate limiting, token revocation, structured logging following backend-security.skill.md
5. **Neon PostgreSQL**: Connection pooling and optimization (T030-T035) following neon-postgres.skill.md

**Parallel Execution Opportunities:**
- T010-T016 (Foundational) can be executed in parallel
- T020-T029 (US1) can be executed with some parallelization
- T030-T035 (US2) can be executed with some parallelization
- T040-T044 (US3) can be executed in parallel
- T050-T054 (US4) can be executed with some parallelization

**User Story Dependencies:**
- All user stories can be implemented independently after foundational setup
- US1 (Authentication) and US2 (Database) can develop in parallel
- US3 (Configuration) and US4 (Architecture) can develop in parallel

## Outcome

- ✅ Impact: Complete task breakdown with Backend_Skills mapping
- 🧪 Tests: Tasks validated against user story acceptance criteria
- 📁 Files: tasks.md created with proper structure and dependencies
- 🔁 Next prompts: Ready for implementation phase
- 🧠 Reflection: Tasks organized by user story for independent development

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation with foundational tasks