# Data Model: User Authentication

## User Entity

### Attributes
- **id** (UUID, Primary Key): Unique identifier for the user
- **email** (String, Required, Unique): User's email address for login
- **hashed_password** (String, Required): BCrypt hashed password
- **name** (String, Optional): User's full name
- **is_active** (Boolean, Default: true): Account status flag
- **created_at** (DateTime, Required): Timestamp when user was created
- **updated_at** (DateTime, Required): Timestamp when user was last updated

### Relationships
- **Tasks**: One-to-many relationship with Task entity (one user can have many tasks)
- The Task entity already includes a `user_id` foreign key field to establish user ownership

### Validation Rules
- Email must be a valid email format
- Email must be unique across all users
- Password must meet minimum strength requirements when implemented
- User ID must be a valid UUID format

### State Transitions
- **Active**: Default state for newly registered users
- **Inactive**: When account is deactivated (soft delete approach)

## Authentication Token

### JWT Token Payload
- **user_id** (UUID): User identifier included in JWT claims
- **exp** (Integer): Expiration timestamp (in Unix time)
- **iat** (Integer): Issued at timestamp (in Unix time)

### Security Considerations
- Tokens must include proper expiration times
- User ID must be validated from token in all protected endpoints
- Tokens should be stored securely on frontend (localStorage with appropriate security considerations)

## Compliance Requirements

### User Isolation
- All data access must be filtered by authenticated user's ID
- Cross-user data access must be prevented at the database query level
- Task queries must include user_id in WHERE clauses

### Data Privacy
- Passwords must be hashed using BCrypt (or similar secure algorithm)
- Plain text passwords must never be stored
- Authentication tokens must be properly secured