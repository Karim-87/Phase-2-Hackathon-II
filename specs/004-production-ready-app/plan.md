# Implementation Plan: Production-Ready App Enhancement

**Branch**: `004-production-ready-app` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/004-production-ready-app/spec.md`

## Summary

Transform the existing Todo application from a development prototype into a production-ready system by: (1) upgrading password hashing from SHA-256 to bcrypt, (2) unifying the task model into the main SQLAlchemy ORM and creating a fully integrated task API router, (3) overhauling the frontend for responsive mobile-first design across all viewports, (4) connecting frontend task management to the backend API end-to-end, and (5) hardening for production with proper error handling, security configuration, debug log removal, and automated test coverage for critical paths.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.3 (frontend)
**Primary Dependencies**: FastAPI 0.109+, SQLAlchemy 2.0+, python-jose, passlib[bcrypt] (NEW), Next.js 16, React 19, Tailwind CSS 3.3
**Storage**: Neon PostgreSQL (serverless) via asyncpg, Alembic migrations
**Testing**: pytest + pytest-asyncio (backend)
**Target Platform**: Web — Next.js on Vercel (frontend), FastAPI on container/server (backend)
**Project Type**: Web application (separate frontend + backend)
**Performance Goals**: Auth flows < 60s registration, < 30s sign-in; all pages responsive at 375px/768px/1440px
**Constraints**: No breaking changes to Better-Auth compatible schema; environment-driven config only
**Scale/Scope**: Single-user to multi-user todo app; 4 database tables; ~15 API endpoints

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The project constitution is currently an unfilled template. No gate violations exist because no principles have been ratified. Proceeding with industry-standard best practices:

- **Security**: bcrypt for passwords, JWT with HS256, environment-driven secrets
- **Testing**: pytest for critical backend paths
- **Simplicity**: Smallest viable diff — enhance existing patterns, don't rewrite
- **Observability**: Structured logging already in place, preserve it

**Post-Phase 1 re-check**: No violations. Design follows existing codebase patterns.

## Project Structure

### Documentation (this feature)

```text
specs/004-production-ready-app/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0: research findings
├── data-model.md        # Phase 1: entity definitions
├── quickstart.md        # Phase 1: setup instructions
├── contracts/
│   └── api-contract.md  # Phase 1: API endpoint contracts
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── main.py                    # FastAPI entry — add tasks router
│   ├── config.py                  # Settings — add production CORS validation
│   ├── database.py                # Async SQLAlchemy — unchanged
│   ├── models/
│   │   ├── base.py                # DeclarativeBase — unchanged
│   │   ├── user.py                # User model — add tasks relationship
│   │   ├── account.py             # Account model — unchanged
│   │   ├── session.py             # Session model — unchanged
│   │   ├── verification.py        # Verification model — unchanged
│   │   └── task.py                # NEW: Task model (SQLAlchemy ORM)
│   ├── routers/
│   │   ├── auth.py                # Auth endpoints — upgrade password hashing
│   │   ├── users.py               # User endpoints — unchanged
│   │   └── tasks.py               # NEW: Task CRUD router
│   ├── schemas/
│   │   ├── user.py                # User schemas — add password validation
│   │   ├── session.py             # Session schemas — unchanged
│   │   ├── common.py              # Common schemas — unchanged
│   │   └── task.py                # NEW: Task request/response schemas
│   ├── services/
│   │   └── auth.py                # JWT verification — unchanged
│   └── utils/
│       ├── dependencies.py        # Auth dependencies — unchanged
│       └── exceptions.py          # Exception handlers — unchanged
├── alembic/
│   └── versions/
│       └── 002_add_task_table.py  # NEW: Task table migration
├── tests/
│   ├── conftest.py                # NEW: Test fixtures (async DB, test client)
│   ├── test_auth.py               # NEW: Auth endpoint tests
│   └── test_tasks.py              # NEW: Task CRUD tests
└── requirements.txt               # Add passlib[bcrypt]

