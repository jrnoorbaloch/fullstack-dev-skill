# Next.js + Supabase SaaS Starter

Landing page, magic-link sign-in, protected dashboard with per-user data (Row Level Security).

## Setup
1. `npm install`
2. Create a Supabase project, run `supabase/schema.sql` in the SQL editor.
3. Copy `.env.example` to `.env.local` and fill in the keys.
4. In Supabase → Authentication → URL Configuration, add `http://localhost:3000/auth/callback`.
5. `npm run dev` → http://localhost:3000

## Scripts
`dev` · `build` · `start` · `lint` (type-check) · `test` (Vitest)

## Deploy
Import the repo in Vercel, add the env vars, deploy. Add the production callback URL in Supabase.
