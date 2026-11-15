# Design System

Use these rules so every product looks deliberate and professional. Pick one clear visual direction per project and apply it everywhere.

## 1. Pick a direction first
| Direction | Use for | Look |
|---|---|---|
| Clean / minimal | SaaS, tools, clinics | White space, one accent color, neutral grays |
| Bold / vibrant | Food, events, kids, marketing | Saturated colors, big type, rounded shapes |
| Dark / premium | Tech, gaming, luxury | Dark surfaces, glowing accent, subtle borders |
| Warm / friendly | Bakeries, cafés, local shops | Cream backgrounds, warm accent, soft shadows |
| Corporate / trust | Finance, legal, real estate | Navy/teal, structured grids, restrained type |

## 2. Color tokens
Define tokens once (CSS variables or Tailwind theme) and never hard-code hex values in components.

```css
:root {
  --bg: #ffffff;       --surface: #f8fafc;   --border: #e2e8f0;
  --text: #0f172a;     --muted: #64748b;
  --primary: #4f46e5;  --primary-fg: #ffffff;
  --success: #16a34a;  --warning: #d97706;   --danger: #dc2626;
}
.dark {
  --bg: #020617;       --surface: #0f172a;   --border: #1e293b;
  --text: #f1f5f9;     --muted: #94a3b8;
  --primary: #818cf8;  --primary-fg: #0b1020;
}
```
- One primary color, at most one secondary accent. Status colors only for status.
- Text contrast ≥ 4.5:1 (≥ 3:1 for large text and icons).
- Ready palettes: indigo `#4f46e5`, emerald `#059669`, rose `#e11d48`, amber `#d97706`, sky `#0284c7`, slate `#334155`.

## 3. Typography
- Fonts: Inter, Geist, Plus Jakarta Sans, Poppins (Latin); **Noto Nastaliq Urdu** / **Noto Naskh Arabic** (Urdu/Arabic); **Noto Sans Devanagari** (Hindi).
- Scale (px): 12 · 14 · 16 (body) · 18 · 20 · 24 · 30 · 36 · 48 · 60.
- Line height 1.5 for body, 1.1–1.25 for headings. Max line length ~70 characters.
- Weights: 400 body, 500–600 labels/buttons, 700–800 headings.

## 4. Spacing, radius, shadow
- 4/8 px spacing scale: 4, 8, 12, 16, 24, 32, 48, 64, 96.
- Sections: 64–112 px vertical padding on desktop, 48–64 on mobile.
- Radius: 6 (inputs), 10–12 (buttons, cards), 16–24 (large cards, modals), full (pills/avatars). Be consistent.
- Shadows: subtle (`0 1px 2px rgb(0 0 0 / .06)`) for cards, stronger only for floating layers (menus, modals).

## 5. Layout
- Container max-width 1120–1280 px, side padding 16 px (mobile) / 24–32 px (desktop).
- Mobile-first breakpoints: 640, 768, 1024, 1280.
- Grids: 1 column on mobile → 2 → 3/4 on desktop. Dashboards: sidebar 240–280 px + content.

## 6. Components (behaviour every component must have)
| Component | Rules |
|---|---|
| Button | Primary / secondary / ghost / destructive variants; 40–44 px tall; visible focus ring; disabled + loading state |
| Input | Visible label, placeholder is not a label, error message under field, 44 px touch target |
| Card | Surface color, border or subtle shadow, consistent padding (16–24 px) |
| Navbar | Logo left, links center/right, primary CTA, collapses to menu on mobile, sticky when useful |
| Table | Sticky header, zebra or row dividers, right-aligned numbers, empty state, pagination |
| Modal | Focus trap, Esc to close, overlay click closes non-destructive modals |
| Toast | Short message, auto-dismiss 3–5 s, `role="status"` |
| Empty state | Icon or illustration, one-line explanation, primary action |
| Skeleton | Same shape as the content it replaces |

Libraries: **shadcn/ui** (React), **Radix**, **Headless UI**, **NativeWind** (React Native), **Material 3** (Flutter). Icons: **lucide**.

## 7. Motion
- 150–250 ms ease-out for hovers and small transitions; 250–400 ms for panels/modals.
- Animate opacity and transform only. Respect `prefers-reduced-motion`.

## 8. RTL & multilingual
- Set `dir="rtl"` and `lang` on `<html>` for Urdu/Arabic. Use logical properties (`margin-inline-start`, Tailwind `ms-/me-/ps-/pe-`).
- Mirror directional icons (arrows, chevrons) in RTL. Never mirror logos or media controls.
- Allow 30–40% extra width for translated text.

## 9. Final design check
- [ ] One visual direction, applied consistently
- [ ] Tokens used, no random colors or spacing
- [ ] Looks right at 360 px, 768 px, 1280 px
- [ ] Dark mode (if offered) has no unreadable text
- [ ] All interactive elements have hover, focus and disabled states
- [ ] Real content, no lorem ipsum, no broken images
