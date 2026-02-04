# Data Model: Backend Hardening & Modernization

## Current Data Models

### Task Model
The primary entity in the system representing user tasks with Eisenhower Matrix prioritization.

```python
class TaskBase(SQLModel):
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)
    due_datetime: Optional[datetime] = Field(default=None)
    priority: PriorityEnum = Field(sa_column=sa_Column(sa_Enum(PriorityEnum), nullable=False))
    is_completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(nullable=False, index=True)  # Index for efficient filtering by user
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID  # Included for transparency but not modifiable
    created_at: datetime
    updated_at: datetime

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_datetime: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None
    is_completed: Optional[bool] = None
```

### Priority Enum
Eisenhower Matrix-based priority classification system:
- `URGENT_IMPORTANT`: Do First - Important and urgent tasks
- `NOT_URGENT_IMPORTANT`: Schedule - Important but not urgent tasks
- `URGENT_NOT_IMPORTANT`: Delegate - Urgent but not important tasks
- `NOT_URGENT_NOT_IMPORTANT`: Eliminate - Neither urgent nor important tasks

## Additional Models Needed

### Token Model (for refresh tokens)
```python
class Token(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    token: str = Field(unique=True, nullable=False, index=True)  # The refresh token
    user_id: uuid.UUID = Field(nullable=False, foreign_key="user.id", index=True)
    expires_at: datetime = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    revoked: bool = Field(default=False)
    device_info: Optional[str] = Field(default=None)  # Optional device identification
```

### User Model (if needed for completeness)
Currently, user information is stored in JWT tokens, but a formal User model might be needed:
```python
class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, index=True)
    name: str = Field(max_length=100, nullable=False)
    is_active: bool = Field(default=True)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    last_login_at: Optional[datetime] = Field(default=None)
```

## Database Relationships

### Task to User
- Many-to-One relationship (many tasks to one user)
- Foreign key constraint on `user_id` field
- Indexed for efficient user-based filtering
- Enforces user isolation at database level

### Token to User (proposed for refresh tokens)
- Many-to-One relationship (many tokens to one user)
- Foreign key constraint on `user_id` field
- Indexed for efficient token lookup by user

## Validation Rules

### Task Validation
- Title: Required, max length 255 characters
- Priority: Required, must be one of the defined PriorityEnum values
- User ID: Required, must exist in the system (enforced by foreign key)
- Due datetime: Optional, if provided must be valid datetime

### Token Validation (proposed)
- Token: Required, unique across all tokens
- User ID: Required, must exist in the system
- Expires At: Required, must be in the future
- Revoked: Boolean flag to support token revocation

## State Transitions

### Task State Transitions
- `is_completed`: Boolean toggle between False and True states
- `updated_at`: Automatically updated on any change
- `created_at`: Set once on creation, immutable

### Token State Transitions (proposed)
- `revoked`: Boolean toggle from False to True (one-way)
- `expires_at`: Set during creation, immutable

## Indexing Strategy

### Current Indexes
- `user_id` on Task table (for user isolation queries)
- Primary keys on all tables

### Proposed Indexes
- `token` on Token table (for fast token lookup)
- `expires_at` on Token table (for cleanup queries)
- Composite indexes on frequently queried fields if needed