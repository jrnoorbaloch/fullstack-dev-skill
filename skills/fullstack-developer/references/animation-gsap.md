# Animation with GSAP

GSAP is the default for anything beyond simple hover/fade transitions: scroll-driven storytelling, timelines, text reveals, SVG drawing/morphing, drag, page transitions. Since 2025 the **entire GSAP toolset is free, including commercial use and every former "Club" plugin** (SplitText, MorphSVG, DrawSVG, ScrollSmoother, Inertia…). Install from the public package only — no tokens, no `gsap-trial`.

```bash
npm i gsap @gsap/react      # React projects
```
```html
<!-- No-build sites (pin a version) -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15/dist/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15/dist/SplitText.min.js"></script>
```

## When to use what
| Need | Use |
|---|---|
| Hover, focus, simple enter/exit | CSS transitions |
| Route/page/shared-element transitions in React | View Transitions (`references/react-patterns.md`) |
| Sequenced intros, scroll storytelling, pinning, scrubbing, text splitting, SVG | **GSAP** |
| Layout animations in React component trees | GSAP **Flip** (or Motion if the project already uses it) |
| 3D scenes | Three.js / R3F, driven by GSAP timelines (`references/threejs.md`) |

## Core API
```js
gsap.registerPlugin(ScrollTrigger, SplitText);           // once, at app start

gsap.to(".card", { y: 0, opacity: 1, duration: 0.6, ease: "power3.out", stagger: 0.08 });
gsap.from(".hero h1", { y: 40, autoAlpha: 0 });           // autoAlpha = opacity + visibility
gsap.fromTo(".bar", { scaleX: 0 }, { scaleX: 1, transformOrigin: "left center" });
gsap.set(".modal", { autoAlpha: 0 });

const tl = gsap.timeline({ defaults: { duration: 0.6, ease: "power3.out" } });
tl.from(".logo", { y: -20, autoAlpha: 0 })
  .from(".nav a", { y: -10, autoAlpha: 0, stagger: 0.05 }, "<0.1")   // starts 0.1s after previous start
  .from(".hero h1", { y: 40, autoAlpha: 0 }, "-=0.3")                 // overlaps previous by 0.3s
  .addLabel("cta")
  .from(".cta", { scale: 0.9, autoAlpha: 0 }, "cta");
```
Position parameter cheatsheet: `"<"` start of previous · `">"` end of previous · `"+=0.5"` gap · `"-=0.3"` overlap · `"label"`.

Eases: `power1-4.out` (UI), `expo.out` (dramatic), `back.out(1.7)` (playful pop), `elastic.out(1, 0.5)` (springy), `"none"` (scrubbed scroll).

## ScrollTrigger
```js
gsap.from(".feature", {
  y: 60, autoAlpha: 0, stagger: 0.15,
  scrollTrigger: { trigger: ".features", start: "top 75%", toggleActions: "play none none reverse" },
});

// Pinned, scrubbed story section
const tl = gsap.timeline({
  scrollTrigger: { trigger: ".story", start: "top top", end: "+=2000", scrub: 1, pin: true, anticipatePin: 1 },
});
tl.to(".step-1", { autoAlpha: 0 }).from(".step-2", { autoAlpha: 0, y: 40 });

// Horizontal scroll gallery
const track = document.querySelector(".track");
gsap.to(track, {
  x: () => -(track.scrollWidth - window.innerWidth), ease: "none",
  scrollTrigger: { trigger: ".gallery", pin: true, scrub: 1, end: () => "+=" + track.scrollWidth, invalidateOnRefresh: true },
});

ScrollTrigger.batch(".reveal", { onEnter: (els) => gsap.from(els, { y: 30, autoAlpha: 0, stagger: 0.1 }) });
```
- `markers: true` while developing, remove before shipping.
- Call `ScrollTrigger.refresh()` after images/fonts/data change layout.
- One ScrollTrigger per timeline (put it on the timeline, not on child tweens).

## Text: SplitText
```js
const split = SplitText.create(".headline", { type: "lines,words", mask: "lines", autoSplit: true,
  onSplit: (self) => gsap.from(self.words, { yPercent: 100, stagger: 0.04, duration: 0.8, ease: "expo.out" }) });
```
Keep the original text accessible (SplitText adds `aria-label`/`aria-hidden` handling); avoid splitting long paragraphs into chars.

