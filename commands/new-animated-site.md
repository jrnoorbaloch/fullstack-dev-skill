---
description: Build a premium animated website with GSAP (scroll stories, text reveals, micro-interactions)
argument-hint: "<what the site is for, style, sections>"
---
Use the fullstack-developer skill to build this animated website: $ARGUMENTS

1. Read `references/animation-gsap.md`, `references/design-system.md` and `references/ui-constraints.md`.
2. Pick a clear visual direction and plan which sections get which motion (hero intro timeline, SplitText headline, ScrollTrigger reveals, a pinned story section, counters, magnetic CTAs). Motion must support the content, not decorate everything.
3. Static site → plain HTML + GSAP CDN (see `examples/aurora-3d`). React/Next.js → `useGSAP` with scoped selectors and `gsap.matchMedia()`.
4. Required: `prefers-reduced-motion` path, content visible without JS, transform/opacity only, no layout shift, mobile layout without long pins.
5. Verify in a browser (desktop + 360 px mobile + reduced motion), run `scripts/verify.py`, then give deploy steps.
