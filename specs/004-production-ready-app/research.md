# Research: 004-production-ready-app

**Date**: 2026-02-08
**Branch**: `004-production-ready-app`
**Spec**: [spec.md](./spec.md)

## Research Tasks & Findings

### R1: Password Hashing — Replace SHA-256

**Context**: Current implementation in `backend/app/routers/auth.py:37-51` uses SHA-256 with salt. SHA-256 is a fast hash designed for data integrity, not password storage. It lacks a work factor, making it vulnerable to brute-force and rainbow table attacks.

**Decision**: Replace SHA-256 with **bcrypt** via the `passlib` library.

**Rationale**:
- bcrypt is purpose-built for password hashing with adaptive cost factor
- `passlib[bcrypt]` is the standard Python library for this, already compatible with FastAPI
- Default work factor of 12 rounds provides ~250ms per hash — slow enough to resist brute force, fast enough for user experience
- Existing password hashes (SHA-256 format `salt:hash`) must be migrated: on next successful login, re-hash with bcrypt transparently

**Alternatives considered**:
- **Argon2**: Newer, memory-hard. Excellent security but requires `argon2-cffi` dependency and is less commonly deployed. Overkill for this iteration.
- **PBKDF2**: Available in Python stdlib via `hashlib.pbkdf2_hmac`. Acceptable but bcrypt is industry standard for web apps.
- **scrypt**: Memory-hard like Argon2. Less tooling support in Python ecosystem.

---

### R2: Task Model Integration — Unify ORM

**Context**: The Task model lives in `backend/src/models/task.py` using SQLModel, while all auth models use SQLAlchemy ORM in `backend/app/models/`. The Task model uses `uuid.UUID` for IDs while User model uses `str` (ULID/UUID strings). This creates a type mismatch for `task.user_id → user.id` foreign keys.

**Decision**: Migrate the Task model to SQLAlchemy ORM in `backend/app/models/task.py`, using `str` (Text) for IDs to match the User model convention.

**Rationale**:
- Single ORM approach reduces complexity and ensures consistent session/transaction management
- Matching ID types (str) avoids foreign key type mismatches with Neon PostgreSQL
- The existing Task CRUD router in `backend/src/api/v1/tasks.py` provides the logic pattern but must be rewritten to use the new model and async session patterns from `app/`
- Alembic migrations can handle the schema change

**Alternatives considered**:
- **Keep SQLModel alongside SQLAlchemy**: Creates two competing session factories and migration paths. Rejected for complexity.
- **Convert all models to SQLModel**: Would require rewriting auth models and breaking Better-Auth schema compatibility. Too risky.

---

### R3: Frontend JWT Storage — Security Improvement

**Context**: Current implementation stores JWT in `localStorage` (XSS vulnerable) and sets a cookie without `HttpOnly` or `Secure` flags. The cookie is set via `document.cookie` in JavaScript.

**Decision**: Keep the hybrid approach (localStorage + cookie) but add security improvements:
1. Remove sensitive data from console.log statements
2. Add `SameSite=Lax` to cookie
3. Add `Secure` flag in production
4. The middleware already reads from cookies for SSR route protection — this pattern is adequate

**Rationale**:
- Moving to HttpOnly cookies requires backend changes (Set-Cookie headers) and a proxy/BFF pattern, which is out of scope for this iteration
- The primary attack vector (XSS) is mitigated by Next.js built-in XSS protection and React's auto-escaping
- Removing console.log statements with tokens is the most impactful quick win
- Future iteration should implement HttpOnly cookie-based auth with a backend-for-frontend pattern

**Alternatives considered**:
- **HttpOnly cookies only**: Requires backend to set cookies, frontend proxy for API calls. Significant architecture change. Deferred.
- **In-memory only**: Loses auth state on page refresh. Poor UX. Rejected.

---

### R4: Frontend Responsive Design — Approach

**Context**: The frontend has partial responsive design. Some components (login-form, dashboard) use responsive Tailwind utilities, but others (task-form, task detail) have fixed layouts. The CSS design system in `globals.css` has breakpoints defined but not consistently applied.

**Decision**: Enhance existing Tailwind-based responsive approach with a mobile-first strategy:
1. Audit and fix all pages at 375px, 768px, and 1440px breakpoints
2. Ensure consistent use of Tailwind responsive prefixes (`sm:`, `md:`, `lg:`)
3. Leverage existing CSS design tokens (spacing, typography) from `globals.css`
4. Add responsive navigation (mobile hamburger menu or collapsible nav)
5. Ensure all touch targets are minimum 44px

**Rationale**:
- Tailwind CSS is already in place with responsive utilities
- The design token system in globals.css provides a solid foundation
- Mobile-first ensures smallest screens work first, then enhance for larger
- No additional CSS framework needed

