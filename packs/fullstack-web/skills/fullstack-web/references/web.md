# Web (websites, web apps, SaaS, dashboards)

## Choose
- 1–5 static pages, no login → single `index.html` + Tailwind CDN, or **Astro** for multi-page/blog.
- Login, database, dashboard, payments → **Next.js 15+ App Router + TypeScript + Tailwind + shadcn/ui**.
- User asks for Vue/Nuxt, Svelte/SvelteKit, Angular, Laravel, Django, Rails → use that.

## Next.js scaffold
```
npx create-next-app@latest my-app --ts --tailwind --eslint --app --src-dir --import-alias "@/*"
npx shadcn@latest init
```
Structure:
```
src/app/(marketing)/page.tsx      landing
src/app/(app)/dashboard/page.tsx  protected area
src/app/api/<resource>/route.ts   API
src/components/ui/                shadcn
src/components/<feature>/         feature components
src/lib/ (db.ts, auth.ts, utils.ts, validations.ts)
```
- Server Components by default; `"use client"` only for interactivity.
- Server Actions or route handlers for mutations; validate with **zod**.
- Forms: react-hook-form + zod. Data fetching on client: TanStack Query.
- Metadata + `sitemap.ts` + `robots.ts` for SEO; `next/image` for images.

## Design checklist
- Mobile-first breakpoints, max content width ~1200px, 8px spacing scale.
- Hero → features → social proof → pricing → FAQ → CTA → footer for landing pages.
- Dashboards: sidebar nav, top bar with user menu, cards for KPIs, tables with search/sort/pagination, charts (Recharts).
- States: skeleton loaders, empty states with a CTA, toast notifications (sonner).
- Accessibility: one `h1`, labelled inputs, focus rings, `alt` text, contrast ≥ 4.5:1.
- RTL languages: `<html dir="rtl" lang="ur">`, use logical CSS (`ms-`, `me-`, `ps-`, `pe-`).

## Common features — how
- **Auth**: Supabase Auth or Auth.js; middleware protects `/dashboard`.
- **Payments**: Stripe Checkout + webhook route (verify signature). Local gateways (JazzCash/Easypaisa, Razorpay, etc.) via their official SDK/REST when asked.
- **File uploads**: Supabase Storage / S3 / UploadThing; validate type and size.
- **Email**: Resend / Nodemailer.
- **i18n**: next-intl with `messages/<locale>.json`.
- **E-commerce**: products, categories, cart (persisted), checkout, orders, admin panel.
