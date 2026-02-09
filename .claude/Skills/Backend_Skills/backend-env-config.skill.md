
```md
---
name: backend-env-config
description: Configure backend environments securely using .env files. Use for local, staging, and production setups.
---

# Backend Environment Configuration

## Instructions

1. **Environment Files**
   - `.env.local` → development
   - `.env.production` → production
   - Never commit secrets

2. **Required Variables**
   - DATABASE_URL
   - JWT_SECRET
   - ENVIRONMENT

3. **Configuration Loading**
   - Use Pydantic settings
   - Validate on startup

## Example

```bash
DATABASE_URL=postgresql://...
JWT_SECRET=super-secure-random-string
ENVIRONMENT=production
