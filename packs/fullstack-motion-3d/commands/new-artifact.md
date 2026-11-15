---
description: Build a rich single-file web artifact with React, Tailwind, shadcn/ui and GSAP
argument-hint: "<tool, dashboard, calculator, interactive explainer…>"
---
Use the fullstack-motion-3d skill to build this artifact: $ARGUMENTS

1. Read `references/artifacts.md`, `references/tailwind-system.md` and `references/react-patterns.md`.
2. Scaffold with `python scripts/scaffold.py react-vite-shadcn <dir> --set TITLE="…" --set DESCRIPTION="…"`.
3. Build with composable components (cva variants, compound components), semantic tokens, accessible primitives, and GSAP via `useGSAP` where motion helps.
4. `npm run build` must produce one self-contained `dist/index.html`; open it from disk to confirm it works without a server.
5. Deliver the single HTML file (and the source project).
