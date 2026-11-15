# React Patterns: Best Practices, Composition, View Transitions

Applies to React 19, Next.js App Router and Vite + React projects.

## 1. Best practices (performance & correctness)

### Data fetching & waterfalls
- Fetch on the server (Server Components / route loaders) whenever possible; pass data down as props.
- Start independent requests in parallel: `const [a, b] = await Promise.all([getA(), getB()])`. Never `await` one then the other unless B needs A.
- Stream slow parts with `<Suspense fallback={<Skeleton/>}>` instead of blocking the whole page.
- Client-side server state: TanStack Query (cache, dedupe, retries) — not `useEffect` + `fetch` + `useState`.
- Mutations: Server Actions or route handlers; use `useActionState` / `useOptimistic` for pending and optimistic UI.

### Bundle size
- Keep `"use client"` boundaries as low in the tree as possible; Server Components ship zero JS.
- Lazy-load heavy, below-the-fold or interaction-only widgets: `const Chart = lazy(() => import("./Chart"))` / `next/dynamic`.
- Import specific modules (`import debounce from "lodash/debounce"`, `lucide-react` named icons); avoid barrel files that defeat tree-shaking.
- Defer third-party scripts until after interaction or idle.

### Rendering
- Derive state instead of syncing it: compute `filtered = items.filter(...)` during render; don't store it in state + effect.
- Don't define components inside components (remounts every render).
- Stable keys from data IDs, never array indexes for reorderable lists.
- `useMemo`/`useCallback` only for expensive work or when identity matters for a memoized child/effect dependency (the React Compiler removes most of the need).
- Use `useTransition` / `useDeferredValue` to keep typing responsive while filtering big lists; virtualize lists > ~200 rows (TanStack Virtual).
- Effects are for synchronizing with external systems (subscriptions, DOM APIs, timers) — always return a cleanup.

### State
- Local first (`useState`), lift only as far as needed, URL state for filters/tabs/pagination (shareable, back-button friendly), context for rarely-changing app-wide values (theme, user), a store (Zustand) for frequently-changing shared client state.
- Split contexts by update frequency so a changing value doesn't re-render unrelated consumers.

### Forms
- `react-hook-form` + `zod` resolver, or native `<form action={serverAction}>` with `useActionState`.
- Show field-level errors, disable submit while pending, keep inputs labelled.

## 2. Composition patterns (avoid boolean-prop explosion)

**Problem:** `<Card compact bordered withHeader withFooter headerIcon="x" footerAlign="right" isLoading hasError …/>` grows forever.

**Compound components** — let callers compose parts:
```tsx
const TabsCtx = createContext<{ value: string; setValue: (v: string) => void } | null>(null);
const useTabs = () => { const c = use(TabsCtx); if (!c) throw new Error("Tabs.* must be inside <Tabs>"); return c; };

export function Tabs({ defaultValue, children }: { defaultValue: string; children: React.ReactNode }) {
  const [value, setValue] = useState(defaultValue);
  return <TabsCtx value={{ value, setValue }}>{children}</TabsCtx>;
}
Tabs.List = ({ children }: { children: React.ReactNode }) => <div role="tablist">{children}</div>;
Tabs.Trigger = ({ value, children }: { value: string; children: React.ReactNode }) => {
  const t = useTabs();
  return <button role="tab" aria-selected={t.value === value} onClick={() => t.setValue(value)}>{children}</button>;
};
Tabs.Panel = ({ value, children }: { value: string; children: React.ReactNode }) =>
  useTabs().value === value ? <div role="tabpanel">{children}</div> : null;

// usage
<Tabs defaultValue="a"><Tabs.List><Tabs.Trigger value="a">A</Tabs.Trigger></Tabs.List><Tabs.Panel value="a">…</Tabs.Panel></Tabs>
```

Other patterns:
| Pattern | Use when |
|---|---|
| `children` / slots (`header`, `footer` props taking nodes) | Layout components with a few customizable regions |
| Variants via `cva` (`variant="primary" size="sm"`) | Visual options of one element — instead of many booleans |
| `asChild` / Slot (Radix) | Let a component render as a link/button the caller chooses |
| Explicit variant components (`<PrimaryButton/>`, `<DangerAlert/>`) | Variants differ in behaviour, not just style |
| Render props / function children | Caller needs internal state to render (`<Combobox>{({ open }) => …}</Combobox>`) |
| Headless hooks (`useCombobox()`) | Share logic, let each caller own markup and style |
| Controlled + uncontrolled (`value`/`defaultValue`/`onValueChange`) | Reusable inputs and widgets |

React 19 notes: `ref` is a normal prop (no `forwardRef` needed), `<Context value>` replaces `<Context.Provider>`, `use()` reads context/promises conditionally.

## 3. View Transitions (native page & element animations)

### Plain web / MPA
```css
@view-transition { navigation: auto; }                 /* cross-document fades between same-origin pages */
.product-image { view-transition-name: product-hero; } /* shared element morph between pages */
::view-transition-old(root), ::view-transition-new(root) { animation-duration: 250ms; }
@media (prefers-reduced-motion: reduce) { ::view-transition-group(*) { animation: none; } }
```

### SPA state changes
```ts
function update(fn: () => void) {
  if (!document.startViewTransition || matchMedia("(prefers-reduced-motion: reduce)").matches) return fn();
  document.startViewTransition(() => flushSync(fn));    // flushSync from react-dom so the DOM updates inside the callback
}
```
- Give each shared element a **unique** `view-transition-name` (e.g. `` `card-${id}` ``) on both the list item and the detail view.
- List reorder/filter: set names per item, wrap the state update in `startViewTransition` → items glide to new positions.

### React `<ViewTransition>` (React canary / Next.js experimental)
If the project's React version exports `ViewTransition`, wrap the changing subtree: `<ViewTransition><Page/></ViewTransition>` and trigger updates inside `startTransition`; Next.js needs `experimental.viewTransition: true`. Otherwise use the `document.startViewTransition` helper above. Check the installed version before choosing.

### Rules
- Feature-detect and fall back to an instant update.
- Keep durations 200–400 ms; respect reduced motion.
- Use View Transitions for navigation/layout changes; use GSAP (`references/animation-gsap.md`) for choreographed, scroll-driven or long timelines.
