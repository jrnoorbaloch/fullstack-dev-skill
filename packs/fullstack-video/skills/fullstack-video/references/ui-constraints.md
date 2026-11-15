# UI Constraints (hard rules for every interface)

Short, opinionated rules that prevent the "AI-generated template" look and common UX bugs. Apply them to every web, mobile and desktop UI.

## Layout & spacing
- Use the spacing scale only (4/8 px steps). Never mix arbitrary values.
- Align everything to a grid; left edges of text blocks should line up.
- Generous section spacing; tight spacing inside groups (proximity shows relationships).
- Max text width ~65–75 characters. Never full-width paragraphs on desktop.
- Use `min-h-dvh` (not `h-screen`) for full-height mobile layouts; respect safe areas (`env(safe-area-inset-*)`).
- Fixed/sticky elements must not cover content or focus targets; add matching padding.

## Typography
- Max 2 font families. Body 16 px minimum on mobile (prevents iOS zoom on inputs).
- Clear hierarchy with size **and** weight; don't rely on color alone.
- `text-balance` for headings, `text-pretty` for short paragraphs; `tabular-nums` for numbers in tables, prices, timers.
- Truncate long single-line text with ellipsis and a `title`/tooltip; never let it break layout.

## Color
- One primary accent; use it for the primary action only. Neutrals do the rest.
- Status colors (success/warning/danger) only for status. Pair color with icon/text for color-blind users.
- Never pure black on pure white for large surfaces; never gray text on colored backgrounds with low contrast.
- Gradients: subtle, 2 stops, purposeful. No rainbow gradients, no glassmorphism everywhere.

## Components & interaction
- Every interactive element has hover, active, **focus-visible** and disabled states. Never remove outlines without a replacement.
- Touch targets ≥ 44×44 px with ≥ 8 px between them.
- Buttons say what they do ("Save changes", "Send invoice"), not "Submit"/"OK".
- One primary button per view; secondary actions use outline/ghost.
- Destructive actions: confirm (or offer undo), red styling, never the default focus.
- Forms: labels above inputs, helpful placeholder examples, inline validation after blur, error text under the field, keep user input on error.
- Show loading state within 100 ms of an action; skeletons that match content shape; disable double-submit.
- Empty states explain what goes here and offer the first action.
- Toasts for background results; inline messages for form errors; modals only for decisions that block the flow.
- Icons: one icon set (lucide), consistent size and stroke; icon-only buttons need `aria-label`.

## Motion
- 150–250 ms for UI feedback, 300–500 ms for larger transitions; ease-out for entering, ease-in for leaving.
- Animate transform/opacity only. Respect `prefers-reduced-motion`.
- Motion must explain (where something came from/went), never decorate for its own sake on every element.

## Content
- Real copy for the actual business; no lorem ipsum, no "Feature 1/2/3", no fake 10,000+ customer claims.
- Sentence case for UI text. Consistent terms (don't mix "Delete"/"Remove" for the same action).
- Dates/numbers/currency formatted with `Intl` for the user's locale.

## Images & media
- Always set width/height (or aspect-ratio) to prevent layout shift; `object-cover` for thumbnails.
- Meaningful `alt` text; `alt=""` for decorative images.
- No stock-photo clichés when an illustration, product shot or icon communicates better.

## Responsive
- Design at 360 px first, then 768, 1024, 1280+. Test landscape phones.
- Tables become cards or horizontal scroll on mobile; navigation collapses into an accessible menu (focus trap, Esc closes).
- Hover-only interactions must have a tap/focus equivalent.

## Accessibility (non-negotiable)
- Semantic HTML first (`button`, `nav`, `main`, `label`), ARIA only to fill gaps.
- Logical heading order, one `h1`, skip-to-content link on content-heavy sites.
- Keyboard: everything reachable and operable; visible focus; modal focus trap and return focus on close.
- Contrast ≥ 4.5:1 text, ≥ 3:1 large text and UI components.
- Announce async results with `role="status"`/`aria-live="polite"`.

## Before shipping
Run through: 360 px phone · keyboard-only · dark mode · slow 3G · empty data · error from API · very long names · RTL (if multilingual).
