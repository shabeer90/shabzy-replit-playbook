# Impact Connect

- **What it is:** a public directory of Muslim-founded startups.
- **Stack:** Express, Vite, React, TypeScript, PostgreSQL and object storage.
- **Where it runs:** Replit, with an external PostgreSQL database.
- **Dates:** August to November 2026.
- **Evidence:** project commits, server code and regression tests; private reports are summarised, never copied or linked. No fresh production audit was run.

## 1. Keep CLI exits out of imported server modules

- **When:** Aug 2026
- **Kind:** Went wrong
- **What happened:** the logo validator was imported by the server and also contained a direct-execution CLI guard. Bundling made the CLI path run during server startup, where its exit call stopped the server. The CLI runner was moved into a separate module.
- **Impact:** a logo-validation failure could stop the whole site, rather than produce a validation result.
- **Evidence:** commit `159fe99`; `server/scripts/validateLogos.ts` and `server/scripts/validateLogos.cli.ts`. The change removes the imported CLI exit path. The historical production outage was not reproduced during this review.
- **Home:** [PLAYBOOK rule 17](../PLAYBOOK.md#1-the-rules), as a project example.

## 2. Await backups and handle a failed result

- **When:** Aug 2026
- **Kind:** Went wrong
- **What happened:** logo uploads depended on local files and backup calls that were not consistently awaited. Write paths were changed to await a retrying storage helper. That helper returns a boolean, so waiting for it still doesn't establish success unless the caller handles `false`.
- **Impact:** returning an upload response before a durable copy exists can leave a published image path without durable backing.
- **Evidence:** commit `826d279`; `server/services/imageStorage.ts` and its upload callers in `server/routes.ts`. The helper retries and returns failure after exhaustion. This doesn't establish that every caller rejects or reports failed backups, or that all production assets are durable.
- **Home:** [PLAYBOOK section 11](../PLAYBOOK.md#11-replit-platform-notes).

## 3. Image existence is not a production image check

- **When:** Aug to Nov 2026
- **Kind:** Went wrong
- **What happened:** the logo validator checked public records in its configured database, then looked for files on disk or in storage. It did not request each published image URL or decode the response. That result could not confirm the production site had no broken logos.
- **Impact:** a reassuring validation result answered a narrower question than the user's production complaint.
- **Evidence:** `server/scripts/validateLogos.ts` checks filesystem and storage existence. In contrast, `tests/blogSocialSharing.smoke.mjs` checks response headers, PNG signature and decoded dimensions for generated social images. That test doesn't cover all startup logos, and no fresh all-logo production audit was run for this contribution.
- **Home:** [PLAYBOOK rule 22](../PLAYBOOK.md#1-the-rules), as a project example.

## 4. Missing images must not become HTML responses

- **When:** Aug 2026
- **Kind:** Went wrong
- **What happened:** a missing image could fall through static serving and storage fallback into the SPA response. Explicit handling was added to return 404 with `Cache-Control: no-store` when the image could not be served.
- **Impact:** an asset request could receive application HTML instead of an image. A successful HTTP status alone could hide the missing asset.
- **Evidence:** commit `7f0a91b`; missing-asset handling in `server/index.ts`. This establishes the response-path change, not that cached HTML caused every reported broken logo.
- **Home:** [PLAYBOOK section 8](../PLAYBOOK.md#8-seo-and-geo-baseline-public-sites-launch-gate).

## 5. Decode the image used in social metadata

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** generated blog covers needed a raster sharing image and absolute HTTPS metadata URLs. A PNG endpoint and shared URL helper were added while retaining the SVG endpoint.
- **Impact:** social previews are checked against the real image, not a plausible URL.
- **Evidence:** commit `31e1258`; `shared/blogSocialImage.ts` and `tests/blogSocialSharing.smoke.mjs`. The smoke test starts the production bundle, checks PNG bytes, decodes 1200×630 dimensions and compares Open Graph, Twitter and JSON-LD references. It doesn't establish that every sharing service has refreshed its cached preview.
- **Home:** [PLAYBOOK section 8](../PLAYBOOK.md#8-seo-and-geo-baseline-public-sites-launch-gate).

## 6. Public content must not depend on a known crawler name

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** public crawler output was incomplete, including article excerpts and missing statistics. Shared server-rendered content now supplies full articles, public founder content and statistics from the API's cache, without relying on a crawler allowlist.
- **Impact:** ordinary and unfamiliar clients can receive useful public page content without executing JavaScript.
- **Evidence:** commit `13a6868`; `server/services/publicContent.ts`, `tests/unit/publicContent.test.ts` and `tests/crawlerContent.smoke.mjs`. HTTP assertions cover ordinary visitors, named crawlers and an unknown retriever. This doesn't prove search indexing, rankings or the JavaScript-rendered journey.
- **Home:** [PLAYBOOK section 8](../PLAYBOOK.md#8-seo-and-geo-baseline-public-sites-launch-gate).

## 7. Check the emitted graph after splitting routes

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** Admin, founder-portal and secondary public routes were split into lazy chunks. A manifest check walks transitive static imports to catch private screens pulled into public or login entry graphs, and applies a project-specific JavaScript size budget.
- **Impact:** route splitting gained a regression check against accidental eager imports and bundle growth.
- **Evidence:** commit `4c7eaa1`; `tests/routeBundles.check.mjs` and `tests/routeLoading.smoke.mjs`. The manifest check enforces a 1.25 MiB budget; the browser smoke checks route loading and unauthenticated redirects. These are local built-output checks, not measurements of live page speed or verification of signed-in dashboards.
- **Home:** [PLAYBOOK section 7](../PLAYBOOK.md#7-ci-baseline-pr-checksyml).
