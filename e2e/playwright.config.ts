import { defineConfig, devices } from "@playwright/test";

/**
 * Runs the full stack and hits /academy/apply as a real user would.
 * Playwright starts the Vite dev server automatically; if you want
 * hits against the real FastAPI backend, run `make dev` in another
 * terminal and remove the webServer block.
 */
export default defineConfig({
  testDir: "./tests",
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? "github" : [["list"], ["html", { open: "never" }]],

  use: {
    baseURL: process.env.E2E_BASE_URL || "http://localhost:5173",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },

  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
  ],

  webServer: process.env.E2E_BASE_URL
    ? undefined
    : {
        command: "npm run dev -- --port 5173",
        cwd: "../frontend",
        port: 5173,
        reuseExistingServer: !process.env.CI,
        timeout: 60_000,
      },
});
