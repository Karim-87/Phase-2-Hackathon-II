
```md
---
name: database-migrations
description: Manage schema changes safely using Alembic. Use when database structure evolves.
---

# Database Migration Management

## Instructions

1. **Alembic Setup**
   - Initialize Alembic in backend root
   - Load database URL from environment settings
   - Never hardcode URLs in alembic.ini

2. **Model Integration**
   - Import all SQLModel / SQLAlchemy models
   - Set `target_metadata` correctly

3. **Migration Workflow**
   - autogenerate migrations
   - review before applying
   - apply with `upgrade head`

## Example Commands

```bash
alembic revision --autogenerate -m "Add users and tasks"
alembic upgrade head
