# Animated HTML Slide Deck (GSAP)

One self-contained `index.html`: 7 slide layouts (title, statement, bullets, split, stats with counters, quote, end), GSAP entrance animations, progress bar, slide counter, URL hash per slide, reduced-motion support and print-to-PDF.

## Edit
- Restyle the whole deck by changing the CSS variables at the top (`--bg`, `--accent`, fonts…).
- Duplicate a `<section class="slide">` to add slides. Add `data-animate="fade-up|fade|scale|stagger"` to any element.
- Numbers animate with `<b data-count="1200" data-suffix="%" data-decimals="1">0</b>`.
- Speaker notes: `<aside class="notes">…</aside>` (hidden).

## Present
Open `index.html`. `→ / Space / PageDown` next · `← / PageUp` previous · `Home / End` · `F` fullscreen · type a number + `Enter` to jump · swipe on touch screens · `#5` in the URL opens slide 5.

## Export to PDF
Browser → Print → Save as PDF (one 16:9 slide per page).
