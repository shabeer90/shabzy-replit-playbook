# Adam Accounting

- **What it is:** a public website for a UK accountancy firm.
- **Stack:** React, Vite, TypeScript, Tailwind, an Express contact API, Supabase and Resend.
- **Where it runs:** Replit, in a pnpm workspace.
- **Dates:** May to November 2026.
- **Evidence:** available local git history, project notes, agent memory and test scripts. The checkout was shallow; GitHub PR descriptions were not reviewed. Private reports are summarised here, not copied or linked. No fresh production or security audit was run for this contribution.

## 1. A mobile speed fix changed the desktop layout

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** critical CSS meant for the mobile homepage also applied on desktop. The project recorded timing-dependent desktop layout shifts. Scoping the critical CSS to mobile kept desktop on its normal stylesheet.
- **Impact:** improving mobile loading needed a separate desktop regression check. The project added repeated Lighthouse runs for both devices, metric budgets and functional checks.
- **Evidence:** commit `7e43d53`; `artifacts/adam-accounting/scripts/performance-check.mjs`, `scripts/regression-check.mjs` and `QUALITY-CHECKS.md`. The recorded local production-build results had no measured layout shift on either device. They do not guarantee the same score at the published edge or on a different Lighthouse version.
- **Home:** [PLAYBOOK section 7, optional public-site performance checks](../PLAYBOOK.md#7-ci-baseline-pr-checksyml).

## 2. An SSR conditional kept eager imports in the browser bundle

- **When:** Nov 2026
- **Kind:** Went wrong
- **Repeat of:** impact-connect lesson 7
- **What happened:** an eager page registry sat behind an SSR conditional in a shared application module. Browser bundling retained initialisation side effects from those imports. Moving the registry into a separate server-only module removed that path from the browser entry.
- **Impact:** initial browser JavaScript fell from about 428KB to 198KB uncompressed, without removing page content.
- **Evidence:** commit `7e43d53`; `artifacts/adam-accounting/src/App.tsx`, `src/ssr-pages.ts` and the recorded build measurements. The regression script enforces an initial JavaScript budget and exercises direct loads and navigation. A conditional in source alone did not establish the emitted boundary.
- **Home:** [PLAYBOOK section 7, built import graphs](../PLAYBOOK.md#7-ci-baseline-pr-checksyml).

## 3. Correct HTML did not establish correct file delivery

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** project notes recorded uncompressed delivery and both public hosts returning pages. A small production file server added compression negotiation, permanent canonical-host redirects, cache policies and real 404s while retaining pre-rendered pages.
- **Impact:** the project could test its delivery contract independently of page markup and keep the separate contact API unchanged.
- **Evidence:** commit `acbe766`; `artifacts/adam-accounting/scripts/serve.mjs`, `scripts/serve.test.mjs` and `SEO-NOTES.md`. Tests cover gzip and Brotli decoding, redirects, cache headers and missing pages. They verify the local server, not every response through the published edge. This is a project hosting choice, not a claim that every site needs a custom server.
- **Home:** [PLAYBOOK section 8, delivery checks](../PLAYBOOK.md#8-seo-and-geo-baseline-public-sites-launch-gate).

## 4. Artifact files remained after their registration was lost

- **When:** Jul 2026
- **Kind:** Went wrong
- **What happened:** project memory records missing artifact registrations after an external CLI installer ran, although artifact files remained on disk. The recorded recovery resubmitted the existing manifests through the validated artifact tool.
- **Impact:** publishing was blocked even though the application files and serving configuration still existed.
- **Evidence:** commit `8e82e30` and `.agents/memory/artifact-reregistration.md`. These record the incident and recovery. The installer's causal role was not independently reproduced during this contribution, and the recovery is not a platform guarantee.
- **Home:** [PLAYBOOK section 11, artifact registration](../PLAYBOOK.md#11-replit-platform-notes). Check current docs before using the recorded recovery.

## 5. Awaiting an email call did not establish success

- **When:** Nov 2026
- **Kind:** Went wrong
- **Repeat of:** impact-connect lesson 2, cogniscore lesson 7
- **What happened:** the contact route awaited the email SDK but ignored its returned error. It now checks both the error and the provider's returned message ID. When email fails and the submission was not saved to the database, the route returns failure rather than a success response.
- **Impact:** a failed, unsaved enquiry no longer gets reported as accepted merely because the awaited call returned. A saved enquiry can still succeed when its notification fails.
- **Evidence:** commit `ea257b2`; `artifacts/api-server/src/routes/contact.ts`. Browser regression checks mock contact responses and preserve entered values on failure. They do not test the email provider, sender-domain verification or inbox delivery. Provider acceptance is not proof of delivery.
- **Home:** [PLAYBOOK rule 20](../PLAYBOOK.md#1-the-rules).

## 6. Sitemap dates need an editorial source

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** the sitemap stopped assigning modification dates to static pages and the blog listing where there was no reliable modification record. Article dates continued to come from editorial records.
- **Impact:** undated pages no longer claimed a modification date without a supporting record.
- **Evidence:** commit `b66996b`; `artifacts/adam-accounting/scripts/prerender.mjs`, the date-policy assertions in `scripts/regression-check.mjs` and `SEO-NOTES.md`. These establish how dates are generated, not that every article's facts are current.
- **Home:** [PLAYBOOK rule 9](../PLAYBOOK.md#1-the-rules); the sitemap item in section 8 links to it.

## 7. Filled form fields needed their own readability check

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** a user reported white text in filled contact fields. Scoped form CSS set explicit text, background, caret and browser autofill text colours.
- **Impact:** a form could look correct while empty but become unreadable when used.
- **Evidence:** commit `cf060d9`; `artifacts/adam-accounting/src/components/ContactForm.css` and the filled-field text-colour checks in `scripts/regression-check.mjs`. The automated test fills fields; it does not exercise every browser's native saved-details autofill or theme.
- **Home:** [QA agent test plan](../template/.claude/agents/qa-tester.md#test-plan-write-it-first-briefly).

## 8. An SEO warning did not always need a code change

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** the SEO review separated actionable findings from warnings that did not justify a change. It kept the established business domain and consistent navigation labels, and treated decorative backgrounds differently from content images.
- **Impact:** the site could address real problems without changing useful content or business identity just to satisfy a checker.
- **Evidence:** commit `acbe766`; `artifacts/adam-accounting/SEO-NOTES.md`, especially its findings that did not need a code change. The notes record the reasoning, not a measured ranking improvement. A decorative image can use empty alt text or an appropriate CSS background; conversion is not automatically required by a warning.
- **Home:** [CMO review of audit findings](../template/.claude/agents/cmo-reviewer.md#findability-public-websites).

## 9. Short search titles did not need short article headlines

- **When:** Nov 2026
- **Kind:** Worked
- **What happened:** search titles and descriptions were shortened while full article headlines and copy were kept. A shared metadata helper applied the same choices when a post came from bundled content or the CMS.
- **Impact:** search metadata could fit the project's audit budget without removing useful detail from the article.
- **Evidence:** commit `b66996b`; `artifacts/adam-accounting/src/lib/blog-seo.ts`, `src/pages/blog/post.tsx` and `SEO-NOTES.md`. The regression script checks title width and initial versus rendered metadata. Its pixel-width budget is project-specific, not a universal search-engine limit or a promise about the snippet shown.
- **Home:** [CMO title checks](../template/.claude/agents/cmo-reviewer.md#seo).

## 10. The first paint was unstyled before JavaScript loaded the CSS

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** server-rendered content appeared in preview before Vite's JavaScript injected the global styles. The page briefly showed unstyled content and an oversized icon. The preview renderer was changed to link the stylesheet directly from its initial HTML.
- **Impact:** a screenshot taken after loading could miss a visible problem during page startup.
- **Evidence:** commit `9d1e836`; `artifacts/adam-accounting/vite.config.ts`, including the comment explaining the stylesheet link. This establishes the preview loading-order change. It does not show that production had the same fault, or replace a production-build check.
- **Home:** [QA loading-state checks](../template/.claude/agents/qa-tester.md#test-plan-write-it-first-briefly).

## 11. An ARIA label alone did not make the star rating accessible

- **When:** Nov 2026
- **Kind:** Went wrong
- **What happened:** a testimonial star group had an accessible label on a generic div and triggered an accessibility-tree failure. Giving the group an appropriate image role made its meaning explicit while keeping the individual decorative stars hidden from screen readers.
- **Impact:** the rating gained semantics that an accessibility check could inspect, rather than only looking correct.
- **Evidence:** commit `367dde1`; `artifacts/adam-accounting/src/components/TestimonialsSlider.tsx`. The regression script checks for an image named "5 out of 5 stars" and runs automated accessibility checks. This does not establish that every screen reader and browser combination was tested.
- **Home:** [Design agent semantic-accessibility checks](../template/.claude/agents/head-of-design.md#when-youre-called-to-add-something).
