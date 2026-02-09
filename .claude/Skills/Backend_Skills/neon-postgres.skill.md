---
name: neon-postgres
description: Guide and configure Neon PostgreSQL for production FastAPI backends. Use when migrating from SQLite or setting up cloud PostgreSQL.
---

# Neon PostgreSQL Setup Skill

## Purpose
Help the agent safely migrate or configure Neon PostgreSQL for production use.

## Instructions

1. **Database Creation**
   - Guide user to Neon dashboard
   - Recommend PostgreSQL v15
   - Select region closest to users

2. **Connection String Handling**
   - Always use SSL (`sslmode=require`)
   - Store in environment variables only
   - Never hardcode credentials

3. **Environment Separation**
   - SQLite for local development (optional)
   - PostgreSQL for staging/production

4. **Driver & Dependencies**
   - Use `psycopg2-binary` or `asyncpg`
   - Validate driver installation

## Example

```bash
DATABASE_URL=postgresql://user:password@ep-name.region.aws.neon.tech/neondb?sslmode=require
