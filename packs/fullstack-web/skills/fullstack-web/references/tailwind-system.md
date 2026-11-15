# Tailwind Design System & Component Architecture

How to turn `references/design-system.md` into a scalable Tailwind setup (Tailwind v4, CSS-first config).

## 1. Tokens with `@theme`
```css
/* src/index.css */
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));

@theme {
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-display: "Plus Jakarta Sans", var(--font-sans);
  --radius-sm: 6px; --radius-md: 10px; --radius-lg: 16px;
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --animate-fade-up: fade-up 0.5s var(--ease-out-expo) both;
  @keyframes fade-up { from { opacity: 0; transform: translateY(12px); } }
}

/* Semantic colors as CSS variables so themes switch at runtime */
:root {
  --background: oklch(1 0 0);       --foreground: oklch(0.21 0.03 265);
  --muted: oklch(0.97 0.01 265);    --muted-foreground: oklch(0.55 0.03 265);
  --primary: oklch(0.51 0.23 277);  --primary-foreground: oklch(0.98 0 0);
  --border: oklch(0.92 0.01 265);   --ring: var(--primary);
  --destructive: oklch(0.58 0.22 27);
}
.dark {
  --background: oklch(0.15 0.03 265); --foreground: oklch(0.97 0.01 265);
  --muted: oklch(0.22 0.03 265);      --muted-foreground: oklch(0.7 0.03 265);
  --primary: oklch(0.68 0.18 277);    --primary-foreground: oklch(0.15 0.03 265);
  --border: oklch(0.28 0.03 265);
}
@theme inline {
  --color-background: var(--background); --color-foreground: var(--foreground);
  --color-muted: var(--muted);           --color-muted-foreground: var(--muted-foreground);
  --color-primary: var(--primary);       --color-primary-foreground: var(--primary-foreground);
  --color-border: var(--border);         --color-ring: var(--ring);
  --color-destructive: var(--destructive);
}
```
Components then use **semantic** classes (`bg-background text-foreground border-border bg-primary`), never raw palette classes like `bg-indigo-600`, so a brand change is a token change.

Tailwind v3 projects: same idea with `theme.extend.colors.primary = "hsl(var(--primary))"` in `tailwind.config.js`.

## 2. Variants with `cva` + `cn`
```ts
// lib/utils.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
export const cn = (...inputs: ClassValue[]) => twMerge(clsx(inputs));
```
```tsx
// components/ui/button.tsx
import { cva, type VariantProps } from "class-variance-authority";
const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        outline: "border border-border bg-transparent hover:bg-muted",
        ghost: "hover:bg-muted",
        destructive: "bg-destructive text-white hover:bg-destructive/90",
      },
      size: { sm: "h-8 px-3", md: "h-10 px-4", lg: "h-12 px-6 text-base", icon: "size-10" },
    },
    defaultVariants: { variant: "default", size: "md" },
  },
);
export function Button({ className, variant, size, ...props }: React.ComponentProps<"button"> & VariantProps<typeof buttonVariants>) {
  return <button className={cn(buttonVariants({ variant, size }), className)} {...props} />;
}
```
- `className` is always the last argument to `cn` so callers can override.
- One `cva` per component; variants are **visual** options. Behavioural differences → separate components (`references/react-patterns.md`).

## 3. Component layers
```
components/
  ui/          primitives: button, input, label, card, dialog, dropdown, tabs, badge, skeleton, toast (shadcn/ui or own)
  blocks/      composed sections: hero, pricing-table, feature-grid, data-table, sidebar-nav
  <feature>/   app-specific: order-list, invoice-form
```
- Primitives: no business logic, fully accessible (use Radix / shadcn under the hood for dialogs, menus, popovers, tabs).
- Blocks: assemble primitives, accept content via props/slots.
- Install shadcn components with `npx shadcn@latest add button card dialog …` — they are copied into the project and can be edited.

## 4. Conventions
- Class order: layout → box → typography → visual → state (Prettier `prettier-plugin-tailwindcss` sorts automatically).
- Extract a component when a class list repeats 3+ times — not `@apply` soup. `@apply` only for third-party markup you can't add classes to.
- Responsive: mobile-first (`md:`, `lg:`), container queries (`@container`, `@md:`) for reusable cards.
- State styling: `data-[state=open]:`, `aria-selected:`, `group-hover:`, `peer-invalid:`.
- RTL: logical utilities (`ms-4`, `pe-2`, `start-0`, `text-start`) and `rtl:` variant when needed.
- Dark mode: toggle `.dark` on `<html>`, store choice in `localStorage` (try/catch), default to `prefers-color-scheme`.

## 5. Checklist
- [ ] All colors/radii/fonts come from tokens
- [ ] Every interactive primitive has focus-visible, disabled and loading styles
- [ ] Variants via `cva`, merged with `cn`
- [ ] Light and dark both pass contrast
- [ ] No arbitrary values (`w-[437px]`) unless truly one-off
