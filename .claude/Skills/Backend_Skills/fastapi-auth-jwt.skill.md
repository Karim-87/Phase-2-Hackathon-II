
```md
---
name: fastapi-auth-jwt
description: Implement secure JWT authentication in FastAPI backends. Use for API authentication.
---

# FastAPI JWT Authentication

## Instructions

1. **Token Design**
   - Access token (short-lived)
   - Refresh token (long-lived)
   - Use HS256 or RS256

2. **Security Rules**
   - Hash passwords (bcrypt)
   - Never store plain tokens
   - Validate token expiry

3. **Endpoints**
   - signup
   - signin
   - refresh
   - logout

## Example Concepts

```python
access_token_expiry = 15  # minutes
refresh_token_expiry = 7  # days
