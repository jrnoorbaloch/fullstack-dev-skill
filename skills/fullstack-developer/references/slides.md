# HTML Presentations (animated slide decks)

Use when the user wants a **code-built, animated web presentation** (pitch on a website, talk with live demos, interactive explainer). If they just want a normal deck to edit, a PowerPoint/Google Slides file or the host app's slide tool may fit better — ask if unclear.

## Start
Use `templates/html-slides`: one self-contained `index.html`, keyboard/touch navigation, progress bar, slide counter, URL hash per slide, GSAP entrance animations, print-to-PDF styles, reduced-motion support.

## Step 1 — pick a visual style (show options before building)
Offer 3 named directions with a one-line description and palette, e.g.:
| Style | Feel | Palette | Type |
|---|---|---|---|
| Midnight Tech | Dark, glowing accents, grid lines | #0b1020 / #7c8cff / #22d3ee | Inter + JetBrains Mono |
| Editorial | Serif headlines, lots of white space | #faf7f2 / #111 / #c2410c | Fraunces + Inter |
| Bold Startup | Big type, saturated blocks | #fef08a / #111 / #2563eb | Plus Jakarta Sans |
| Calm Corporate | Navy and teal, structured | #0f172a / #14b8a6 / #e2e8f0 | IBM Plex Sans |
Let the user choose (or pick the best fit and say why).

## Step 2 — structure
- 1 idea per slide. Title ≤ 8 words. ≤ 3 bullets or 1 visual.
- Typical pitch: Title → Problem → Solution → Demo → How it works → Market → Business model → Traction → Team → Ask → Thank you.
- Slide types in the template: `title`, `statement`, `bullets`, `split` (text + visual), `stats` (big numbers), `quote`, `code`, `image`, `end`.

## Step 3 — animation rules
- Entrance animations per slide: elements with `data-animate` (`fade-up`, `fade`, `scale`, `stagger`) run when the slide becomes active.
- Durations 0.4–0.8 s, stagger 0.06–0.12 s. No animation longer than 1 s.
- Counters for stats, line-by-line reveals for bullets, SplitText for the title slide only.
- Respect `prefers-reduced-motion` (template handles it).

## Navigation contract
- `→`, `Space`, `PageDown`, click right half / swipe left → next; `←`, `PageUp`, swipe right → previous; `Home`/`End`; `F` → fullscreen; number + `Enter` → jump.
- `#5` in the URL opens slide 5; history updates as you move.

## Export
- PDF: browser Print → Save as PDF (template has `@media print` with one slide per page, 16:9).
- Hosting: any static host (GitHub Pages, Netlify, Vercel).
- Speaker notes: put them in `<aside class="notes">` — hidden in the deck, shown in print if needed.

See `examples/pitch-deck` for a finished deck.
