# Replit platform notes

Read during setup, and whenever Replit behaves in a way the code doesn't explain. The release loop itself is in [PLAYBOOK.md](../PLAYBOOK.md#release-loop-on-replit).

These are project observations from Cogniscore, Ihsan, Impact Connect and Adam Accounting, not platform guarantees. Replit changes, so **(check current docs)** before relying on them.

- **Publishing uses the workspace copy:** pull `main` in the Shell before you publish.
- **Uploaded assets need durable storage:** do not treat the published filesystem as the permanent copy. Await the storage write and check its result before reporting that an upload is durable. If it fails, report failure or clearly mark the upload as not backed up; retries alone are not success.
  *On Impact Connect:* logo paths depended on uploaded files. Backup calls were made awaitable with retries, but the helper still returns `false` when they fail, so callers must handle that result. This is not evidence that every production logo is backed up.
  [Replit's current guidance](https://docs.replit.com/build/troubleshooting) says published filesystems are not persistent; use [App Storage](https://docs.replit.com/features/data-and-storage/object-storage) or another durable store for uploads (checked 27 Nov 2026).
- **Playwright on Replit (NixOS):** Playwright's downloaded Chromium can't find its system libraries.
  - Install the Nix `chromium` package.
  - Set `executablePath` from `which chromium` in `playwright.config`.
  - Add `--no-sandbox --disable-setuid-sandbox --disable-dev-shm-usage`.
  - Prefer `http://localhost:<port>` for isolated app checks. Cogniscore recorded a preview access problem attributed to mTLS; that is not a blanket restriction on headless preview access. Ihsan ran browser checks through its preview proxy. Current preview authentication and any mTLS requirement depend on the environment **(check current docs)**.
- **Preview proxy and synthetic QA:** check what reaches the app before assuming a browser-supplied client IP isolates a login bucket. Keep reserved synthetic-account transport inside the non-production test harness, targeting the real local API with unchanged password, session and rate-limit checks (rule 18). Never route real-user credentials this way, weaken production authentication, or raise, disable or globally reset limits to pass QA.
  *On Ihsan:* preview IP handling made repeated synthetic logins share a rate-limit bucket. A test-only local transport isolated those logins without changing application security.
- **Preview crawler headers:** check app-owned HTTP responses directly at the local service and production server, then check the proxied response separately. A proxy's `noindex` is not evidence that the app sends it, and is not a reason to remove platform headers. Current proxy header behaviour is environment-specific **(check current docs)**.
  *On Ihsan:* the preview proxy added broad `noindex` headers, including on public pages. Direct app checks separated the app's policy from the proxy's additions.
- **Separate dev and production build output** (`distDir` by phase in `next.config`). A production build into the dev server's `.next` broke the preview with missing chunks.
- **One launcher per port.** Use the managed workflow for the Run button, and don't add a second "Start application". Competing launchers caused port conflicts, and left the app marked stopped while it was actually serving. Write the port map down in `.agents/memory/`.
- **pnpm workspace:** if `.replit` says `stack = "PNPM_WORKSPACE"`, make sure `pnpm-workspace.yaml` and `tsconfig.base.json` exist. Without them, workspace packages silently get no dependencies.
- **`postMerge` script:** keep it non-interactive with a frozen lockfile (`pnpm install --frozen-lockfile --prefer-offline`). Fix a conflicted lockfile on its own, from the merged manifests, not by discarding one side.
- **A root-level app can't write `.replit-artifact/artifact.toml` directly.** Register it with `createArtifact`, then swap the config with `verifyAndReplaceArtifactToml`, keeping `[[integratedSkills]]` verbatim.
  If publishing can't find an app whose artifact files are still there, compare the registered artifacts with the files before touching run commands. On Adam Accounting, registration was lost after an external CLI installer ran; resubmitting the existing manifests through the artifact tool fixed it ([lesson 4](../learnings/adam-accounting.md#4-artifact-files-remained-after-their-registration-was-lost)). The installer's role wasn't reproduced **(check current docs)**. Read an installer before running it, and check what config it changed.
- **Replit's built-in database is not your database.** If the project uses Supabase or another external DB, schema changes go there, through its SQL editor or a management connection, never into a Replit DB as a substitute.
