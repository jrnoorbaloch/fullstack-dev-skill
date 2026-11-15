# SEO & Performance

Target: Lighthouse **≥ 90** in Performance, Accessibility, Best Practices and SEO on mobile.

## On-page SEO
- Unique `<title>` (50–60 chars) and meta description (140–160 chars) per page.
- One `<h1>` per page, logical `h2`/`h3` order. Descriptive link text.
- Clean URLs (`/services/teeth-whitening`, not `/page?id=7`), `<link rel="canonical">`.
- `lang` attribute (and `hreflang` alternates for multilingual sites).
- Open Graph + Twitter tags: `og:title`, `og:description`, `og:image` (1200×630), `og:url`.
- `sitemap.xml` and `robots.txt` (Next.js: `app/sitemap.ts`, `app/robots.ts`).
- Structured data (JSON-LD): `LocalBusiness`/`Restaurant`/`MedicalClinic`, `Product`, `FAQPage`, `Article`, `BreadcrumbList`.
- Image `alt` text that describes the image.
- Local businesses: Google Business Profile, consistent name/address/phone (NAP) on every page, embed map.

```html
<script type="application/ld+json">
{ "@context": "https://schema.org", "@type": "LocalBusiness", "name": "Ali Bakery",
  "address": { "@type": "PostalAddress", "addressLocality": "Lahore", "addressCountry": "PK" },
  "telephone": "+92-300-0000000", "openingHours": "Mo-Su 08:00-22:00", "url": "https://example.com" }
</script>
```

## Core Web Vitals
| Metric | Good | Main fixes |
|---|---|---|
| LCP (largest paint) | < 2.5 s | Optimise hero image (AVIF/WebP, correct size, `fetchpriority="high"`, no lazy-load on it), preload main font, server-render above-the-fold content |
| INP (interaction) | < 200 ms | Less client JS, split bundles, avoid long tasks, debounce inputs, move work to server |
| CLS (layout shift) | < 0.1 | Width/height on images and embeds, reserve space for ads/banners, `font-display: swap` with size-adjusted fallbacks |

## Performance checklist
- Images: modern formats, responsive `srcset`/`next/image`, `loading="lazy"` below the fold, compress (< 200 KB hero).
- Fonts: max 2 families, `woff2`, subset, self-host or `next/font`.
- JavaScript: Server Components by default, dynamic `import()` for heavy widgets (maps, charts, editors), remove unused libraries.
- CSS: Tailwind purge (default), no large CSS frameworks on top.
- Caching: static assets with long `Cache-Control` + hashed names; CDN (Vercel/Netlify/Cloudflare).
- Data: paginate, index DB columns used in filters, avoid N+1 queries, cache expensive reads.
- Third-party scripts: load after interaction or with `defer`/`next/script strategy="lazyOnload"`.

## Measure
```bash
npx lighthouse https://your-site.com --preset=desktop --view
npx lighthouse https://your-site.com --form-factor=mobile --view
```
Also check PageSpeed Insights and Google Search Console (submit sitemap, watch coverage and Core Web Vitals).

## Analytics (privacy-friendly options)
Plausible, Umami, Vercel Analytics, or GA4 with consent banner where required.