## Other high-value plugins
| Plugin | Use |
|---|---|
| Flip | Animate between layout states (filters, grid ↔ list, expanding cards): `const s = Flip.getState(els); change(); Flip.from(s, { duration: .5, ease: "power2.inOut", absolute: true })` |
| Draggable + InertiaPlugin | Carousels, sliders, sortable lists with momentum |
| DrawSVG / MorphSVG / MotionPath | Line drawing, icon morphs, objects following a path |
| ScrollSmoother | Smooth scrolling + parallax (`data-speed`). Needs `#smooth-wrapper > #smooth-content` |
| ScrollToPlugin | Animated anchor scrolling with offset |
| Observer | Swipe/wheel/touch-driven sections (fullpage-style slides) |
| CustomEase | Brand-specific motion curves |

## React: `useGSAP`
```tsx
import { useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(useGSAP, ScrollTrigger);

export function Hero() {
  const root = useRef<HTMLDivElement>(null);
  useGSAP(() => {
    gsap.from(".hero-title", { y: 40, autoAlpha: 0, duration: 0.8 });   // selector scoped to root
  }, { scope: root });                                                    // auto-cleanup on unmount
  const { contextSafe } = useGSAP({ scope: root });
  const onClick = contextSafe(() => gsap.to(".hero-cta", { scale: 1.05, yoyo: true, repeat: 1 }));
  return <div ref={root}><h1 className="hero-title">Hello</h1><button className="hero-cta" onClick={onClick}>Go</button></div>;
}
```
- Never create tweens during render; use `useGSAP` (or `useLayoutEffect` + `gsap.context().revert()`).
- Wrap event-handler animations in `contextSafe` so they are cleaned up.
- Next.js: GSAP code only in Client Components (`"use client"`); register plugins once in a client module.
- Use `gsap.matchMedia()` for breakpoint-specific animations; it reverts automatically.

## Accessibility & reduced motion (required)
```js
const mm = gsap.matchMedia();
mm.add({ reduce: "(prefers-reduced-motion: reduce)", full: "(prefers-reduced-motion: no-preference)" }, (ctx) => {
  const { reduce } = ctx.conditions;
  gsap.from(".hero > *", { autoAlpha: 0, y: reduce ? 0 : 40, duration: reduce ? 0.01 : 0.8, stagger: reduce ? 0 : 0.1 });
});
```
- Content must be readable with JS disabled or before animations run (avoid permanent `opacity: 0` in CSS; use `gsap.set` or `autoAlpha` from-tweens, or a `.js` class gate).
- Never block reading: no scroll-jacking on long text, no pins longer than ~3 screens on mobile.
- Keep focus order and visible focus states intact when moving elements.

## Performance
- Animate `transform` (x, y, scale, rotation) and `opacity` / `autoAlpha` only. Avoid animating `top/left/width/height/box-shadow/filter` on large elements.
- Use `will-change: transform` sparingly (only on elements that animate continuously).
- Use `gsap.quickTo()` for pointer-follow effects; throttle heavy work with `gsap.ticker`.
- Lazy-register heavy plugins only on pages that use them; tree-shake by importing from `gsap/<Plugin>`.
- Kill/revert on route change (`ctx.revert()`, `ScrollTrigger.getAll().forEach(t => t.kill())` in non-React apps).

## Ready-made patterns
| Pattern | Recipe |
|---|---|
| Hero intro | timeline: nav → headline SplitText lines → sub → CTA (`"<0.1"` offsets) |
| Reveal on scroll | `ScrollTrigger.batch(".reveal", …)` |
| Number counter | `gsap.to(obj, { val: 1250, snap: { val: 1 }, onUpdate: () => el.textContent = obj.val })` |
| Magnetic button | `quickTo` x/y on `pointermove`, reset on `pointerleave` |
| Marquee | `gsap.to(".marquee-inner", { xPercent: -50, repeat: -1, duration: 20, ease: "none" })` with duplicated content |
| Page transition | timeline that covers screen → route change → uncover; or View Transitions API |
| Sticky product showcase | pinned section, scrubbed timeline swapping images/text per step |

See `templates/react-vite-shadcn` and `examples/aurora-3d` for working code.
