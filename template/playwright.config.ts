import { defineConfig } from "@playwright/test";

// e2e runs against the built app, never the dev server (PLAYBOOK rule 17). Four projects passed
// in dev and broke in the build. scripts/test_release_guards.py fails CI if this points at dev.
const port = Number(process.env.E2E_PORT ?? 4173);

export default defineConfig({
  testDir: "e2e",
  use: { baseURL: `http://localhost:${port}` },
  webServer: {
    command: "<the command that serves the built output, for example pnpm preview --port 4173>",
    port,
    reuseExistingServer: false,
  },
});
