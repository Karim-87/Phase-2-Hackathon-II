# Tasks: Production-Ready App Enhancement

**Input**: Design documents from `specs/004-production-ready-app/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/api-contract.md

**Tests**: Backend tests are included per spec requirement SC-007 ("critical paths have automated test coverage"). Frontend tests are deferred per research decision R8.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/`, `backend/tests/`, `backend/alembic/`
- **Frontend**: `frontend/app/`, `frontend/components/`, `frontend/lib/`, `frontend/hooks/`, `frontend/types/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add new dependencies and prepare project structure for feature work

- [x] T001 Add `passlib[bcrypt]>=1.7.4` to `backend/requirements.txt` and install
- [x] T002 [P] Create `backend/app/models/task.py` — empty file with module docstring placeholder
- [x] T003 [P] Create `backend/app/schemas/task.py` — empty file with module docstring placeholder
- [x] T004 [P] Create `backend/app/routers/tasks.py` — empty file with module docstring placeholder
- [x] T005 [P] Create `backend/tests/conftest.py` — test fixtures: async SQLite engine, async session factory, FastAPI TestClient with httpx.AsyncClient, test user creation helper, JWT token generation helper
- [x] T006 [P] Create `frontend/components/ui/toast.tsx` — Toast notification component with auto-dismiss, error/success/info variants, positioned top-right, uses design tokens from globals.css

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core changes that MUST be complete before user story work begins

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Upgrade password hashing in `backend/app/routers/auth.py` — replace `hash_password()` (lines 37-43) and `verify_password()` (lines 45-51) with bcrypt via passlib. New `hash_password()` uses `CryptContext(schemes=["bcrypt"], deprecated="auto")`. New `verify_password()` checks bcrypt first; if hash format is `salt:hash` (legacy SHA-256), verify with old method, re-hash to bcrypt, and update Account.password in DB. Keep old functions as `_legacy_verify_sha256()` fallback
- [x] T008 Add password strength validation to signup endpoint in `backend/app/routers/auth.py` — add `validate_password()` function: min 8 chars, 1 uppercase, 1 lowercase, 1 number. Call before `hash_password()` in signup handler (around line 105). Return 422 with `error_code: "VALIDATION_ERROR"` and details dict if invalid. Update `backend/app/schemas/user.py` UserCreate to add `@field_validator("password")` with same rules
- [x] T009 Remove hardcoded JWT secret fallback in `backend/app/routers/auth.py` — replace `settings.BETTER_AUTH_SECRET or "dev-secret-change-in-production"` (line 66) with `settings.BETTER_AUTH_SECRET`. Add startup validation in `backend/app/config.py`: if `ENVIRONMENT == "production"` and `BETTER_AUTH_SECRET` is empty/default, raise `ValueError`
- [x] T010 Add production CORS validation in `backend/app/config.py` — in `Settings` class, add a `model_post_init` or `@model_validator` that logs a WARNING if `ENVIRONMENT == "production"` and any origin in `ALLOWED_ORIGINS` contains "localhost" or "127.0.0.1"
- [x] T011 Enhance `frontend/components/ui/loading-spinner.tsx` — accept `size` prop (sm=16px, md=32px, lg=48px) and `color` prop (defaults to `blue-600`). Export as named and default export
- [x] T012 Enhance `frontend/components/ui/modern-button.tsx` — add `isLoading` prop: when true, show LoadingSpinner (sm) inline before children text, disable button, reduce opacity. Add `disabled` visual state styling
- [x] T013 Enhance `frontend/components/ui/error-boundary.tsx` — modernize fallback UI: use design tokens from globals.css, show error icon, "Something went wrong" heading, descriptive text, and styled "Try again" button using ModernButton component. Add `onReset` callback prop

**Checkpoint**: Foundation ready — password hashing upgraded, validation in place, UI components enhanced. User story implementation can now begin.

---

## Phase 3: User Story 1 — Secure Account Registration and Sign-In (Priority: P1) MVP

**Goal**: Upgrade auth security, improve sign-in/sign-up UX with loading states, password strength feedback, and proper error display. Users can register and sign in securely with data stored in Neon PostgreSQL.

**Independent Test**: Create a new account with name/email/password → verify redirect to dashboard → sign out → sign back in → verify dashboard loads. Test with weak password → verify rejection. Test with duplicate email → verify error message.

### Tests for User Story 1

- [x] T014 [P] [US1] Create auth tests in `backend/tests/test_auth.py` — test cases: (1) POST /auth/signup with valid data returns 201 + token, (2) POST /auth/signup with duplicate email returns 400, (3) POST /auth/signup with weak password (no uppercase) returns 422, (4) POST /auth/signup with short password (<8 chars) returns 422, (5) POST /auth/signin with valid credentials returns 200 + token, (6) POST /auth/signin with wrong password returns 401, (7) POST /auth/signin with nonexistent email returns 401 (same message), (8) GET /auth/me with valid token returns user profile, (9) GET /auth/me without token returns 401. Use fixtures from conftest.py

### Implementation for User Story 1

- [x] T015 [US1] Add `isLoading` state to login form in `frontend/components/auth/login-form.tsx` — set true on submit, false on success/error. Pass `isLoading` to submit ModernButton. Show error message in styled error banner (red bg, border, icon). Ensure form is responsive: full-width at 375px with `px-4`, max-w-md centered on desktop
- [x] T016 [US1] Add password strength indicator and loading state to register form in `frontend/components/auth/register-form.tsx` — add real-time password strength bar below password input (weak=red, fair=yellow, strong=green) checking: length>=8, uppercase, lowercase, number. Set `isLoading` on submit button. Show validation errors inline below fields. Ensure responsive: same layout as login form
- [x] T017 [US1] Remove all `console.log` statements from `frontend/components/auth/auth-provider.tsx` — remove lines with `console.log('SignIn:`, `console.log('Signup`, `console.log('Attempting signup`, `console.error` that log sensitive data (tokens, payloads). Keep `console.error` for actual error reporting but strip token/password data from logged objects
- [x] T018 [US1] Add cookie security flags in `frontend/components/auth/auth-provider.tsx` — update both cookie set calls (signIn line 92 and signUp line 145) to include `SameSite=Lax`. Add `Secure` flag conditionally when `window.location.protocol === 'https:'`. Format: `jwt_token=${token}; path=/; max-age=86400; SameSite=Lax${isSecure ? '; Secure' : ''}`
- [x] T019 [US1] Update `frontend/types/user.ts` — expand `UserSession` interface to include `name?: string`, `email?: string`, `role?: string` fields. Update `auth-provider.tsx` to call `GET /auth/me` after sign-in/sign-up to populate full user profile (name, email, role) into the user state

**Checkpoint**: User Story 1 complete. Users can register with password validation, sign in securely with bcrypt hashing, see loading states, and get clear error messages. Auth flows work end-to-end with Neon DB.

---

## Phase 4: User Story 2 — Responsive and Polished User Interface (Priority: P1)

**Goal**: Make every page fully responsive at 375px (mobile), 768px (tablet), and 1440px (desktop). Ensure proper loading states, visual feedback, and consistent design.

**Independent Test**: Open every page at 375px, 768px, and 1440px viewports. Verify: no horizontal scrolling, all buttons >=44px, text readable, forms usable, loading spinners shown during async operations, error boundaries catch render errors.

### Implementation for User Story 2

- [x] T020 [US2] Wrap root layout with ErrorBoundary in `frontend/app/layout.tsx` — import ErrorBoundary, wrap `{children}` inside `<ErrorBoundary>`. Ensure proper viewport meta tag exists in html head
- [x] T021 [US2] Make home page responsive in `frontend/app/page.tsx` — hero text: use `text-2xl sm:text-3xl md:text-4xl` for heading. CTA buttons: stack vertically on mobile (`flex-col`), side-by-side on tablet+ (`sm:flex-row`). Add proper spacing with `gap-3 sm:gap-4`. Ensure min-h-[80vh] works on mobile
- [x] T022 [US2] Overhaul dashboard responsiveness in `frontend/app/dashboard/page.tsx` — mobile (375px): single-column layout, filters in collapsible section or horizontal scroll, task cards full-width. Tablet (768px): two-column task grid `md:grid-cols-2`. Desktop (1440px): task grid with `lg:grid-cols-3`, max-w-7xl container. Replace `"Loading..."` text with `<LoadingSpinner size="lg" />`. Add proper empty state with icon and "Create your first task" CTA button
- [x] T023 [P] [US2] Make task list page responsive in `frontend/app/tasks/page.tsx` — same responsive grid pattern as dashboard. Filter controls: stack on mobile, inline row on tablet+. Replace loading text with LoadingSpinner. Add error state display with retry button
- [x] T024 [P] [US2] Make task creation page responsive in `frontend/app/tasks/create/page.tsx` — full-width form on mobile with `px-4`, max-w-2xl on desktop. Add loading state to submit button. Add error banner for failed submissions. Back button visible at all sizes
- [x] T025 [P] [US2] Make task detail page responsive in `frontend/app/tasks/[id]/page.tsx` — full-width on mobile with `px-4`, max-w-2xl centered on desktop. Replace `confirm()` delete dialog with styled confirmation modal using ModernButton (danger variant). Replace "Loading task..." with LoadingSpinner. Priority badge and action buttons: stack on mobile, inline on tablet+
- [x] T026 [US2] Make task form responsive in `frontend/components/tasks/task-form.tsx` — inputs full-width on mobile, two-column layout on tablet+ for date/priority row (`md:grid-cols-2`). Labels above inputs (not inline). Submit and cancel buttons: full-width stacked on mobile, side-by-side on tablet+ (`sm:flex-row`). Add loading state to submit button
- [x] T027 [P] [US2] Make task filters responsive in `frontend/components/tasks/task-filters.tsx` — on mobile: stack vertically with full-width selects. On tablet+: horizontal row `md:grid-cols-4`. Active filter indicator (badge count or highlight). Reset button: always visible
- [x] T028 [P] [US2] Make task card responsive in `frontend/components/tasks/task-card.tsx` — action buttons (edit, delete, complete): icon-only on mobile, icon+text on tablet+. Ensure tap targets >= 44px. Title truncation with `truncate` class. Due date and priority badge: wrap below title on mobile, inline on tablet+

**Checkpoint**: User Story 2 complete. All pages render correctly at 375px, 768px, and 1440px. Loading spinners, error boundaries, and visual feedback are consistent across the application.

---

## Phase 5: User Story 3 — Seamless Frontend-Backend Task Management (Priority: P2)

**Goal**: Full task CRUD operations through the frontend, persisted to backend Neon database. Server-side filtering, proper error handling, and loading states for every operation.

**Independent Test**: Sign in → create task with all fields → see it in list → edit title and priority → mark complete → verify visual change → delete task → verify removed. Refresh page → verify persistence. Disconnect backend → attempt operation → verify error message with retry option.

### Tests for User Story 3

- [x] T029 [P] [US3] Create task CRUD tests in `backend/tests/test_tasks.py` — test cases: (1) POST /tasks with valid data returns 201 + task, (2) GET /tasks returns only authenticated user's tasks, (3) GET /tasks with priority filter returns filtered results, (4) GET /tasks/{id} returns task owned by user, (5) GET /tasks/{id} for other user's task returns 404, (6) PATCH /tasks/{id} updates fields and returns updated task, (7) DELETE /tasks/{id} returns success and task is gone, (8) All endpoints return 401 without token. Use fixtures from conftest.py

### Implementation for User Story 3

- [x] T030 [US3] Create Task model in `backend/app/models/task.py` — SQLAlchemy ORM model per data-model.md: Text PK (generate UUID string), FK to user.id with CASCADE delete, title (Text, NOT NULL), description (Text, nullable), due_datetime (DateTime with tz, nullable), priority (Text, NOT NULL), is_completed (Boolean, default False), created_at, updated_at with server defaults. Add indexes: user_id, composite (user_id, is_completed). Add `user` relationship back_populates="tasks"
- [x] T031 [US3] Add tasks relationship to User model in `backend/app/models/user.py` — add `tasks: Mapped[List["Task"]] = relationship("Task", back_populates="user", cascade="all, delete-orphan")`. Import Task in `backend/app/models/__init__.py`
- [x] T032 [US3] Create Task schemas in `backend/app/schemas/task.py` — Pydantic v2 models per api-contract.md: `TaskCreate` (title required max 255, description optional max 5000, due_datetime optional, priority required as enum), `TaskRead` (all fields with `from_attributes=True`), `TaskUpdate` (all optional), `TaskListResponse` (tasks list + total_count + limit + offset in data envelope)
- [x] T033 [US3] Create Task router in `backend/app/routers/tasks.py` — per api-contract.md: `GET /tasks` (list with query params: priority, is_completed, sort_by, sort_order, limit, offset — all scoped to current user), `POST /tasks` (create, assign user_id from auth), `GET /tasks/{task_id}` (get by ID, verify ownership), `PATCH /tasks/{task_id}` (partial update, verify ownership), `DELETE /tasks/{task_id}` (delete, verify ownership). Use `get_active_user` dependency. Use SuccessResponse envelope from common.py. Register router with prefix `/tasks` and tags=["tasks"]
- [x] T034 [US3] Register task router in `backend/app/main.py` — add `from app.routers import tasks` and `app.include_router(tasks.router, prefix=settings.API_V1_PREFIX)`. Import Task model in `backend/app/database.py` init_db function
- [x] T035 [US3] Create Alembic migration for Task table — run `alembic revision --autogenerate -m "add_task_table"` from backend directory. Verify generated migration has correct columns, indexes, and foreign key. Test with `alembic upgrade head`
- [x] T036 [US3] Align task service with new API in `frontend/lib/api/task-service.ts` — update all methods to use `/api/v1/tasks` endpoint pattern. Update response parsing to unwrap `data` envelope: `getAllTasks()` reads `response.data.tasks`, `createTask()` reads `response.data`, etc. Add TypeScript return types matching Task interface. Add `getTasksWithFilters(params)` that builds query string from filter object
- [x] T037 [US3] Update API client in `frontend/lib/api/api-client.ts` — add 10-second timeout via AbortController. Improve error parsing: extract `error` and `error_code` from response body. On 401: clear localStorage token, clear cookie, redirect to `/sign-in` via `window.location.href`. Add structured error type: `ApiError { message: string, code?: string, status: number }`
- [x] T038 [US3] Update useTasks hook in `frontend/hooks/use-tasks.ts` — replace client-side filtering with server-side: `applyFilters()` calls `taskService.getTasksWithFilters(filterParams)` instead of local array operations. Add per-operation loading states: `isCreating`, `isUpdating`, `isDeleting` booleans. Add `retryLastOperation()` function that re-executes the last failed call. Update `fetchTasks()` to accept optional filter params
- [x] T039 [US3] Integrate toast notifications for task errors — import Toast component in `frontend/app/dashboard/page.tsx` and `frontend/app/tasks/page.tsx`. Show toast on task operation failure (create, update, delete) with error message from API. Show success toast on task creation. Wire toast dismiss to auto-clear after 5 seconds

**Checkpoint**: User Story 3 complete. Full task CRUD works end-to-end: create, read, update, delete with server-side filtering. All operations persist to Neon DB. Errors show user-friendly toasts with retry options.

---

## Phase 6: User Story 4 — Production Readiness and Reliability (Priority: P2)

**Goal**: Remove debug code, harden security, add backend test coverage for critical paths, verify production build succeeds.

**Independent Test**: Run backend tests → all pass. Run `npm run build` in frontend → no errors. Search frontend build for `console.log` with sensitive data → zero found. Start app with production env vars → verify it serves requests.

### Implementation for User Story 4

- [x] T040 [US4] Remove all remaining `console.log` statements from frontend production code — search all files in `frontend/` for `console.log` and `console.error`. Remove debug logging from: `auth-provider.tsx` (already done in T017 if so, verify), `api-client.ts`, `task-service.ts`, `use-tasks.ts`, any page components. Keep only error logging in error-boundary.tsx with sanitized data (no tokens/passwords)
- [x] T041 [P] [US4] Add input length validation to frontend auth forms — in `login-form.tsx`: add `maxLength={255}` to email input. In `register-form.tsx`: add `maxLength={255}` to email input, `maxLength={100}` to name input. Add client-side validation messages for exceeded lengths
- [x] T042 [P] [US4] Verify and fix backend exception handlers in `backend/app/utils/exceptions.py` — ensure all custom exceptions return `success: false` envelope with `error_code`. Ensure generic 500 handler never exposes stack traces or internal details in response body (only logs server-side). Verify `HTTPException` handler returns structured error response
- [x] T043 [US4] Write backend auth test suite in `backend/tests/test_auth.py` — if not already created in T014, create now with all test cases. Add additional tests: (10) signup with bcrypt verifies password hash format starts with `$2b$`, (11) legacy SHA-256 password is re-hashed to bcrypt on signin, (12) token expiration is properly set to 24 hours
- [x] T044 [US4] Write backend task test suite in `backend/tests/test_tasks.py` — if not already created in T029, create now with all test cases. Add additional tests: (9) create task with missing title returns 422, (10) create task with invalid priority returns 422, (11) filter by is_completed returns correct subset, (12) sort_by due_datetime returns ordered results
- [x] T045 [US4] Verify frontend production build — run `npm run build` in frontend directory. Fix any TypeScript errors. Verify no build warnings about missing environment variables. Confirm `next.config.js` properly exposes `NEXT_PUBLIC_API_BASE_URL`
- [x] T046 [US4] Final integration verification — start backend with `uvicorn app.main:app --port 8001`, start frontend with `npm run dev`. Test full flow: signup → dashboard → create task → edit → complete → delete → sign out → sign in. Test at 375px and 1440px viewports. Verify no console.log with sensitive data in browser dev tools

**Checkpoint**: User Story 4 complete. All backend tests pass. Frontend builds without errors. No sensitive debug logging. Application runs in production configuration.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup that spans all user stories

- [x] T047 [P] Update `backend/.env.example` with all required environment variables and documentation comments
- [x] T048 [P] Update `frontend/.env.example` (create if not exists) with `NEXT_PUBLIC_API_BASE_URL` and usage notes
- [x] T049 Run `specs/004-production-ready-app/quickstart.md` validation — follow each step in quickstart.md and verify it works. Fix any discrepancies
- [x] T050 Final acceptance verification — check off each item in plan.md Acceptance Verification section (SC-001 through SC-008)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 (T001 for bcrypt dep). BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Phase 2 completion. Can run in parallel with US2
- **US2 (Phase 4)**: Depends on Phase 2 completion (T011, T012, T013 for enhanced UI components). Can run in parallel with US1
- **US3 (Phase 5)**: Depends on Phase 2 completion. Backend tasks (T030-T035) can run in parallel with US1/US2. Frontend tasks (T036-T039) depend on backend task API being ready (T034)
- **US4 (Phase 6)**: Depends on US1 + US2 + US3 being complete
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (Auth)**: Independent after Phase 2. No dependency on other stories.
- **US2 (Responsive UI)**: Independent after Phase 2. No dependency on other stories. Can parallel with US1.
- **US3 (Task CRUD)**: Backend tasks independent. Frontend tasks need backend API (Phase 5 T030-T035 before T036-T039). Integration tasks need US1 auth working.
- **US4 (Production)**: Depends on US1 + US2 + US3. Tests validate all prior work.

### Within Each User Story

- Tests written first (if included), verified to fail
- Models → Schemas → Routers (backend)
- Service alignment → Hook update → Page integration (frontend)
- Cross-cutting (error handling, toasts) last within story

### Parallel Opportunities

**Phase 1** — All setup tasks T002-T006 can run in parallel.
**Phase 2** — T007 (bcrypt) and T011-T013 (UI components) can run in parallel. T008-T010 depend on T007 pattern.
**Phase 3 + Phase 4** — US1 and US2 can run entirely in parallel since they touch different files.
**Phase 5** — Backend tasks (T030-T035) can run in parallel with US1/US2 frontend work. Frontend tasks (T036-T039) are sequential within the story.
**Phase 6** — T040, T041, T042 can run in parallel. T043-T044 (tests) can run in parallel.

---

## Parallel Example: Phase 3 + Phase 4 (US1 + US2 in parallel)

```
# Stream A: User Story 1 (Auth)
Task T014: Write auth tests in backend/tests/test_auth.py
Task T015: Add loading to login form in frontend/components/auth/login-form.tsx
Task T016: Add password strength to register form in frontend/components/auth/register-form.tsx
Task T017: Remove console.logs from frontend/components/auth/auth-provider.tsx
Task T018: Add cookie security flags in frontend/components/auth/auth-provider.tsx
Task T019: Expand UserSession type in frontend/types/user.ts

# Stream B: User Story 2 (Responsive UI) — different files, no conflicts
Task T020: Wrap layout with ErrorBoundary in frontend/app/layout.tsx
Task T021: Responsive home page in frontend/app/page.tsx
Task T022: Responsive dashboard in frontend/app/dashboard/page.tsx
Task T023: Responsive task list in frontend/app/tasks/page.tsx
Task T024: Responsive task create in frontend/app/tasks/create/page.tsx
Task T025: Responsive task detail in frontend/app/tasks/[id]/page.tsx
Task T026: Responsive task form in frontend/components/tasks/task-form.tsx
Task T027: Responsive task filters in frontend/components/tasks/task-filters.tsx
Task T028: Responsive task card in frontend/components/tasks/task-card.tsx
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T013)
3. Complete Phase 3: User Story 1 — Secure Auth (T014-T019)
4. **STOP and VALIDATE**: Register, sign in, sign out. Verify bcrypt hashing, password validation, loading states.
5. Deploy/demo if ready — auth is the minimum viable product

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 (Auth) → Secure login works → Deploy (MVP!)
3. US2 (Responsive) → Polished UI on all devices → Deploy
4. US3 (Task CRUD) → Full task management end-to-end → Deploy
5. US4 (Production) → Tests pass, hardened → Production deploy
6. Polish → Final validation → Done

### Parallel Execution Strategy

With concurrent implementation capacity:
1. Complete Setup + Foundational together
2. Once Foundational is done:
   - Stream A: US1 (Auth) + US3 backend tasks (T030-T035)
   - Stream B: US2 (Responsive UI)
3. After US3 backend ready: US3 frontend tasks (T036-T039)
4. After US1 + US2 + US3: US4 (Production hardening)
5. Polish phase last

---

## Summary

| Phase | Story | Task Count | Parallel Tasks |
| ----- | ----- | ---------- | -------------- |
| Phase 1: Setup | — | 6 | 5 |
| Phase 2: Foundational | — | 7 | 3 |
| Phase 3: US1 Auth | P1 | 6 | 1 |
| Phase 4: US2 Responsive | P1 | 9 | 5 |
| Phase 5: US3 Task CRUD | P2 | 11 | 1 |
| Phase 6: US4 Production | P2 | 7 | 3 |
| Phase 7: Polish | — | 4 | 2 |
| **Total** | | **50** | **20** |

**MVP scope**: Phase 1 + Phase 2 + Phase 3 (US1) = 19 tasks
**Full scope**: All 50 tasks across 7 phases

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks in same phase
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable at its checkpoint
- Commit after each task or logical group of tasks
- Stop at any checkpoint to validate the story independently
- Backend and frontend tasks within a story follow: models → schemas → routers → services → hooks → pages
