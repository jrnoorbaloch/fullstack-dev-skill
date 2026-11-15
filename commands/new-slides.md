---
description: Create an animated HTML presentation (pitch deck, talk, explainer)
argument-hint: "<topic, audience, number of slides, style>"
---
Use the fullstack-developer skill to create this presentation: $ARGUMENTS

1. Read `references/slides.md`. Offer 3 visual styles (name, palette, fonts) unless the user already chose one.
2. Outline the slides (one idea per slide, ≤ 8-word titles) and confirm briefly if the topic is ambiguous.
3. Scaffold with `python scripts/scaffold.py html-slides <dir>`, set the theme variables, write real content, use `data-animate` and `data-count`.
4. Check keyboard, swipe, URL hash navigation and print-to-PDF; keep animations ≤ 1 s.
5. Deliver the `index.html` plus hosting and PDF export instructions.
