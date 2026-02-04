# Data Model: FastAPI Better-Auth Integration

**Feature Branch**: `003-fastapi-better-auth`
**Date**: 2026-02-03
**Database**: Neon PostgreSQL (Serverless)

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ┌─────────────┐       ┌─────────────┐       ┌─────────────┐       │
│  │    User     │       │   Session   │       │   Account   │       │
│  ├─────────────┤       ├─────────────┤       ├─────────────┤       │
│  │ id (PK)     │◄──┬───┤ user_id(FK) │       │ user_id(FK) │───┐   │
│  │ email       │   │   │ token       │       │ provider_id │   │   │
│  │ name        │   │   │ expires_at  │       │ account_id  │   │   │
│  │ role        │   │   │ ip_address  │       │ access_token│   │   │
│  │ banned      │   │   │ user_agent  │       │ refresh_tkn │   │   │
│  │ email_ver   │   │   └─────────────┘       └─────────────┘   │   │
│  └─────────────┘   │                                           │   │
│         ▲          │   ┌─────────────┐                         │   │
│         │          │   │Verification │                         │   │
│         │          │   ├─────────────┤                         │   │
│         └──────────┴───┤ identifier  │◄────────────────────────┘   │
│                        │ value       │                             │
│                        │ expires_at  │                             │
│                        └─────────────┘                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Entities

### User

Primary entity representing authenticated users. Schema follows Better-Auth conventions.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | TEXT | PK | Unique identifier (ULID or UUID) |
| email | TEXT | UNIQUE, NOT NULL | User's email address |
| email_verified | BOOLEAN | NOT NULL, DEFAULT false | Email verification status |
| name | TEXT | NULLABLE | User's display name |
| image | TEXT | NULLABLE | Profile image URL |
| role | TEXT | DEFAULT 'user' | User role: 'admin', 'user' |
| banned | BOOLEAN | DEFAULT false | Ban status |
| ban_reason | TEXT | NULLABLE | Reason for ban |
| ban_expires | TIMESTAMP | NULLABLE | Ban expiration timestamp |
| created_at | TIMESTAMP | NOT NULL | Record creation time |
| updated_at | TIMESTAMP | NOT NULL | Last update time |

**SQLAlchemy Model**:
```python
class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False, index=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    role: Mapped[str] = mapped_column(Text, default="user")
    banned: Mapped[bool] = mapped_column(Boolean, default=False)
    ban_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ban_expires: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    sessions: Mapped[List["Session"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    accounts: Mapped[List["Account"]] = relationship(back_populates="user", cascade="all, delete-orphan")
```

### Session

Represents active user sessions managed by Better-Auth.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | TEXT | PK | Session identifier |
| user_id | TEXT | FK(user.id), NOT NULL | Associated user |
| token | TEXT | UNIQUE, NOT NULL | Session token |
| expires_at | TIMESTAMP | NOT NULL | Session expiration |
| ip_address | TEXT | NULLABLE | Client IP address |
| user_agent | TEXT | NULLABLE | Client user agent |
| impersonated_by | TEXT | NULLABLE | Admin ID if impersonating |
| created_at | TIMESTAMP | NOT NULL | Session creation time |
| updated_at | TIMESTAMP | NOT NULL | Last update time |

**SQLAlchemy Model**:
```python
class Session(Base):
    __tablename__ = "session"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    user_id: Mapped[str] = mapped_column(Text, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    token: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    impersonated_by: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user: Mapped["User"] = relationship(back_populates="sessions")
```

### Account

Represents OAuth provider linkages and credential storage.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | TEXT | PK | Account record identifier |
| user_id | TEXT | FK(user.id), NOT NULL | Associated user |
| account_id | TEXT | NOT NULL | Provider-specific user ID |
| provider_id | TEXT | NOT NULL | Provider name (google, github, credential) |
| access_token | TEXT | NULLABLE | OAuth access token |
| refresh_token | TEXT | NULLABLE | OAuth refresh token |
| id_token | TEXT | NULLABLE | OAuth ID token (OIDC) |
| access_token_expires_at | TIMESTAMP | NULLABLE | Access token expiration |
| refresh_token_expires_at | TIMESTAMP | NULLABLE | Refresh token expiration |
| scope | TEXT | NULLABLE | OAuth scopes granted |
| password | TEXT | NULLABLE | Hashed password (for credential provider) |
| created_at | TIMESTAMP | NOT NULL | Record creation time |
| updated_at | TIMESTAMP | NOT NULL | Last update time |

**SQLAlchemy Model**:
```python
class Account(Base):
    __tablename__ = "account"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    user_id: Mapped[str] = mapped_column(Text, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    account_id: Mapped[str] = mapped_column(Text, nullable=False)
    provider_id: Mapped[str] = mapped_column(Text, nullable=False)
    access_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    refresh_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    id_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    access_token_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    refresh_token_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    scope: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    password: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user: Mapped["User"] = relationship(back_populates="accounts")

    # Unique constraint for provider + account combination
    __table_args__ = (
        UniqueConstraint('provider_id', 'account_id', name='uq_account_provider'),
    )
```

### Verification

Stores verification tokens for email confirmation and password reset.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | TEXT | PK | Verification record identifier |
| identifier | TEXT | NOT NULL | Target identifier (email) |
| value | TEXT | NOT NULL | Verification token/code |
| expires_at | TIMESTAMP | NOT NULL | Token expiration |
| created_at | TIMESTAMP | NULLABLE | Record creation time |
| updated_at | TIMESTAMP | NULLABLE | Last update time |

**SQLAlchemy Model**:
```python
class Verification(Base):
    __tablename__ = "verification"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    identifier: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

## Validation Rules

### User Validation
- **email**: Valid email format, max 255 characters
- **name**: Max 100 characters, alphanumeric with spaces
- **role**: Enum of ['admin', 'user']
- **image**: Valid URL format if provided

### Session Validation
- **token**: Non-empty string, unique across all sessions
- **expires_at**: Must be in the future when created

### Account Validation
- **provider_id**: Enum of ['credential', 'google', 'github']
- **password**: Required when provider_id is 'credential'
- Unique constraint on (provider_id, account_id)

## State Transitions

### User States
```
[Unregistered] --register--> [Unverified] --verify email--> [Active]
[Active] --ban--> [Banned] --unban--> [Active]
[Banned] --ban expires--> [Active]
```

### Session States
```
[Created] --authenticate--> [Active] --expires/logout--> [Expired/Invalidated]
```

## Indexes

| Table | Index Name | Columns | Purpose |
|-------|------------|---------|---------|
| user | user_email_idx | email | Login lookup |
| session | session_user_id_idx | user_id | User sessions lookup |
| session | session_token_idx | token | Token validation |
| account | account_user_id_idx | user_id | User accounts lookup |
| account | uq_account_provider | (provider_id, account_id) | Provider uniqueness |
| verification | verification_identifier_idx | identifier | Token lookup |

## Migration Strategy

1. **Phase 1**: Create new tables with Better-Auth schema
2. **Phase 2**: Migrate existing users from current schema
3. **Phase 3**: Drop legacy user/auth tables

### Migration Notes
- Existing `hashed_password` maps to `account.password` with `provider_id='credential'`
- UUID fields should be converted to TEXT (Better-Auth uses ULID/text IDs)
- Add missing columns (email_verified, role, etc.)
