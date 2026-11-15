---
description: Build a backend REST API with auth, database, docs and tests
argument-hint: "<resources/endpoints and preferred language>"
---
Use the fullstack-mobile skill to build this API: $ARGUMENTS

1. Design resources, endpoints, schema and auth (`references/backend-db.md`).
2. Python → start from `templates/fastapi-api`; other languages → follow that ecosystem's conventions.
3. Validate all input, scope every query to the current user, return consistent errors.
4. Write tests for each endpoint, run `scripts/verify.py`, and provide OpenAPI docs + `.env.example`.
