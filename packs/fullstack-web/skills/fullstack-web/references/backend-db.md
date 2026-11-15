# Backend, APIs, Database, Auth

## Choose
- Inside Next.js → route handlers / server actions.
- Separate Node API → **Fastify or Express + TypeScript + zod**.
- Python → **FastAPI + Pydantic + SQLAlchemy/SQLModel**, run with uvicorn.
- Other ecosystems on request: Laravel, Django REST, Spring Boot, ASP.NET Core, Go (Gin/Fiber), Rails.

## API conventions
- REST: `GET /api/items`, `GET /api/items/:id`, `POST`, `PATCH`, `DELETE`. Plural nouns, JSON, proper status codes (200/201/204/400/401/403/404/409/422/500).
- Consistent error shape: `{ "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [] } }`.
- Pagination: `?page=&limit=` or cursor. Filtering & sorting via query params.
- Validate every input; never trust the client.
- Generate OpenAPI docs (FastAPI does it automatically; Fastify → @fastify/swagger).

## Database
- Default: **PostgreSQL** (Supabase or Neon). Small/local: SQLite. Document-style on request: MongoDB + Mongoose.
- ORM: Prisma (`prisma/schema.prisma`, `npx prisma migrate dev`) or Drizzle.
- Every table: `id` (uuid/cuid), `created_at`, `updated_at`; foreign keys + indexes on lookup columns.
- Provide a `seed` script with realistic demo data.
- Supabase: enable **Row Level Security** and write policies (`auth.uid() = user_id`).

## Auth & security
- Hash passwords with bcrypt/argon2; sessions via HTTP-only secure cookies or short-lived JWT + refresh.
- Roles (user/admin) checked server-side on every protected route.
- Rate limiting on auth and public endpoints; CORS restricted to known origins.
- Secrets only in env vars; ship `.env.example` with every key listed (no real values).
- Webhooks: verify signatures.

## Background work
- Cron: Vercel Cron / Supabase pg_cron / node-cron.
- Queues: BullMQ + Redis (Upstash) when jobs are heavy.
- Realtime: Supabase Realtime, Socket.IO, or Server-Sent Events.

## Testing
- Unit: Vitest/Jest or pytest. API: supertest / httpx TestClient. Seed a test DB.
