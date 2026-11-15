---
description: Build a full-stack web app or SaaS (auth, database, dashboard, payments)
argument-hint: "<app idea and must-have features>"
---
Use the fullstack-web skill to build this web app: $ARGUMENTS

1. Give a short plan: features, data model, pages, API routes, stack (default Next.js + Supabase from `templates/nextjs-saas`).
2. Scaffold with `scripts/scaffold.py nextjs-saas <dir>` and extend it; add tables + RLS policies to `supabase/schema.sql`.
3. Use `references/payments.md` for payments and `references/ai-features.md` for any AI feature.
4. Add tests (`references/testing.md`), run `scripts/verify.py`, fix every failure.
5. Generate `.env.example` with `scripts/gen_env_example.py`, then give run + deploy steps.
