---
description: Deploy the current project to production
argument-hint: "[target: vercel | netlify | github-pages | railway | docker | eas]"
---
Use the fullstack-developer skill to deploy this project. Target (optional): $ARGUMENTS

1. Detect the project type and pick a target from `references/deploy.md` if none was given.
2. Run `scripts/verify.py` first; do not deploy a failing build.
3. List every env var the host needs (from `.env.example`) and any database migrations.
4. Create needed config (Dockerfile, `vercel.json`, `netlify.toml`, GitHub Actions, `eas.json`) and give exact steps or run them if tools are available.
5. Finish with the production checklist from `references/deploy.md`.
