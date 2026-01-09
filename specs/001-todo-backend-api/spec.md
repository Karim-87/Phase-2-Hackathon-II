# Feature Specification: Todo Backend API

**Feature Branch**: `001-todo-backend-api`
**Created**: 2026-01-09
**Status**: Draft
**Input**: User description: "You are the Backend Agent for the Multi-User Todo Web Application (Phase II Hackathon Project). You MUST strictly follow the Spec Constitution provided by the user (Last Updated: January 2026). This constitution is binding and non-negotiable. SCOPE (Backend Only): - FastAPI application - SQLModel ORM - Neon Serverless PostgreSQL - JWT-based authentication (shared secret with frontend) - uv for dependency & project management CORE RESPONSIBILITIES: 1. Provide secure RESTful APIs for task management 2. Enforce strict per-user data isolation using JWT 3. Validate and verify JWT tokens for every request 4. Persist data in Neon PostgreSQL using SQLModel 5. Follow clean backend architecture and separation of concerns API REQUIREMENTS: Base path: /api Endpoints (ALL require JWT auth): - POST   /api/tasks - GET    /api/tasks - GET    /api/tasks/{taskId} - PUT    /api/tasks/{taskId} - DELETE /api/tasks/{taskId} - PATCH  /api/tasks/{taskId}/complete SECURITY REQUIREMENTS: - JWT must be verified on every request - Invalid, missing, or expired tokens → HTTP 401 - User identity must be derived ONLY from JWT - user_id from JWT must be used to filter all DB queries - No endpoint may accept user_id from URL or body DATABASE REQUIREMENTS: Task model must include: - id - user_id (from JWT) - title - description - due_datetime - priority (Eisenhower Matrix compatible) - is_completed - created_at - updated_at TECHNICAL CONSTRAINTS: - Use environment variables: • NEON_DATABASE_URL • BETTER_AUTH_SECRET - Use async FastAPI where appropriate - No hardcoded secrets - No frontend or UI logic - No mock authentication OUTPUT EXPECTATION: - Project structure - Database models - JWT auth dependency/middleware - CRUD API endpoints - Input/output schemas - Error handling - Clear inline comments referencing this constitution User isolation is NON-NEGOTIABLE."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Task Management API (Priority: P1)

Authenticated users can securely create, read, update, and delete their own tasks through a RESTful API. The system enforces user isolation by using JWT tokens to identify the user and restrict access to their own data only.

**Why this priority**: This is the core functionality that enables the entire todo application to work. Without a secure API for task management, the frontend cannot function properly.

**Independent Test**: Can be fully tested by authenticating with a JWT token, creating a task, retrieving it, updating it, and deleting it. The system should only allow access to tasks belonging to the authenticated user.

**Acceptance Scenarios**:

1. **Given** a user with a valid JWT token, **When** they POST to /api/tasks with valid task data, **Then** a new task is created for that user and returned with HTTP 201
2. **Given** a user with a valid JWT token and existing tasks, **When** they GET /api/tasks, **Then** only tasks belonging to that user are returned with HTTP 200
3. **Given** a user with a valid JWT token and an existing task they own, **When** they GET /api/tasks/{taskId}, **Then** the specific task is returned with HTTP 200
4. **Given** a user with a valid JWT token and an existing task they own, **When** they PUT /api/tasks/{taskId} with updated data, **Then** the task is updated and returned with HTTP 200

---

### User Story 2 - Task Completion and Deletion (Priority: P2)

Authenticated users can mark their tasks as complete/incomplete and delete their tasks through dedicated API endpoints. The system ensures users can only modify tasks they own.

**Why this priority**: This provides essential task management functionality that allows users to track their progress and clean up completed tasks.

**Independent Test**: Can be fully tested by authenticating with a JWT token, creating a task, marking it as complete/incomplete, and deleting it. The system should reject attempts to modify tasks owned by other users.

**Acceptance Scenarios**:

