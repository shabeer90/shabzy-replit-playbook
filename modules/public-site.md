# Public sites

For any project with pages people find through search or share. Rules 11 and 22 in [PLAYBOOK.md](../PLAYBOOK.md#the-rules) are the rules; this is the launch baseline and the optional growth work.

## SEO and GEO baseline (launch gate)

- One canonical host, with the other redirecting via 308. The `metadataBase`/canonical tag on every page.
- `sitemap.xml` and `robots.txt` generated from the database. IndexNow on publish if you want Bing. Source sitemap modification dates from actual content records; omit optional dates when none exist, rather than substituting the build time (rule 9).
- JSON-LD per page type (Organization, WebSite, Product/Review, BreadcrumbList, FAQ), through the escaping helper.
- Self-hosted fonts, and `next/image` limited to a host allowlist in `config/`.
  Check that the required font files ship in the production output. For generated graphics, load those files in the renderer and wait for fonts before capture.
  *On Impact Connect:* the poster renderer needed production font paths, embedded WOFF2 files and `document.fonts.ready`. The source fix alone did not prove the fonts shipped or rendered correctly in a live release.
- A test that every page template has a title, description, canonical, H1 and JSON-LD.
- Response headers, checked separately from the HTML: compression on text responses, long caching for fingerprinted assets, revalidation for HTML. Check the production server and the published site separately (rule 17). Use the host's own settings where they're enough ([Adam Accounting lesson 3](../learnings/adam-accounting.md#3-correct-html-did-not-establish-correct-file-delivery)).
- Search Console and Bing Webmaster verified on day one. Export links and queries weekly.
- Internal links: every sitemap page linked from at least a few others.
- Missing image paths return a real 404, with `Cache-Control: no-store`, not the SPA's HTML.
  *On Impact Connect:* missing uploads could fall through to the application response. Explicit missing-asset handling now returns 404 without caching; that doesn't tell us what browsers had already cached.
- Social preview tags use absolute HTTPS image URLs and a raster format supported by the target sharing services. Fetch and decode the image, check its intended dimensions, and compare Open Graph, Twitter and JSON-LD references.
  *On Impact Connect:* generated blog previews needed a PNG derivative and absolute metadata URLs. The production-bundle smoke test decodes a 1200×630 PNG and checks that the references agree.
- For AI assistants (GEO), each page answers its main question plainly near the top, with specific, attributed facts. AI crawlers are allowed in `robots.txt` unless the owner decides otherwise.
- Public article text, public profile content and displayed statistics are available in initial HTML without JavaScript. Use the same public data and access rules for ordinary visitors and crawlers, including unfamiliar user agents. Test the served content, not just metadata or an excerpt.
  *On Impact Connect:* full article and public founder content replaced incomplete crawler output, with statistics from the API's shared cache. HTTP checks cover ordinary visitors and named and unknown crawlers; they do not prove indexing or rankings.

**Private portals are an exception to the public indexing baseline.** Put `noindex` in initial HTML before JavaScript and in app-owned response directives (`X-Robots-Tag`), including app-controlled redirects and errors. Set crawler rules at hostname-root `/robots.txt`, not just inside a portal subpath. Scope them to private routes on a shared host, so the public pages stay crawlable; blanket disallow belongs only on wholly private hosts. Keep private URLs out of public sitemaps.

Crawler instructions are not access controls. Protected routes still need authentication. Disallowing a crawl can stop the crawler reading `noindex`; a blocked URL may still appear in search. Neither directive guarantees immediate removal.

*On Ihsan:* the private staff portal needed its own initial HTML and response directives, with root robots rules scoped so its public pages stayed crawlable.

## Growth

Optional; use what fits.

- **UTM tags** on every link you post: `utm_source`, `utm_medium=social` and a campaign per post. The site records them on arrival.
- **Click tracking** to partners: signed, single-use tokens (HMAC plus a nonce), so the counts can't be inflated.
- **Cookie consent** that's accurate. The banner wording must match what's actually stored, including any fingerprint.
- **Reddit and forums:** a project skill that finds threads, checks each community's rules, and drafts replies **for the owner to post by hand**. Never automate posting.
- **Short video (Instagram and TikTok):**
  - a 30-day plan from real numbers;
  - a mix of reel types: trust, education, top-of-category, data;
  - every fact re-read on the day it's posted;
  - nothing automated until a few reels have worked.

  *On Cogniscore:* `social/30-day-plan.md`.
