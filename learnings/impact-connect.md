# Impact Connect

- **What it is:** A public directory of Muslim-founded startups.
- **Stack:** Express, Vite, React, TypeScript, PostgreSQL and object storage.
- **Where it runs:** Replit, with an external PostgreSQL database.
- **Dates:** August to November 2026.
- **Evidence:** Project commits, server code and regression tests were reviewed. Project paths and commit references below identify that evidence; private reports and operational data are not copied or linked. This review did not run a fresh production audit.

## 1. Keep CLI exits out of imported server modules

- **When:** August 2026.
- **Kind:** Went wrong.
- **What happened:** The logo validator was imported by the server and also contained a direct-execution CLI guard. Bundling made the CLI path run during server startup, where its exit call stopped the server. The CLI runner was moved into a separate module.
- **Impact:** A logo-validation failure could stop the whole site, rather than produce a validation result.
- **Evidence:** Commit `159fe99`; `server/scripts/validateLogos.ts` and `server/scripts/validateLogos.cli.ts`. The change removes the imported CLI exit path. The historical production outage was not reproduced during this review.
- **Home:** [Rule 17: verify on what production serves](../PLAYBOOK.md#1-the-rules), as a project example.

## 2. Await backups and handle a failed result

- **When:** August 2026.
- **Kind:** Went wrong.
- **What happened:** Logo uploads depended on local files and backup calls that were not consistently awaited. Write paths were changed to await a retrying storage helper. That helper returns a boolean, so waiting for it still does not establish success unless the caller handles `false`.
- **Impact:** Returning an upload response before a durable copy exists can leave a published image path without durable backing.
- **Evidence:** Commit `826d279`; `server/services/imageStorage.ts` and its upload callers in `server/routes.ts`. The helper retries and returns failure after exhaustion. This review does not establish that every caller rejects or reports failed backups, or that all production assets are durable.
- **Home:** [Section 11: Replit platform notes](../PLAYBOOK.md#11-replit-platform-notes).

## 3. Image existence is not a production image check

- **When:** August to November 2026.
- **Kind:** Went wrong.
- **What happened:** The logo validator checked public records in its configured database, then looked for files on disk or in storage. It did not request each published image URL or decode the response. That result could not confirm the production site had no broken logos.
- **Impact:** A reassuring validation result answered a narrower question than the user's production complaint.
- **Evidence:** `server/scripts/validateLogos.ts` checks filesystem and storage existence. In contrast, `tests/blogSocialSharing.smoke.mjs` checks response headers, PNG signature and decoded dimensions for generated social images. That test does not cover all startup logos, and no fresh all-logo production audit was run for this contribution.
- **Home:** [Rule 22: scripted live checks](../PLAYBOOK.md#1-the-rules), as a project example.

## 4. Missing images must not become HTML responses

- **When:** August 2026.
- **Kind:** Went wrong.
- **What happened:** A missing image could fall through static serving and storage fallback into the SPA response. Explicit handling was added to return 404 with `Cache-Control: no-store` when the image could not be served.
- **Impact:** An asset request could receive application HTML instead of an image. A successful HTTP status alone could hide the missing asset.
- **Evidence:** Commit `7f0a91b`; missing-asset handling in `server/index.ts`. This establishes the response-path change, not that cached HTML caused every reported broken logo.
- **Home:** [Section 8: SEO and GEO baseline](../PLAYBOOK.md#8-seo-and-geo-baseline-public-sites-launch-gate).

## 5. Decode the image used in social metadata

- **When:** November 2026.
- **Kind:** Worked.
- **What happened:** Generated blog covers needed a raster sharing image and absolute HTTPS metadata URLs. A PNG endpoint and shared URL helper were added while retaining the SVG endpoint.
- **Impact:** The sharing test checks the actual image response and agreement between metadata fields instead of accepting a plausible URL.
- **Evidence:** Commit `31e1258`; `shared/blogSocialImage.ts` and `tests/blogSocialSharing.smoke.mjs`. The smoke test starts the production bundle, checks PNG bytes, decodes 1200×630 dimensions and compares Open Graph, Twitter and JSON-LD references. It does not establish that every sharing service has refreshed its cached preview.
- **Home:** [Section 8: SEO and GEO baseline](../PLAYBOOK.md#8-seo-and-geo-baseline-public-sites-launch-gate).

## 6. Public content must not depend on a known crawler name

- **When:** November 2026.
- **Kind:** Worked.
- **What happened:** Public crawler output was incomplete, including article excerpts and missing statistics. Shared server-rendered content supplied full articles, allowed public founder content and statistics from the API's cache, without relying on a crawler allowlist.
- **Impact:** Ordinary and unfamiliar clients can receive useful public page content without executing JavaScript.
- **Evidence:** Commit `13a6868`; `server/services/publicContent.ts`, `tests/unit/publicContent.test.ts` and `tests/crawlerContent.smoke.mjs`. HTTP assertions cover ordinary visitors, named crawlers and an unknown retriever. This does not prove search indexing, rankings or the JavaScript-rendered journey.
- **Home:** [Section 8: SEO and GEO baseline](../PLAYBOOK.md#8-seo-and-geo-baseline-public-sites-launch-gate).

## 7. Check the emitted graph after splitting routes

- **When:** November 2026.
- **Kind:** Worked.
- **What happened:** Admin, founder-portal and secondary public routes were split into lazy chunks. A manifest check walks transitive static imports to catch private screens pulled into public or login entry graphs, and applies a project-specific JavaScript size budget.
- **Impact:** Route splitting gained a regression check against accidental eager imports and bundle growth.
- **Evidence:** Commit `4c7eaa1`; `tests/routeBundles.check.mjs` and `tests/routeLoading.smoke.mjs`. The manifest check enforces a 1.25 MiB budget; the browser smoke checks route loading and unauthenticated redirects. These are local built-output checks, not measurements of live page speed or verification of signed-in dashboards.
- **Home:** [Section 7: CI baseline](../PLAYBOOK.md#7-ci-baseline-pr-checksyml).
