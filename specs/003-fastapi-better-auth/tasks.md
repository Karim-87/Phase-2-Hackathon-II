# Tasks: FastAPI Better-Auth Backend

**Input**: Design documents from `/specs/003-fastapi-better-auth/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml

**Tests**: Tests included as specified in plan.md (pytest + pytest-asyncio for >80% coverage)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/` for source, `backend/tests/` for tests
- **Config**: `backend/.env.example`, `backend/pyproject.toml`
- **Migrations**: `backend/alembic/`

---

## Phase 1: Setup (Project Infrastructure)

**Purpose**: Restructure backend directory and initialize new project structure

- [X] T001 Create new project structure with `backend/app/` directory layout per plan.md
- [X] T002 [P] Create `backend/app/__init__.py` with package initialization
- [X] T003 [P] Create `backend/requirements.txt` with updated async dependencies (fastapi, sqlalchemy[asyncio], asyncpg, python-jose[cryptography], httpx, pydantic-settings)
- [X] T004 [P] Create `backend/requirements-dev.txt` with test dependencies (pytest, pytest-asyncio, pytest-cov, httpx)
- [X] T005 [P] Update `backend/pyproject.toml` with project metadata and pytest configuration
- [X] T006 [P] Create `backend/.env.example` with all required environment variables

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Configuration & Database

- [X] T007 Create `backend/app/config.py` with Pydantic Settings for async database URL, Better-Auth URL, JWT settings
- [X] T008 Create `backend/app/database.py` with async SQLAlchemy engine, async session factory, and get_db dependency
- [X] T009 Create `backend/app/models/__init__.py` with model exports
- [X] T010 Create `backend/app/models/base.py` with SQLAlchemy declarative Base class

### Better-Auth Compatible Models

- [X] T011 [P] Create `backend/app/models/user.py` with User model following Better-Auth schema (id, email, email_verified, name, image, role, banned, ban_reason, ban_expires, timestamps)
- [X] T012 [P] Create `backend/app/models/session.py` with Session model (id, user_id FK, token, expires_at, ip_address, user_agent, impersonated_by, timestamps)
- [X] T013 [P] Create `backend/app/models/account.py` with Account model for OAuth (id, user_id FK, account_id, provider_id, tokens, password, timestamps)
- [X] T014 [P] Create `backend/app/models/verification.py` with Verification model (id, identifier, value, expires_at, timestamps)

### Alembic Migration Setup

- [X] T015 Update `backend/alembic/env.py` for async SQLAlchemy with Neon PostgreSQL
- [X] T016 Create initial Alembic migration for Better-Auth schema tables in `backend/alembic/versions/`

### Pydantic Schemas

- [X] T017 Create `backend/app/schemas/__init__.py` with schema exports
- [X] T018 [P] Create `backend/app/schemas/common.py` with SuccessResponse, ErrorResponse, Pagination schemas
- [X] T019 [P] Create `backend/app/schemas/user.py` with UserRead, UserUpdate, RoleUpdate, BanUserRequest schemas

### Services & Utils Base

- [X] T020 Create `backend/app/services/__init__.py` with service exports
- [X] T021 Create `backend/app/utils/__init__.py` with utils exports
- [X] T022 Create `backend/app/utils/exceptions.py` with custom HTTPException handlers and error codes

### FastAPI Application

- [X] T023 Create `backend/app/main.py` with FastAPI app, CORS middleware, exception handlers, health endpoint
- [X] T024 Create `backend/app/routers/__init__.py` with router exports

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 & 2 - Registration & Authentication (Priority: P1)

**Goal**: Enable users to authenticate via Better-Auth JWT tokens and access protected resources

**Independent Test**: Authenticate with a valid JWT from Better-Auth and access GET /api/v1/auth/me successfully

**Note**: Registration/Login are handled by Better-Auth. FastAPI validates JWTs and provides session/user endpoints.

### Tests for Auth Foundation

- [X] T025 [P] [US1] Create `backend/tests/__init__.py` for test package
- [X] T026 [P] [US1] Create `backend/tests/conftest.py` with async pytest fixtures (test client, mock JWT, test database session)
- [X] T027 [P] [US1] Create `backend/tests/test_auth.py` with JWT validation tests (valid token, expired token, invalid signature, missing token)

### JWT Verification Service

- [X] T028 [US1] Create `backend/app/services/auth.py` with JWKSClient class (fetch JWKS from Better-Auth, cache keys, verify JWT signatures)
- [X] T029 [US1] Add get_current_user dependency in `backend/app/utils/dependencies.py` (extract JWT, verify, return user_id)
- [X] T030 [US1] Add require_verified_email dependency in `backend/app/utils/dependencies.py`
- [X] T031 [US1] Add check_user_not_banned dependency in `backend/app/utils/dependencies.py`

