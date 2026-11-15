# Deploy & DevOps

## Where
| What | Recommended | Free tier |
|---|---|---|
| Static site | Netlify, Vercel, GitHub Pages, Cloudflare Pages | yes |
| Next.js | Vercel | yes |
| Node/Python API | Railway, Render, Fly.io | limited |
| Postgres + auth + storage | Supabase, Neon | yes |
| Mobile | Expo EAS → Play Store / App Store | limited |
| Docker anywhere | VPS (Hetzner, DigitalOcean) + Docker Compose + Caddy | no |

## Steps (web)
1. Push code to GitHub.
2. Import repo in Vercel/Netlify → set env vars → deploy.
3. Add custom domain → DNS (A/CNAME) → HTTPS automatic.

## Docker (when asked or for VPS)
- Multi-stage `Dockerfile`, non-root user, `.dockerignore`.
- `docker-compose.yml` with app + db + reverse proxy; volumes for data.

## CI (GitHub Actions)
`.github/workflows/ci.yml`: checkout → setup node/python → install → lint → test → build on every push/PR.

## Production checklist
- Env vars set, no secrets in repo, `NODE_ENV=production`.
- Database migrations run; backups enabled.
- Error monitoring (Sentry), basic analytics, uptime check.
- SEO: title/description/OG image, sitemap, robots.
- Performance: images optimised, Lighthouse ≥ 90.