1. **Given** a user with a valid JWT token and an existing task they own, **When** they PATCH /api/tasks/{taskId}/complete with {completed: true}, **Then** the task is marked as completed and returned with HTTP 200
2. **Given** a user with a valid JWT token and an existing task they own, **When** they DELETE /api/tasks/{taskId}, **Then** the task is deleted and HTTP 204 is returned

---

### User Story 3 - Secure Authentication and Error Handling (Priority: P3)

The system validates JWT tokens on every request and properly handles various error conditions, ensuring security and reliability.

**Why this priority**: This ensures the security and robustness of the API, preventing unauthorized access and providing clear feedback for error conditions.

**Independent Test**: Can be fully tested by making requests with invalid/missing/expired JWT tokens and observing that appropriate 401 responses are returned.

**Acceptance Scenarios**:

1. **Given** a request with no JWT token, **When** any API endpoint is accessed, **Then** HTTP 401 Unauthorized is returned
2. **Given** a request with an invalid/expired JWT token, **When** any API endpoint is accessed, **Then** HTTP 401 Unauthorized is returned
3. **Given** a user with a valid JWT token attempting to access another user's task, **When** GET /api/tasks/{otherUserTaskId} is accessed, **Then** HTTP 404 Not Found is returned

---

### Edge Cases

- What happens when a user attempts to access a task that exists but belongs to another user? (Should return 404 to maintain privacy)
- How does system handle malformed JWT tokens? (Should return 401)
- What happens when database connection fails? (Should return appropriate 5xx error)
- How does system handle concurrent updates to the same task? (Should handle gracefully with proper transaction management)
- What happens when a user tries to update a task with invalid data? (Should return 422 with validation errors)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST validate JWT tokens on every API request and reject invalid/missing/expired tokens with HTTP 401
- **FR-002**: System MUST derive user identity exclusively from JWT token and use user_id from JWT to filter all database queries
- **FR-003**: System MUST enforce user data isolation by ensuring users can only access their own tasks
- **FR-004**: System MUST provide POST endpoint at /api/tasks to create new tasks with title, description, due_datetime, priority, and is_completed fields
- **FR-005**: System MUST provide GET endpoint at /api/tasks to retrieve all tasks belonging to the authenticated user with optional filtering and sorting
- **FR-006**: System MUST provide GET endpoint at /api/tasks/{taskId} to retrieve a specific task belonging to the authenticated user
- **FR-007**: System MUST provide PUT endpoint at /api/tasks/{taskId} to update an existing task belonging to the authenticated user
- **FR-008**: System MUST provide DELETE endpoint at /api/tasks/{taskId} to delete a task belonging to the authenticated user
- **FR-009**: System MUST provide PATCH endpoint at /api/tasks/{taskId}/complete to update only the completion status of a task
- **FR-010**: System MUST persist task data in Neon Serverless PostgreSQL database using SQLModel ORM
- **FR-011**: System MUST store task data with required fields: id, user_id (from JWT), title, description, due_datetime, priority, is_completed, created_at, updated_at
- **FR-012**: System MUST use environment variables NEON_DATABASE_URL and BETTER_AUTH_SECRET for configuration
- **FR-013**: System MUST implement proper error handling and return appropriate HTTP status codes
- **FR-014**: System MUST use async/await patterns appropriately in FastAPI endpoints for performance
- **FR-015**: System MUST NOT accept user_id in URL parameters or request body, relying solely on JWT for user identification

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's task with properties including id, user_id (derived from JWT), title, description, due_datetime, priority (Eisenhower Matrix compatible), is_completed, created_at, updated_at
- **JWT Token**: Authentication token containing user identity information used to authorize all API requests and enforce user isolation

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create, read, update, and delete their tasks through the API with 99.9% success rate under normal load conditions
- **SC-002**: API responds to requests within 500ms for 95% of requests under normal load conditions
- **SC-003**: System successfully enforces user data isolation with 100% accuracy - no user can access another user's tasks
- **SC-004**: All API endpoints properly validate JWT tokens and return HTTP 401 for invalid/missing tokens with 100% accuracy
- **SC-005**: System supports at least 1000 concurrent users making API requests without data corruption or security breaches