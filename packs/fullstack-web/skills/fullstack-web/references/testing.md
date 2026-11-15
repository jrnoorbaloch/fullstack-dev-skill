# Testing

Minimum for every project: tests for core business logic and every API endpoint, plus one end-to-end test of the main user flow when there is a UI. Run them with `scripts/verify.py`.

## What to test
| Layer | Test | Tool |
|---|---|---|
| Pure logic (prices, totals, validation) | Unit | Vitest / Jest / pytest |
| API endpoints | Integration with a test DB | supertest, FastAPI TestClient, Laravel/Django test clients |
| Components | Render + interaction | React Testing Library, Flutter widget tests |
| Full flows (sign up → create → pay) | End-to-end in a real browser | Playwright |
| Mobile | Unit + E2E | Jest + React Native Testing Library, Maestro / Detox |

Always test: happy path, validation errors, unauthorized access (user A cannot read user B's data), empty states, edge values (0, negative, very long input).

## Vitest (Node / Next.js)
```bash
npm i -D vitest @testing-library/react @testing-library/jest-dom jsdom
```
```ts
// vitest.config.ts
import { defineConfig } from "vitest/config";
export default defineConfig({ test: { environment: "jsdom", globals: true } });
```
```ts
import { describe, it, expect } from "vitest";
import { cartTotal } from "./cart";
describe("cartTotal", () => {
  it("applies discount but never below zero", () => {
    expect(cartTotal([{ price: 100, qty: 2 }], 250)).toBe(0);
  });
});
```

## API test (Express + supertest)
```ts
import request from "supertest";
import { app } from "../src/app";
it("rejects unauthenticated requests", async () => {
  await request(app).get("/api/items").expect(401);
});
```

## pytest (FastAPI)
See `templates/fastapi-api/tests/test_api.py`: in-memory SQLite via `StaticPool`, dependency override for the session, helper that registers and logs in a user.

## Playwright (end-to-end)
```bash
npm init playwright@latest
```
```ts
import { test, expect } from "@playwright/test";
test("visitor can send the contact form", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Name").fill("Sara");
  await page.getByLabel("Email").fill("sara@example.com");
  await page.getByLabel("Message").fill("Hello");
  await page.getByRole("button", { name: "Send" }).click();
  await expect(page.getByRole("status")).toContainText("Thanks");
});
```
- Prefer `getByRole` / `getByLabel` (also checks accessibility).
- Use `webServer` in `playwright.config.ts` to start the app automatically.
- Run on mobile viewport too: `projects: [{ name: "mobile", use: devices["Pixel 7"] }]`.

## Accessibility test
```bash
npm i -D @axe-core/playwright
```
```ts
import AxeBuilder from "@axe-core/playwright";
const results = await new AxeBuilder({ page }).analyze();
expect(results.violations).toEqual([]);
```

## CI
Run lint, type-check, unit and E2E tests on every push (see `references/deploy.md` → GitHub Actions). Block merges when tests fail.