### Auth Endpoints

- [X] T032 [US2] Create `backend/app/routers/auth.py` with GET /api/v1/auth/session endpoint (validate JWT, return session + user)
- [X] T033 [US2] Add GET /api/v1/auth/me endpoint in `backend/app/routers/auth.py` (return current user profile)
- [X] T034 [US2] Register auth router in `backend/app/main.py`

**Checkpoint**: Users can authenticate via Better-Auth JWT and access protected endpoints

---

## Phase 4: User Story 3 & 6 - OAuth & Password Reset Support (Priority: P2)

**Goal**: FastAPI reads OAuth accounts and verification records (actual flows handled by Better-Auth)

**Independent Test**: After OAuth login via Better-Auth, verify user can access FastAPI endpoints with their JWT

**Note**: OAuth flows and password reset emails are handled by Better-Auth. FastAPI just reads the data.

### Tests for OAuth/Verification

- [X] T035 [P] [US3] Add OAuth account lookup tests in `backend/tests/test_auth.py`
- [X] T036 [P] [US3] Add user with linked accounts fixture in `backend/tests/conftest.py`

### Account Service

- [X] T037 [US3] Create `backend/app/services/account.py` with get_user_accounts, get_account_by_provider functions
- [X] T038 [US3] Add GET /api/v1/auth/accounts endpoint in `backend/app/routers/auth.py` (list linked OAuth accounts for current user)

**Checkpoint**: OAuth users can access their linked accounts via FastAPI

---

## Phase 5: User Story 4 - Session Management (Priority: P2)

**Goal**: Users can view and manage their active sessions

**Independent Test**: List active sessions for authenticated user, revoke a session, verify it's invalidated

### Tests for Session Management

- [X] T039 [P] [US4] Create `backend/tests/test_sessions.py` with session list/revoke tests

### Session Service

- [X] T040 [US4] Create `backend/app/services/session.py` with get_user_sessions, revoke_session, revoke_all_sessions functions
- [X] T041 [US4] Add session schema in `backend/app/schemas/session.py` (SessionRead, SessionsListResponse)

### Session Endpoints

- [X] T042 [US4] Add GET /api/v1/users/{user_id}/sessions endpoint in `backend/app/routers/users.py`
- [X] T043 [US4] Add DELETE /api/v1/users/{user_id}/sessions endpoint for revoking all sessions
- [X] T044 [US4] Add DELETE /api/v1/users/{user_id}/sessions/{session_id} endpoint for revoking single session

**Checkpoint**: Users can manage their active sessions

---

## Phase 6: User Story 5 - Role-Based Access Control (Priority: P3)

**Goal**: Admins can manage users and roles, regular users have restricted access

**Independent Test**: Admin can list all users and change roles; regular user gets 403 on admin endpoints

### Tests for RBAC

- [X] T045 [P] [US5] Create `backend/tests/test_users.py` with admin/user permission tests
- [X] T046 [P] [US5] Add admin user fixture in `backend/tests/conftest.py`

### Role Dependencies

- [X] T047 [US5] Add require_admin dependency in `backend/app/utils/dependencies.py`
- [X] T048 [US5] Add require_role(roles: list) dependency for flexible role checks

### User Service

- [X] T049 [US5] Create `backend/app/services/user.py` with list_users (paginated), get_user, update_user functions
- [X] T050 [US5] Add update_user_role, ban_user, unban_user functions in `backend/app/services/user.py`

### User Management Endpoints

- [X] T051 [US5] Create `backend/app/routers/users.py` with GET /api/v1/users endpoint (admin only, paginated)
- [X] T052 [US5] Add GET /api/v1/users/{user_id} endpoint (admin or self)
- [X] T053 [US5] Add PATCH /api/v1/users/{user_id} endpoint (admin or self, restricted fields)
- [X] T054 [US5] Add PUT /api/v1/users/{user_id}/role endpoint (admin only)
- [X] T055 [US5] Add POST /api/v1/users/{user_id}/ban endpoint (admin only)
- [X] T056 [US5] Add DELETE /api/v1/users/{user_id}/ban endpoint (admin only, unban)
- [X] T057 [US5] Register users router in `backend/app/main.py`

**Checkpoint**: Full RBAC system operational - admins can manage users

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, DevOps, and quality improvements

### Documentation

- [X] T058 [P] Create `backend/README.md` with setup instructions, API overview, and development guide
- [X] T059 [P] Add comprehensive docstrings to all service functions
- [X] T060 [P] Add OpenAPI description to all endpoints in routers

### Docker & DevOps

- [X] T061 [P] Create `backend/Dockerfile` with multi-stage build (Python 3.11-slim, uvicorn)
- [X] T062 [P] Create `backend/docker-compose.yml` with FastAPI service and local PostgreSQL
- [X] T063 Add health check endpoints in `backend/app/main.py` (/health, /health/db)