frontend/
├── app/
│   ├── layout.tsx                 # Root layout — wrap with ErrorBoundary
│   ├── page.tsx                   # Home page — responsive enhancement
│   ├── (auth)/
│   │   ├── sign-in/page.tsx       # Sign-in — unchanged (delegates to form)
│   │   └── sign-up/page.tsx       # Sign-up — unchanged (delegates to form)
│   ├── dashboard/page.tsx         # Dashboard — responsive overhaul
│   └── tasks/
│       ├── page.tsx               # Tasks list — responsive, use backend filters
│       ├── create/page.tsx        # Create task — add loading/error states
│       └── [id]/page.tsx          # Task detail — responsive, better UX
├── components/
│   ├── auth/
│   │   ├── auth-provider.tsx      # Auth context — remove console.logs, cookie flags
│   │   ├── login-form.tsx         # Login form — add loading state, responsive
│   │   └── register-form.tsx      # Register form — add password strength, loading
│   ├── tasks/
│   │   ├── task-card.tsx          # Task card — responsive, loading states
│   │   ├── task-list.tsx          # Task list — use LoadingSpinner, error state
│   │   ├── task-form.tsx          # Task form — validation, responsive
│   │   ├── task-filters.tsx       # Filters — responsive
│   │   └── priority-badge.tsx     # Priority badge — unchanged
│   ├── ui/
│   │   ├── modern-button.tsx      # Button — add loading variant
│   │   ├── loading-spinner.tsx    # Spinner — add size/color props
│   │   ├── error-boundary.tsx     # Error boundary — better styling
│   │   └── toast.tsx              # NEW: Toast notification component
│   └── providers/
│       └── theme-provider.tsx     # Theme — unchanged
├── hooks/
│   └── use-tasks.ts              # Tasks hook — use backend filtering
├── lib/
│   └── api/
│       ├── api-client.ts         # API client — add retry, better errors
│       └── task-service.ts       # Task service — align with new API contract
├── types/
│   ├── user.ts                   # User types — add name, email, role
│   └── task.ts                   # Task types — unchanged
└── middleware.ts                  # Route protection — unchanged
```

**Structure Decision**: Web application with separate frontend (Next.js) and backend (FastAPI). This preserves the existing architecture. All changes are modifications to existing files or additions within established directories. No new top-level directories introduced.

## Complexity Tracking

No constitution gate violations to justify — constitution is unfilled.

## Implementation Phases

### Phase A: Backend Security & Data Layer (P1 — Auth)

**Goal**: Upgrade password hashing, unify Task model, create Task API router.

**Changes**:

1. **Add `passlib[bcrypt]` to `requirements.txt`**
   - Ref: `backend/requirements.txt`
   - Add line: `passlib[bcrypt]>=1.7.4`

2. **Upgrade password hashing in `auth.py`**
   - Ref: `backend/app/routers/auth.py:37-51`
   - Replace `hash_password()` and `verify_password()` with bcrypt via passlib
   - Add transparent migration: if stored hash matches SHA-256 format (`salt:hash`), verify with old method, then re-hash to bcrypt and update the Account record
   - New bcrypt hashes use passlib's `$2b$` format

3. **Add password validation to signup**
   - Ref: `backend/app/routers/auth.py:91-148` (signup endpoint)
   - Validate: min 8 chars, 1 uppercase, 1 lowercase, 1 number
   - Return 422 with structured error if validation fails

4. **Create Task model (`backend/app/models/task.py`)**
   - SQLAlchemy ORM model matching `data-model.md`
   - Text PK (ULID string), FK to user.id
   - Priority as text column with enum validation
   - Indexes: user_id, (user_id, is_completed) composite

5. **Add tasks relationship to User model**
   - Ref: `backend/app/models/user.py`
   - Add: `tasks: Mapped[List["Task"]] = relationship(...)`

6. **Create Task schemas (`backend/app/schemas/task.py`)**
   - Pydantic v2 models: TaskCreate, TaskRead, TaskUpdate, TaskListResponse
   - Matching API contract

7. **Create Task router (`backend/app/routers/tasks.py`)**
   - CRUD endpoints per API contract
   - All endpoints use `get_active_user` dependency
   - Queries scoped to `user_id == current_user.id`
   - Register in `main.py`

8. **Create Alembic migration for Task table**
   - `alembic revision --autogenerate -m "add_task_table"`
   - Verify migration creates table with correct columns and indexes

9. **Add production CORS validation**
   - Ref: `backend/app/config.py`
   - If `ENVIRONMENT=production` and any origin contains `localhost`, log warning

---

### Phase B: Frontend Responsive UI Overhaul (P1 — UI/UX)

**Goal**: Make all pages fully responsive and polished.

**Changes**:

1. **Enhance auth forms (`login-form.tsx`, `register-form.tsx`)**
   - Add loading/disabled state on submit button
   - Add password strength indicator on register form
   - Ensure forms are usable at 375px (full-width inputs, proper padding)
   - Add proper form validation feedback

2. **Overhaul dashboard (`dashboard/page.tsx`)**
   - Mobile: single-column, stacked layout, collapsible filters
   - Tablet: two-column task grid
   - Desktop: full-width with sidebar-style filters
   - Replace "Loading..." text with LoadingSpinner component
   - Proper empty state with illustration/icon

3. **Responsive task pages**
   - `tasks/page.tsx`: Responsive grid, use backend filtering via API
   - `tasks/create/page.tsx`: Add loading state, error feedback
   - `tasks/[id]/page.tsx`: Responsive detail layout, replace `confirm()` with styled dialog

4. **Enhance UI components**
   - `loading-spinner.tsx`: Accept size/color props
   - `modern-button.tsx`: Add loading variant with spinner
   - `error-boundary.tsx`: Modernize styling to match design system
   - NEW `toast.tsx`: Simple toast notification for API errors

5. **Root layout enhancement**
   - Ref: `frontend/app/layout.tsx`
   - Wrap children with ErrorBoundary component
   - Ensure proper viewport meta tag

6. **Home page (`page.tsx`)**
   - Responsive hero section
   - Proper CTA buttons at all breakpoints

---

### Phase C: Frontend-Backend Integration (P2 — Task Flow)

**Goal**: Connect task management UI to backend API end-to-end.

**Changes**:

1. **Align task-service.ts with new API contract**
   - Ref: `frontend/lib/api/task-service.ts`
   - Update all endpoints to match `/api/v1/tasks` patterns
   - Add proper TypeScript return types
   - Handle error responses with structured error codes

2. **Update use-tasks.ts hook**
   - Ref: `frontend/hooks/use-tasks.ts`
   - Use server-side filtering via API query params instead of client-side
   - Add per-operation loading states (creating, updating, deleting)
   - Add retry capability for failed operations

3. **Update API client**
   - Ref: `frontend/lib/api/api-client.ts`
   - Add configurable timeout
   - Improve error response parsing for structured error codes
   - On 401, redirect to sign-in page

4. **Update user types**
   - Ref: `frontend/types/user.ts`
   - Add name, email, role fields to UserSession
   - Fetch user details from `/auth/me` on mount

---

### Phase D: Production Hardening (P2 — Reliability)

**Goal**: Remove debug code, harden error handling, add test coverage.

**Changes**:

1. **Remove console.log statements**
   - Ref: `frontend/components/auth/auth-provider.tsx` — 10+ console.log calls with sensitive data
   - Search and remove all `console.log` in production-facing frontend code
   - Backend: verify no secrets logged (already uses structured logging)

2. **Security improvements**
   - Auth provider: add `SameSite=Lax` and `Secure` (production) to cookie
   - Remove hardcoded fallback secret (`"dev-secret-change-in-production"`) — require env var
   - Add input length validation on frontend forms (max 255 chars for email/name)

3. **Error handling**
   - Integrate toast component for API error display
   - Ensure all async operations in hooks have try/catch with user-facing messages
   - Verify error boundary catches rendering errors

4. **Backend tests**
   - `tests/conftest.py`: Test fixtures with async SQLite DB, FastAPI test client
   - `tests/test_auth.py`: Signup (valid, duplicate, weak password), signin (valid, wrong password, banned user)
   - `tests/test_tasks.py`: CRUD operations, authorization (can't access other user's tasks), filtering

5. **Frontend build verification**
   - Run `npm run build` to verify no TypeScript errors
   - Verify no console.log in production bundle

---

## Dependency Order

```
Phase A (Backend Security & Data)
  └──→ Phase C (Frontend-Backend Integration) — needs task API

