---
description: "Task list for frontend implementation of Todo Web Application"
---

# Tasks: Todo Frontend Application

**Input**: Design documents from `/specs/001-todo-frontend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend project**: `frontend/` at repository root
- Paths shown below follow the structure defined in plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize Next.js 16+ project with TypeScript using `npx create-next-app@16.0.10`
- [X] T002 [P] Install required dependencies: better-auth, tailwindcss, swr, react-query, @types/node
- [X] T003 Configure Tailwind CSS for styling according to plan.md requirements

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Setup TypeScript configuration and type definitions structure per plan.md
- [X] T005 [P] Implement authentication context/provider in frontend/components/auth/auth-provider.tsx (required by FR-001, FR-002)
- [X] T006 [P] Setup API service abstraction layer in frontend/lib/api/api-client.ts (required by all API calls)
- [X] T007 Create base types for Task and User Session in frontend/types/task.ts and frontend/types/user.ts (from data-model.md)
- [X] T008 Configure Next.js middleware for authentication in frontend/middleware.ts (required by FR-001, FR-002)
- [X] T009 Setup global CSS and layout structure in frontend/app/layout.tsx and frontend/app/globals.css

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication and Task Creation (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to securely sign in and create new tasks with title, description, due date, and priority level (from spec US1)

**Independent Test**: Can be fully tested by signing in, creating a task with all required fields, and verifying the task appears in the user's task list. Delivers core value of being able to capture tasks.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for POST /api/tasks endpoint in frontend/__tests__/contract/task-api.test.ts
- [ ] T011 [P] [US1] Integration test for user authentication flow in frontend/__tests__/integration/auth-flow.test.ts

### Implementation for User Story 1

- [X] T012 [P] [US1] Create login form component in frontend/components/auth/login-form.tsx (required by FR-001)
- [X] T013 [P] [US1] Create sign-in page in frontend/app/(auth)/sign-in/page.tsx (required by FR-001)
- [X] T014 [P] [US1] Create register form component in frontend/components/auth/register-form.tsx (required by FR-001)
- [X] T015 [US1] Create sign-up page in frontend/app/(auth)/sign-up/page.tsx (required by FR-001)
- [X] T016 [P] [US1] Implement auth client utilities in frontend/lib/auth/auth-client.ts (required by FR-001, FR-002)
- [X] T017 [US1] Create task creation form component in frontend/components/tasks/task-form.tsx (required by FR-003)
- [X] T018 [US1] Create task service in frontend/lib/api/task-service.ts for POST /api/tasks (required by FR-003, FR-005)
- [X] T019 [US1] Create task creation page in frontend/app/tasks/create/page.tsx (required by FR-003)
- [X] T020 [US1] Create dashboard page in frontend/app/dashboard/page.tsx to show user's task list (required by acceptance scenario 1)
- [X] T021 [US1] Implement JWT token storage and retrieval in auth context (required by FR-002, FR-008)
- [X] T022 [US1] Add auth hook in frontend/hooks/use-auth.ts for authentication state (required by FR-001, FR-002)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management and Visualization (Priority: P2)

**Goal**: Allow authenticated users to view, filter, sort, update, and delete their tasks with visual indicators for priority levels based on Eisenhower Matrix (from spec US2)

**Independent Test**: Can be fully tested by creating multiple tasks with different priority levels, viewing them in the list with appropriate visual indicators, and performing update/delete operations. Delivers value of organizing and managing tasks efficiently.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T023 [P] [US2] Contract test for GET /api/tasks endpoint in frontend/__tests__/contract/task-api.test.ts
- [ ] T024 [P] [US2] Integration test for task visualization in frontend/__tests__/integration/task-visualization.test.ts

### Implementation for User Story 2

- [X] T025 [P] [US2] Create task card component in frontend/components/tasks/task-card.tsx with priority indicators (required by FR-004)
- [X] T026 [P] [US2] Create priority badge component in frontend/components/tasks/priority-badge.tsx for visual indicators (required by FR-004)
- [X] T027 [US2] Create task list component in frontend/components/tasks/task-list.tsx to display tasks (required by FR-005)
- [X] T028 [US2] Implement update task functionality in task service frontend/lib/api/task-service.ts for PUT /api/tasks/{id} (required by FR-005)
- [X] T029 [US2] Create individual task view/edit page in frontend/app/tasks/[id]/page.tsx (required by FR-005)
- [X] T030 [US2] Implement task deletion functionality in task service for DELETE /api/tasks/{id} (required by FR-005)
- [X] T031 [US2] Add task completion toggle in PATCH /api/tasks/{id}/complete endpoint implementation (required by FR-005)
- [X] T032 [US2] Create task priority helpers in frontend/lib/utils/priority-helpers.ts for matrix visualization (required by FR-004)
- [X] T033 [US2] Update dashboard to show all user tasks with priority visual indicators (required by acceptance scenario 1)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Advanced Task Operations (Priority: P3)

**Goal**: Allow authenticated users to filter, sort, and perform advanced operations on their tasks including marking complete/incomplete and deleting tasks (from spec US3)

**Independent Test**: Can be fully tested by filtering tasks by priority, due date, or completion status, and performing update/delete operations. Delivers value of better task organization and management.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T034 [P] [US3] Contract test for query parameters on GET /api/tasks in frontend/__tests__/contract/task-api.test.ts
- [ ] T035 [P] [US3] Integration test for task filtering and sorting in frontend/__tests__/integration/task-filtering.test.ts

### Implementation for User Story 3

- [X] T036 [P] [US3] Create task filters component in frontend/components/tasks/task-filters.tsx for priority/due date/completion filtering (required by FR-006)
- [X] T037 [P] [US3] Enhance task service with filtering and sorting options in frontend/lib/api/task-service.ts (required by FR-006)
- [X] T038 [US3] Add date formatting utilities in frontend/lib/utils/date-formatter.ts for due date handling (required by FR-003)
- [X] T039 [US3] Update task list component to support sorting by priority, due date, and completion status (required by FR-006)
- [X] T040 [US3] Implement optimistic UI updates in task hooks for better UX (required by FR-005)
- [X] T041 [US3] Add error handling for 401 responses and token expiration in auth context (required by FR-008)
- [X] T042 [US3] Create use-tasks hook in frontend/hooks/use-tasks.ts for task state management (required by FR-005, FR-006)

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T043 [P] Responsive styling updates across all components to ensure mobile/desktop compatibility (required by FR-009)
- [X] T044 Error boundary implementation for graceful error handling throughout the app
- [X] T045 Loading and empty state components for better UX
- [X] T046 Theme provider setup in frontend/components/providers/theme-provider.tsx for consistent styling (required by FR-009)
- [ ] T047 Performance optimizations and code splitting
- [X] T048 Update frontend/app/tasks/page.tsx to integrate all task management features
- [X] T049 Security hardening for JWT handling and API communications (required by FR-002, FR-007, FR-008)
- [ ] T050 Run quickstart validation from quickstart.md to ensure all works as expected

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds upon US1 components
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds upon US1/US2 components

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models/types before services
- Services before UI components
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, user stories can proceed in priority order
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different components within a user story marked [P] can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence