# Rich Single-File Web Artifacts (React + Vite + Tailwind + shadcn/ui)

Use when the result must be **one self-contained HTML file** (shareable artifact, embeddable widget, offline demo, email attachment, a tool that runs by double-clicking) but needs more than plain HTML: React state, routing between views, shadcn/ui components, charts, GSAP animation.

For a simple page, write plain HTML instead (`templates/landing-page`). For a real deployed app, use `templates/nextjs-saas`.

## Workflow
1. Scaffold: `python scripts/scaffold.py react-vite-shadcn <dir>` (Vite + React + TypeScript + Tailwind v4 + shadcn-style UI primitives + GSAP + lucide icons, with `@/` alias).
2. Build the UI in `src/` like a normal React app. Add components from `src/components/ui/` (Button, Card, Badge, Input, Tabs, Dialog patterns) or more via `npx shadcn@latest add <name>` (config in `components.json`).
3. `npm run dev` to develop.
4. `npm run build` → `dist/index.html` is a **single file** with all JS and CSS inlined (`vite-plugin-singlefile`). That file is the deliverable.
5. Verify: `python scripts/verify.py <dir>` (type-check + build), then open `dist/index.html` directly from disk to confirm it works without a server.

## Rules for single-file output
- No runtime fetches to your own server; bundle data as JSON imports. External APIs only if the user wants them (and they allow CORS).
- Images: small ones as imports (inlined as base64 by Vite), large ones as external URLs, or SVG.
- Fonts: system font stack or a single Google Fonts `<link>` (needs network) — or inline a small `woff2` via import.
- Routing: hash routing or in-memory state (`useState` view switch); no history-API routes (file:// can't serve them).
- Storage: `localStorage` wrapped in try/catch (may be unavailable in sandboxed iframes); keep state in memory otherwise.
- Keep bundle reasonable: tree-shake icons (named imports), avoid heavy libraries unless used (charts → Recharts only when needed).
- Avoid "AI slop" look: no centered-everything layouts, purple gradients, uniform rounded cards and Inter-on-white by default — follow `references/design-system.md` and `references/ui-constraints.md`.

## shadcn/ui notes
- Components are copied into the project (`src/components/ui`) — edit freely.
- Use semantic tokens (`bg-background`, `text-muted-foreground`, `bg-primary`) defined in `src/index.css` (see `references/tailwind-system.md`).
- Accessible primitives (Dialog, DropdownMenu, Popover, Select, Tooltip) come from Radix — install them via the shadcn CLI rather than hand-rolling focus management.

## Typical artifacts
Calculators, quizzes, dashboards with mock data, interactive explainers, pricing configurators, kanban boards, form builders, mini games, animated product tours (GSAP), data visualizations.
