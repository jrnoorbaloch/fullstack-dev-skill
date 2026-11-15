# Programmatic Video with Remotion

Remotion renders React components to MP4/WebM frame by frame. Use it for promo videos, social clips, product demos, data-driven videos (one template, many personalised renders), animated captions.

> Licensing: Remotion is free for individuals and small companies; larger companies need a company license. Check https://www.remotion.dev/license before using it commercially.

## Start
```bash
npx create-video@latest            # or use templates/remotion-video
npm run dev                        # Remotion Studio (preview + timeline)
npx remotion render MyVideo out/video.mp4
```

## Core concepts
| Concept | Meaning |
|---|---|
| `<Composition>` | A renderable video: `id`, `component`, `durationInFrames`, `fps`, `width`, `height`, `defaultProps`, optional `schema` (zod) |
| `useCurrentFrame()` | The frame being rendered — **all** animation derives from it |
| `useVideoConfig()` | `fps`, `width`, `height`, `durationInFrames` |
| `interpolate(frame, [in], [out], { extrapolateRight: "clamp" })` | Map frames to values |
| `spring({ frame, fps, config })` | Natural easing 0 → 1 |
| `<Sequence from={30} durationInFrames={60}>` | Time-shift children (their `useCurrentFrame` starts at 0) |
| `<Series>` / `<TransitionSeries>` | Back-to-back scenes, with `@remotion/transitions` (fade, slide, wipe) |
| `<AbsoluteFill>` | Full-frame layer |
| `<Img>`, `<Video>`/`<OffthreadVideo>`, `<Audio>`, `staticFile()` | Assets that block rendering until loaded |

## Rules (deterministic rendering)
- Animate only from `useCurrentFrame()` — **no** CSS transitions/animations, `setTimeout`, `Math.random()` (use `random(seed)` from `remotion`), or `Date.now()`.
- Don't use GSAP's own clock; if you want GSAP eases, use `gsap.parseEase("power3.out")(progress)` with progress computed from the frame, or a paused timeline with `tl.progress(frame / total)`.
- Load fonts with `@remotion/google-fonts` or `loadFont` and wait (`delayRender`/`continueRender`) for any async data.
- Use `<Img>`/`<OffthreadVideo>` rather than `<img>`/`<video>` so frames wait for media.
- Durations in frames: `seconds * fps`.

## Example scene
```tsx
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Title: React.FC<{ title: string; color: string }> = ({ title, color }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 200 } });
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ background: color, justifyContent: "center", alignItems: "center" }}>
      <h1 style={{ opacity, transform: `translateY(${(1 - enter) * 60}px)`, color: "white", fontSize: 120 }}>{title}</h1>
    </AbsoluteFill>
  );
};
```

## Formats
| Use | Size | fps |
|---|---|---|
| YouTube / landscape | 1920×1080 | 30 |
| Reels / TikTok / Shorts | 1080×1920 | 30 |
| Instagram feed | 1080×1350 or 1080×1080 | 30 |

## Data-driven & captions
- Pass data via `defaultProps` + zod `schema` (editable in Studio) or `--props=props.json` on render.
- Render many variants in a loop with `@remotion/renderer` (`bundle` → `selectComposition` → `renderMedia`).
- Captions: `@remotion/captions` / `@remotion/install-whisper-cpp` to transcribe, then render word-by-word highlights.
- Audio-reactive visuals: `@remotion/media-utils` (`useAudioData`, `visualizeAudio`).

## Rendering at scale
- Local: `npx remotion render`. Cloud: `@remotion/lambda` (AWS) or Cloud Run.
- Embed an interactive preview in a web app with `@remotion/player`.
