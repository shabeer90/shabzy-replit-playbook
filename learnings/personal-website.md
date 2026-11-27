# Personal Website

- **What it is:** A public portfolio, case studies and blog.
- **Stack:** React, TypeScript, Vite, Tailwind CSS and static prerendering.
- **Where it runs:** Replit.
- **Dates:** June to November 2026.
- **Evidence:** Current source and local Git history. No project-owned retros, tests or CI were found; PR descriptions were unavailable.

## 1. Check focus contrast on every surface

- **When:** Sep–Nov 2026
- **Kind:** Went wrong
- **What happened:** The site used cyan as its only global focus outline. It stood out on dark backgrounds but had only 1.08:1 contrast against a light Ventures panel. A dark halo was added for links and as the button ring offset, while keeping the cyan accent.
- **Impact:** Keyboard focus could be hard to see on light panels. The paired indicator has a contrasting color on both the light and dark surfaces.
- **Evidence:** Commits `3182c8c` and `eba5f59`; `src/index.css` and `src/components/Button.tsx`. The new dark token contrasts 13.95:1 with the Ventures panel and cyan contrasts 12.94:1 with the dark page. No browser-based focus test is part of the project.
- **Home:** [PLAYBOOK section 9](../PLAYBOOK.md#9-writing-and-design-quality), design/accessibility baseline.

## 2. Case-study titles should describe the engagement

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** Case studies used titles that named the site and company but not the work. Each now has a title tied to its product, design or leadership engagement. The client page and prerendered HTML read the title from the same case-study data.
- **Impact:** Search titles describe the study's subject more clearly. The build check covered all five prerendered case-study routes; rankings were not measured.
- **Evidence:** Commit `b89f046`; `src/data/caseStudies.ts`, `src/pages/CaseStudy.tsx` and `scripts/prerender.mjs`.
- **Home:** [PLAYBOOK section 8](../PLAYBOOK.md#8-seo-and-geo-baseline-public-sites-launch-gate), page-title checklist.

## 3. Latest lists should use publication dates

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** The home page's blog preview was a hard-coded list of four posts from 2025, 2024 and 2023, although newer articles existed. It now sorts the shared post data by publication date and selects five.
- **Impact:** New articles were missing from a prominent internal-link list. The prerendered home page now contains the five newest entries; traffic and ranking changes were not measured.
- **Evidence:** Commit `37c8a90`; `src/pages/Home.tsx` and `src/data/blogPosts.ts`.
- **Home:** [PLAYBOOK section 8](../PLAYBOOK.md#8-seo-and-geo-baseline-public-sites-launch-gate), internal-link and freshness checks.

## 4. Serve responsive cover images

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** Blog articles loaded full-size cover images even though smaller thumbnails existed for the list. Each article now selects 640px or 900px WebP sources, with the original image as fallback.
- **Impact:** The 20 originals totalled about 17 MB. Both responsive variant sets totalled about 1.2 MB; each page can load a source suited to its rendered width.
- **Evidence:** Commit `b89f046`; `src/pages/BlogPost.tsx` and the 40 generated files in `public/blog-images/`. The build check verified the sources for all 20 articles; live transfer sizes were not measured.
- **Home:** [PLAYBOOK section 8](../PLAYBOOK.md#8-seo-and-geo-baseline-public-sites-launch-gate), image-delivery checklist.

## 5. Keep prerendered and client trees aligned

- **When:** Sep 2026
- **Kind:** Went wrong
- **What happened:** A lazy route's client Suspense fallback replaced prerendered page content during hydration. The skip link and Suspense boundaries were aligned between the server and client.
- **Impact:** Hydration recovery replaced the rendered page and caused a recorded layout shift. Matching both trees removed the recovery error and shift.
- **Evidence:** Commit `1b5b42c`; `src/entry-server.tsx` and `src/main.tsx`. A browser trace against the built site showed the mismatch and layout shift; it does not establish that the reviewed change was deployed live.
- **Home:** [PLAYBOOK rule 17](../PLAYBOOK.md#1-the-rules), production-output verification.

## 6. Unknown static routes need a real 404

- **When:** Jun 2026
- **Kind:** Went wrong
- **What happened:** A blanket SPA rewrite served the home-page HTML with status 200 for unknown paths. It was replaced with rewrites for known routes and a 404 catch-all.
- **Impact:** Unknown blog and case-study URLs could appear to exist, creating soft 404s for visitors and crawlers.
- **Evidence:** Commit `3fd5ecd`; `public/_redirects`. The configuration shows the catch-all change; no live HTTP status check is recorded.
- **Home:** [PLAYBOOK rule 17](../PLAYBOOK.md#1-the-rules), route and status-code verification.
