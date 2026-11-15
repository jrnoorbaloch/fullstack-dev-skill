# React + Vite + Tailwind + shadcn/ui + GSAP (single-file build)

A rich React starter whose production build is **one self-contained `dist/index.html`** — ideal for shareable artifacts, widgets and offline demos. Also works as a normal Vite app.

Includes: Tailwind v4 with semantic tokens and dark mode, shadcn-style `Button`, `Card`, `Badge`, `Input`, `Tabs` (cva + `cn`), lucide icons, and a GSAP intro timeline with `useGSAP` and reduced-motion handling.

## Use
```bash
npm install
npm run dev        # http://localhost:5173
npm run build      # → dist/index.html (open it straight from disk)
```
Add more shadcn components: `npx shadcn@latest add dialog dropdown-menu select` (uses `components.json`).

## Deploy as a normal site
Any static host (Netlify, Vercel, GitHub Pages) — upload `dist/`.
