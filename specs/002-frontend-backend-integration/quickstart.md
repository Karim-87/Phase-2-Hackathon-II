# Quickstart Guide: Authentication Implementation

## Overview
This guide provides instructions for implementing the authentication system with both frontend and backend components.

## Backend Setup

### 1. Install Dependencies
```bash
# Navigate to backend directory
cd backend/

# Install required packages
pip install python-multipart bcrypt passlib[bcrypt]
```

### 2. Create User Model
Create `backend/src/models/user.py` with SQLModel structure following the same pattern as the Task model.

### 3. Create User Service
Create `backend/src/services/user_service.py` with methods for:
- User registration
- User authentication
- Password hashing
- User retrieval

### 4. Create Authentication Endpoints
Create `backend/src/api/v1/auth.py` with endpoints for:
- `/signup` - POST endpoint for user registration
- `/signin` - POST endpoint for user authentication
- `/me` - GET endpoint for retrieving user profile
- `/signout` - POST endpoint for signing out

### 5. Update Main Application
Update `backend/src/main.py` to include the auth router:
```python
from src.api.v1 import auth

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
```

### 6. Database Migration
Generate and run database migrations for the new User model:
```bash
cd backend/
alembic revision --autogenerate -m "Add user table"
alembic upgrade head
```

## Frontend Integration

### 1. Environment Variables
Ensure the frontend has the correct API base URL in `.env.local`:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 2. Authentication Flow
The existing authentication flow in `frontend/hooks/use-auth.ts` is already configured to call the correct endpoints:
- `/api/auth/signin` for login
- `/api/auth/signup` for registration

### 3. Protected Routes
Use the `useAuth` hook in protected pages to check authentication status:
```typescript
const { user, isLoading } = useAuth();

if (isLoading) return <div>Loading...</div>;
if (!user) {
  // Redirect to sign-in page
  router.push('/(auth)/sign-in');
  return null;
}
```

## Testing

### 1. Backend Tests
Create tests for:
- User registration with valid/invalid data
- User authentication with correct/incorrect credentials
- JWT token generation and validation
- User profile retrieval

### 2. Frontend Tests
Create tests for:
- Sign-in form submission
- Sign-up form submission
- Authentication state management
- Protected route access

## Security Considerations

### Password Handling
- Passwords must be hashed using BCrypt before storage
- Never log or expose plaintext passwords
- Implement password strength requirements

### Token Security
- JWT tokens should have appropriate expiration times
- Store tokens securely on the frontend
- Implement proper token refresh mechanisms

### Rate Limiting
- Apply rate limiting to authentication endpoints
- Prevent brute force attacks
- Implement account lockout after multiple failed attempts