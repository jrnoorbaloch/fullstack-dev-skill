# Remotion Promo Video Starter

A 3-scene promo video (intro with word-by-word headline, animated key points, CTA outro) with slide/fade transitions, in **landscape 1920×1080** and **vertical 1080×1920** (Reels/Shorts/TikTok). All text and colors are editable props (zod schema → editable in Remotion Studio).

> Remotion is free for individuals and small companies; bigger companies need a license — see https://www.remotion.dev/license

## Use
```bash
npm install
npm run dev                  # Remotion Studio: preview, edit props, scrub the timeline
npm run render               # out/promo.mp4
npm run render:vertical      # out/promo-vertical.mp4
npm run still                # out/thumbnail.png
```
Custom content without code changes: `npx remotion render Promo out/a.mp4 --props='{"headline":"Your text"}'`.

Rules: animate only from `useCurrentFrame()` (no CSS animations/timers/Math.random) so renders are deterministic.
