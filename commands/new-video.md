---
description: Create a programmatic video with Remotion (promo, social clip, data-driven video)
argument-hint: "<video purpose, length, format (16:9 / 9:16), content>"
---
Use the fullstack-developer skill to create this video: $ARGUMENTS

1. Read `references/remotion.md` and mention the Remotion license note for companies.
2. Scaffold with `python scripts/scaffold.py remotion-video <dir>`; plan scenes with durations in frames.
3. Make all text/colors props in the zod schema; animate only from `useCurrentFrame()` (spring/interpolate), no CSS animations or randomness.
4. Run `npm run lint`, render a still (`npm run still`) to check composition, then explain `npm run render` / vertical render.
