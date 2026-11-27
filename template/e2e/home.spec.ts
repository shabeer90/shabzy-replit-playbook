import { test, expect } from "@playwright/test";

// The first journey: the built home page loads with one main heading.
// Add each journey in docs/JOURNEYS.md as e2e/journeys/<name>.spec.ts.
test("home page loads from the built app", async ({ page }) => {
  const response = await page.goto("/");
  expect(response?.status()).toBe(200);
  await expect(page.locator("h1")).toHaveCount(1);
});
