---
name: backend-security
description: Enforce backend security best practices. Use for production hardening.
---

# Backend Security Best Practices

## Instructions

1. **Secrets**
   - Use environment variables
   - Rotate secrets periodically

2. **Protection**
   - Rate limiting on auth endpoints
   - Input validation
   - SQL injection protection

3. **JWT Security**
   - Strong secrets (64+ chars)
   - Short access token lifetime

## Recommended Tools
- slowapi (rate limiting)
- passlib (password hashing)
- pyjwt or jose

## Best Practices
- Log security events
- Avoid detailed error messages in production