Phase B (Frontend Responsive UI) — independent, can parallel with A

Phase C (Integration) — depends on A
  └──→ Phase D (Production Hardening) — depends on A + B + C
```

**Recommended execution**: A and B in parallel, then C, then D.

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| SHA-256 → bcrypt migration breaks existing users | Medium | High | Transparent re-hashing on login; keep SHA-256 verify as fallback |
| Task model type mismatch (UUID → str) with existing data | Low | Medium | New table, no data migration needed; fresh start |
| Responsive CSS changes break desktop layout | Medium | Medium | Test at all 3 breakpoints after each component change |
| Neon PostgreSQL connection issues in tests | Low | Low | Use async SQLite for tests; Neon for integration only |

## Acceptance Verification

After all phases complete, verify against spec success criteria:

- [x] **SC-001**: Registration flow < 60s on mobile — signup form with loading states, password strength indicator, responsive layout
- [x] **SC-002**: Sign-in flow < 30s on mobile — login form with isLoading, error banner, responsive
- [x] **SC-003**: All pages correct at 375px, 768px, 1440px — responsive breakpoints on all pages/components
- [x] **SC-004**: Task CRUD persists to Neon DB — full CRUD via /api/v1/tasks with SQLAlchemy ORM
- [x] **SC-005**: API errors show user-friendly messages — structured error responses + toast notifications + error banners
- [x] **SC-006**: Zero debug console.logs with sensitive data — verified: 0 console statements in frontend source
- [x] **SC-007**: Backend tests pass for auth + tasks — test_auth.py (12 tests) + test_tasks.py (14 tests)
- [x] **SC-008**: App starts in production mode with env vars only — BETTER_AUTH_SECRET validated, no hardcoded secrets