### Logging & Observability

- [X] T064 Add structured logging configuration in `backend/app/config.py`
- [X] T065 Add request logging middleware in `backend/app/main.py`
- [X] T066 Add authentication event logging (login success/failure) in `backend/app/services/auth.py`

### Additional Tests

- [X] T067 [P] Create `backend/tests/test_services.py` with unit tests for service layer
- [X] T068 Run full test suite and verify >80% coverage
- [X] T069 Run quickstart.md validation to ensure setup instructions work

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1/US2 (Auth): Can start immediately after Phase 2
  - US3/US6 (OAuth/Reset): Can start after Phase 2 (independent of US1/US2)
  - US4 (Sessions): Can start after Phase 2 (independent of US1/US2)
  - US5 (RBAC): Can start after Phase 2 (independent of other stories)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Depends On | Can Parallel With |
|-------|------------|-------------------|
| US1/US2 (Auth) | Phase 2 only | US3, US4, US5, US6 |
| US3/US6 (OAuth/Reset) | Phase 2 only | US1, US2, US4, US5 |
| US4 (Sessions) | Phase 2 only | US1, US2, US3, US5, US6 |
| US5 (RBAC) | Phase 2 only | US1, US2, US3, US4, US6 |

### Within Each User Story

1. Tests MUST be written and FAIL before implementation
2. Dependencies/services before endpoints
3. Core implementation before integration
4. Story complete before moving to next priority (if sequential)

### Parallel Opportunities

**Phase 1 (Setup)**: T002, T003, T004, T005, T006 can all run in parallel

**Phase 2 (Foundation)**:
- T011, T012, T013, T014 (models) can all run in parallel
- T018, T019 (schemas) can run in parallel
- After models complete: T015, T016 (migrations)

**User Stories** (after Phase 2):
- ALL user story phases can run in parallel with different team members
- Within each story: Tests [P] can run in parallel, Models [P] can run in parallel

---

## Parallel Example: Foundation Phase

```bash
# Launch all models in parallel:
Task: "Create User model in backend/app/models/user.py"
Task: "Create Session model in backend/app/models/session.py"
Task: "Create Account model in backend/app/models/account.py"
Task: "Create Verification model in backend/app/models/verification.py"

# Launch all schemas in parallel:
Task: "Create common schemas in backend/app/schemas/common.py"
Task: "Create user schemas in backend/app/schemas/user.py"
```

---

## Parallel Example: User Stories (Multi-Developer)

```bash
# Developer A works on US1/US2 (Auth):
Task: "Create auth.py service with JWT verification"
Task: "Create auth router with /session and /me endpoints"

# Developer B works on US5 (RBAC) simultaneously:
Task: "Create user.py service with CRUD and role management"
Task: "Create users router with admin endpoints"

# Developer C works on US4 (Sessions) simultaneously:
Task: "Create session.py service"
Task: "Add session management endpoints"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: US1/US2 (Auth Foundation)
4. **STOP and VALIDATE**: Test JWT validation and /auth/me endpoint
5. Deploy/demo if ready - users can now authenticate!

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1/US2 (Auth) → Test → Deploy (MVP - authentication works!)
3. Add US5 (RBAC) → Test → Deploy (admin features available)
4. Add US4 (Sessions) → Test → Deploy (session management)
5. Add US3/US6 (OAuth/Reset) → Test → Deploy (full auth system)
6. Add Phase 7 (Polish) → Final release

### Recommended Order (Sequential)

1. **Phase 1**: Setup (T001-T006)
2. **Phase 2**: Foundation (T007-T024)
3. **Phase 3**: Auth (T025-T034) - **MVP CHECKPOINT**
4. **Phase 6**: RBAC (T045-T057) - High value
5. **Phase 5**: Sessions (T039-T044)
6. **Phase 4**: OAuth Support (T035-T038)
7. **Phase 7**: Polish (T058-T069)

---

## Summary

| Category | Count |
|----------|-------|
| Total Tasks | 69 |
| Phase 1 (Setup) | 6 |
| Phase 2 (Foundation) | 18 |
| Phase 3 (US1/US2 Auth) | 10 |
| Phase 4 (US3/US6 OAuth) | 4 |
| Phase 5 (US4 Sessions) | 6 |
| Phase 6 (US5 RBAC) | 13 |
| Phase 7 (Polish) | 12 |
| Parallel Tasks [P] | 32 |

**MVP Scope**: Phases 1-3 (34 tasks) delivers working JWT authentication
**Full Feature**: All 69 tasks for complete Better-Auth integration

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Verify tests fail before implementing (TDD approach per plan.md)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All OAuth flows, registration, and login are handled by Better-Auth - FastAPI only validates JWTs
