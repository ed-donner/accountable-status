import { expect, test } from "@playwright/test";

const control = "http://127.0.0.1:8794";

async function standIn(action: "start" | "stop" | "state"): Promise<boolean> {
  const response = await fetch(`${control}/${action}`);
  if (!response.ok) throw new Error(`Stand-in ${action} failed with ${response.status}`);
  return ((await response.json()) as { running: boolean }).running;
}

test("first run shows 90 days of sample history and its incidents", async ({ page }) => {
  await standIn("start");
  await page.goto("/");
  await expect(page.getByTestId("service-name")).toHaveText("Accountable");
  await expect(page.getByTestId("uptime-bar")).toHaveCount(90);

  const colors = await page.getByTestId("uptime-bar").evaluateAll((els) => els.map((e) => e.getAttribute("data-color")));
  expect(colors).toContain("green");
  expect(colors.some((c) => c === "amber" || c === "red")).toBe(true);

  const closed = page.locator('[data-testid="incident"][data-open="false"]');
  expect(await closed.count()).toBeGreaterThanOrEqual(3);
  await expect(page.getByTestId("response-chart")).toBeVisible();

  await page.getByTestId("uptime-bar").nth(40).hover();
  await expect(page.getByTestId("uptime-tooltip")).toContainText("%");
});

test("an incident opens when the service stops and closes when it comes back", async ({ page }) => {
  await standIn("start");
  await page.goto("/");
  await expect(page.getByTestId("service-state")).toContainText("Up", { timeout: 15_000 });

  try {
    await standIn("stop");
    await expect(async () => {
      await page.reload();
      await expect(page.getByTestId("service-state")).toBeVisible({ timeout: 5_000 });
      await expect(page.getByTestId("incident-open")).toHaveCount(1, { timeout: 2_000 });
    }).toPass({ timeout: 30_000 });
    await expect(page.getByTestId("service-state")).toContainText("Down");
  } finally {
    await standIn("start");
  }

  await expect(async () => {
    await page.reload();
    await expect(page.getByTestId("service-state")).toBeVisible({ timeout: 5_000 });
    await expect(page.getByTestId("incident-open")).toHaveCount(0, { timeout: 2_000 });
  }).toPass({ timeout: 30_000 });
  await expect(page.getByTestId("service-state")).toContainText("Up");
});