**Alternatives considered**:
- **CSS-in-JS (styled-components)**: Would add dependency and change styling approach. Rejected.
- **CSS Modules**: Good isolation but Tailwind already handles this with utility classes. Unnecessary.

---

### R5: Task API Endpoints — Backend Router Design

**Context**: A task router exists in `backend/src/api/v1/tasks.py` but is not registered in the main FastAPI app (`backend/app/main.py`). The main app only includes auth and users routers. The existing task router uses SQLModel patterns incompatible with the app's async session factory.

**Decision**: Create a new task router at `backend/app/routers/tasks.py` following the same patterns as the existing auth and users routers:
1. Use async session dependency from `app/database.py`
2. Use auth dependency chain from `app/utils/dependencies.py`
3. Support CRUD + filtering + pagination
4. Scope all queries to the authenticated user's ID
5. Register in `app/main.py`

**Rationale**:
- Consistency with existing router patterns ensures maintainability
- The auth dependency chain already handles JWT verification and user loading
- The existing task router logic provides a reference but must be adapted for the async SQLAlchemy patterns used in `app/`

**Alternatives considered**:
- **Import and adapt existing src/ router**: Would require bridging two ORM systems in one request. Rejected.
- **GraphQL for task operations**: Overhead for a CRUD-focused feature. REST is simpler and sufficient.

---

### R6: CORS and Production Configuration

**Context**: CORS is currently hardcoded to `http://localhost:3000,http://127.0.0.1:3000`. The `ALLOWED_ORIGINS` setting in config.py reads from environment but defaults to localhost. Production needs the actual frontend domain.

**Decision**: Make CORS fully environment-driven:
1. `ALLOWED_ORIGINS` env var is already the mechanism — ensure no hardcoded fallback to localhost in production
2. Add validation: if `ENVIRONMENT=production` and `ALLOWED_ORIGINS` contains `localhost`, log a warning
3. Ensure the frontend `NEXT_PUBLIC_API_BASE_URL` is also configurable per environment

**Rationale**:
- The mechanism already exists; it just needs hardening
- No code architecture change needed, just configuration discipline

---

### R7: Error Handling — Frontend Error Boundary

**Context**: An error boundary component exists at `frontend/components/ui/error-boundary.tsx` but is a basic class component. It only catches rendering errors, not async/network errors. It's not wrapped around the app layout.

**Decision**:
1. Wrap the root layout with the existing ErrorBoundary component
2. Enhance the error boundary with better styling matching the app's design system
3. Add a toast/notification system for async error display (API failures, network errors)
4. Enhance the API client to provide structured error messages

**Rationale**:
- The error boundary already exists — just needs to be used and enhanced
- Toast notifications are the standard UX pattern for transient API errors
- The API client already has error parsing logic that can be improved

---

### R8: Testing Strategy

**Context**: Backend has `requirements-dev.txt` with pytest, pytest-asyncio, pytest-cov. Frontend has no testing dependencies in package.json. No existing test files were found (except `backend/test_signup.py` which appears to be a manual test script).

**Decision**:
1. **Backend**: Write pytest-asyncio tests for critical paths (auth signup/signin, task CRUD, JWT verification)
2. **Frontend**: Defer comprehensive frontend testing to a future iteration. Focus on manual testing at the three viewport breakpoints.
3. **Integration**: Write a small set of integration tests that verify the full auth flow (signup → get token → create task → list tasks)

**Rationale**:
- Backend tests provide the most value-per-effort for production readiness
- Frontend testing requires additional setup (jest, testing-library) which is not in current dependencies
- The spec requires "critical paths have automated test coverage" — backend auth + task CRUD are the critical paths

**Alternatives considered**:
- **Full E2E with Playwright/Cypress**: High setup cost, fragile tests. Deferred to future iteration.
- **Frontend unit tests with Jest**: Would need to add jest, @testing-library/react, configure with Next.js. Can be done but lower priority than backend tests.

---

## Summary of Decisions

| # | Topic | Decision | Impact |
| --- | ----- | -------- | ------ |
| R1 | Password hashing | bcrypt via passlib | Critical security fix |
| R2 | Task model | Migrate to SQLAlchemy ORM, str IDs | Unifies data layer |
| R3 | JWT storage | Keep hybrid, remove debug logs, add cookie flags | Security hardening |
| R4 | Responsive design | Mobile-first Tailwind audit | UX improvement |
| R5 | Task API | New router in app/routers/tasks.py | Backend integration |
| R6 | CORS/config | Environment-driven, production validation | Production readiness |
| R7 | Error handling | Error boundary + toast notifications | UX reliability |
| R8 | Testing | Backend pytest for auth + tasks | Quality assurance |
