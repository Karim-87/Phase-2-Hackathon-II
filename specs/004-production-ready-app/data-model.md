# Data Model: 004-production-ready-app

**Date**: 2026-02-08
**Branch**: `004-production-ready-app`
**Spec**: [spec.md](./spec.md)

## Entity Relationship Overview

```
User 1──* Account    (one user has many auth provider accounts)
User 1──* Session    (one user has many active sessions)
User 1──* Task       (one user owns many tasks)
```

## Entities

### User (existing — preserve)

| Field | Type | Constraints | Notes |
| ----- | ---- | ----------- | ----- |
| id | text | PK | ULID/UUID string, generated on creation |
| email | text | UNIQUE, NOT NULL, indexed | Primary login identifier |
| email_verified | boolean | NOT NULL, default: false | Not enforced this iteration |
| name | text | nullable, max 100 chars | Display name |
| image | text | nullable, max 500 chars | Avatar URL |
| role | text | NOT NULL, default: "user" | "user" or "admin" |
| banned | boolean | NOT NULL, default: false | Account ban flag |
| ban_reason | text | nullable | Reason for ban |
| ban_expires | datetime(tz) | nullable | Temporary ban expiry |
| created_at | datetime(tz) | NOT NULL, server default: now() | Record creation |
| updated_at | datetime(tz) | NOT NULL, server default: now(), on update: now() | Last modification |

**Relationships**: sessions (1:many), accounts (1:many), tasks (1:many — NEW)
**Table**: `user`

---

### Account (existing — preserve)

| Field | Type | Constraints | Notes |
| ----- | ---- | ----------- | ----- |
| id | text | PK | Generated string |
| user_id | text | FK → user.id, NOT NULL, indexed, CASCADE delete | Owner |
| account_id | text | NOT NULL | Provider-specific account ID |
| provider_id | text | NOT NULL | "credential" for password, "google" for OAuth, etc. |
| access_token | text | nullable | OAuth access token |
| refresh_token | text | nullable | OAuth refresh token |
| id_token | text | nullable | OAuth ID token |
| access_token_expires_at | datetime(tz) | nullable | Token expiry |
| refresh_token_expires_at | datetime(tz) | nullable | Token expiry |
| scope | text | nullable | OAuth scope |
| password | text | nullable | **bcrypt hash** (for credential provider only) |
| created_at | datetime(tz) | NOT NULL, server default: now() | Record creation |
| updated_at | datetime(tz) | NOT NULL, server default: now(), on update: now() | Last modification |

**Unique constraint**: (provider_id, account_id)
**Table**: `account`

**Migration note**: Existing SHA-256 password hashes (`salt:hash` format) will be detected by format and re-hashed to bcrypt on next successful login.

---

### Session (existing — preserve)

| Field | Type | Constraints | Notes |
| ----- | ---- | ----------- | ----- |
| id | text | PK | Generated string |
| user_id | text | FK → user.id, NOT NULL, indexed, CASCADE delete | Owner |
| token | text | UNIQUE, NOT NULL, indexed | Session token |
| expires_at | datetime(tz) | NOT NULL | Session expiry |
| ip_address | text | nullable | Client IP |
| user_agent | text | nullable | Client browser info |
| impersonated_by | text | nullable | Admin impersonation tracking |
| created_at | datetime(tz) | NOT NULL, server default: now() | Record creation |
| updated_at | datetime(tz) | NOT NULL, server default: now(), on update: now() | Last modification |

**Table**: `session`

---

### Verification (existing — preserve, not used this iteration)

| Field | Type | Constraints | Notes |
| ----- | ---- | ----------- | ----- |
| id | text | PK | Generated string |
| identifier | text | NOT NULL, indexed | Email address |
| value | text | NOT NULL | Verification token |
| expires_at | datetime(tz) | NOT NULL | Token expiry |
| created_at | datetime(tz) | nullable, server default: now() | Record creation |
| updated_at | datetime(tz) | nullable, server default: now(), on update: now() | Last modification |

**Table**: `verification`

---

### Task (NEW — migrate from SQLModel to SQLAlchemy ORM)

| Field | Type | Constraints | Notes |
| ----- | ---- | ----------- | ----- |
| id | text | PK | ULID/UUID string, generated on creation |
| user_id | text | FK → user.id, NOT NULL, indexed, CASCADE delete | Task owner |
| title | text | NOT NULL, max 255 chars | Task title |
| description | text | nullable | Task details |
| due_datetime | datetime(tz) | nullable | Optional due date/time |
| priority | text | NOT NULL | Eisenhower enum: see below |
| is_completed | boolean | NOT NULL, default: false | Completion status |
| created_at | datetime(tz) | NOT NULL, server default: now() | Record creation |
| updated_at | datetime(tz) | NOT NULL, server default: now(), on update: now() | Last modification |

**Priority enum values**: `urgent_important`, `not_urgent_important`, `urgent_not_important`, `not_urgent_not_important`

**Indexes**: user_id (for filtering user's tasks), (user_id, is_completed) composite for filtered queries

**Table**: `task`

**Relationship**: user (many:1 → User)

---

## Validation Rules

### User
- email: valid email format, max 255 chars, unique across system
- name: max 100 chars, trimmed whitespace
- password (on Account): min 8 chars, at least 1 uppercase, 1 lowercase, 1 number

### Task
- title: required, max 255 chars, trimmed whitespace, non-empty after trim
- description: max 5000 chars
- priority: must be one of the 4 enum values
- due_datetime: if provided, must be a valid datetime (past dates allowed for existing tasks)
- user_id: must reference an existing, non-banned user

## State Transitions

### Task Lifecycle
```
Created (is_completed=false)
  → Completed (is_completed=true)
  → Reopened (is_completed=false)
  → Deleted (hard delete)
```

### User Account Lifecycle
```
Registered (email_verified=false, banned=false)
  → Active (normal usage)
  → Banned (banned=true, optional ban_expires)
  → Unbanned (banned=false)
```
