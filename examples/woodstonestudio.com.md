> **Example report.** A real run of the **full version** ([GEO Agent Team](https://buy.polar.sh/polar_cl_f2U4MFgb5c5drxsz566CbomAj2BGhgQ2Ou8qG3Wf2CZ), 78 signals, v1.1.2) on our own site, 1 November 2026. Two changes since that run: the total is shown with the v1.1.3 rounding rule (round down, so a site with an open issue never shows 100), and one note was removed. It said the visible FAQ did not match the FAQPage schema; that was wrong, because the collector did not read FAQ questions inside `<details>` toggles. Fixed in v1.1.4, which now checks every schema question against the visible page text. The free version in this repo produces the same kind of report on the 24 most important of these signals.

# woodstonestudio.com — Google + AI search readiness

**Score: 99/100 · Excellent** — score excludes mobile speed (Google PageSpeed returned "429 rate limit"; covers 92 % of the applicable signal weight; unrounded 99.52)
Audited: 2026-11-01 · Homepage only (https://woodstonestudio.com, Turkish version) · 78 signals in 10 areas

## In short
1. **Search engines and AI assistants can read the whole site.** robots.txt allows every search and AI bot. All six live bot tests (Google, Bing, ChatGPT ×2, Claude, Perplexity) got a 200 and the same 1,479 words a browser gets. llms.txt is served as plain text and all its links work.
2. **Mobile speed is the one thing we could not check.** PageSpeed refused the request, so the performance score, LCP, CLS and TBT are unmeasured and left out of the score. The page loads 76 scripts (none render-blocking), so this is worth checking at pagespeed.web.dev.
3. **Only one measured signal fails:** there is no Content-Security-Policy header. It is a minor security hardening step, not a visibility problem.

## Areas
| Area | Score | Pass | Partial | Fail |
|---|---|---|---|---|
| AI access | 100 | 9 | 0 | 0 |
| Technical SEO | 100 | 12 | 0 | 0 |
| Speed | 100 | 7 | 0 | 0 |
| Brand and entity | 100 | 7 | 0 | 0 |
| Content and answers | 100 | 8 | 0 | 0 |
| Structured data | 100 | 4 | 0 | 0 |
| Security | 94 | 8 | 0 | 1 |
| Contact and conversion | 100 | 5 | 0 | 0 |
| Sharing | 100 | 5 | 0 | 0 |
| Language | 100 | 4 | 0 | 0 |

Not counted: `speed.perf`, `speed.lcp`, `speed.cls`, `speed.tbt` are `unknown` (PageSpeed 429). `brand.address`, `schema.local` and `contact.map` are `na` because this is an online-only business (no address, no LocalBusiness type, `areaServed`: Turkey, Albania, Worldwide). `tech.applinks` is `na` because the JoVVo and ShqipTR apps are separate products that don't open this site's links. The Speed score of 100 covers only the 7 speed signals we could measure.

## Can AI assistants read the site?
| Bot | robots.txt | Live test (hint) |
|---|---|---|
| Googlebot / Bingbot | Allowed (`*` → Allow: /) | 200 · 1,479 words · same content |
| ChatGPT (OAI-SearchBot, ChatGPT-User) | Allowed (own groups, Allow: /) | 200 · 1,479 words · same content |
| Claude (Claude-SearchBot) | Allowed (falls under `*`) | 200 · 1,479 words · same content |
| Perplexity (PerplexityBot) | Allowed (own group, Allow: /) | 200 · 1,479 words · same content |
| Training bots (GPTBot, ClaudeBot, Google-Extended, CCBot, Applebot-Extended) | Allowed. This is a choice, not an error. There is no `__usage_ai-training` opt-out group. | — |

## Fix list (most important first)

### 1. Mobile speed (PageSpeed score, LCP, CLS, TBT) · Critical weight, not measured
- **What we saw:** The PageSpeed Insights API returned HTTP 429 (rate limit), so we have no lab numbers. The page has 76 `<script>` tags, none render-blocking, and 194 KB of gzip-compressed HTML.
- **Why it matters:** Google uses mobile speed in ranking, and slow pages lose visitors before they load.
- **Fix:** Run https://pagespeed.web.dev/ on the homepage, or get a free key (Google Cloud → PageSpeed Insights API → API key), set it as `PAGESPEED_API_KEY` and re-run this audit. If TBT is above 200 ms, cut or defer unused and third-party scripts.

### 2. Content Security Policy · Minor, fail
- **What we saw:** No `Content-Security-Policy` in the response headers (we checked the full list of header names) and no CSP `<meta http-equiv>` in the HTML. HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy and Permissions-Policy are all present.
- **Why it matters:** A CSP makes injected malicious scripts much harder to run.
- **Fix:** Add it as a Cloudflare Transform Rule (response header). Start with `Content-Security-Policy-Report-Only`, check what it reports, then enforce it.

### Notes (not scored)
- **Response time varies.** This run measured 268 ms TTFB (pass), with 115–127 ms on repeat checks. An earlier run today measured 2,418 ms on the first, uncached request. The headers show GitHub Pages (Fastly) behind Cloudflare with `cf-cache-status: DYNAMIC`, so Cloudflare does not cache the HTML. A Cloudflare cache rule for HTML would smooth out cold requests.
- **Review in the Organization schema:** The `review` attached to your own Organization is self-serving, so Google won't show review stars for it. It is harmless, but expect no rich result from it.
- **Local search is optional:** The site is scored as online-only. If you want to appear for searches like "İzmir web tasarım", add a city or address and a Google Business Profile link.

## What is already good
- Server-rendered text: 1,479 words, one H1, 11 H2s, 21 H3s, question headings and a FAQ section.
- robots.txt is open to every search and AI bot and points to the sitemap. The sitemap returns valid XML with 77 URLs.
- llms.txt: 200, `text/plain`, 13.9 KB, a clear description of the studio and both languages, and 5/5 checked links return 200.
- Six valid JSON-LD blocks: Organization (logo, sameAs to LinkedIn, GitHub and Instagram, contact point, priced offers), WebSite, Service, two MobileApplication blocks and FAQPage.
- The brand name "WoodstoneStudio" is identical in the title, `og:site_name`, the JSON-LD `name` and the llms.txt heading.
- Title is 61 characters and the description 157. The canonical points to the page itself, the page is indexable, a missing page returns a real 404, and www and http both 301-redirect to https://woodstonestudio.com/.
- tr/en hreflang links point at each other (checked on both pages), plus x-default.
- Contact options: a form, a tel: link, WhatsApp, mailto and "Teklif Al" / "Bize Ulaşın" calls to action.
- All 13 images have alt text and use WebP/AVIF; 11 load lazily. The HTML is gzip-compressed.
- Open Graph (including og:locale and image dimensions) and Twitter card tags are complete, and the og:image returns 200.
- The footer shows © 2026. The collector did not pick this up because the year sits in the page's script data, so we confirmed it with curl.

## Limits of this audit
Homepage only; one point in time. Live bot tests are hints: they used spoofed user agents from one IP, and firewalls may refuse those on purpose. The score excludes mobile speed because PageSpeed (a lab test on a simulated slow phone) could not be run. TTFB varied between runs (see notes).

<details><summary>Score arithmetic</summary>

Signal values: pass 1 · partial 0.5 · fail 0; `na` and `unknown` excluded. Per-signal statuses and evidence are in `signals.json`.

| Area (weight) | Σ(value × w) / Σw over measured signals | Score |
|---|---|---|
| AI access (14) | 25 / 25 | 100 |
| Technical SEO (14) | 31 / 31 (applinks na) | 100 |
| Speed (14) | ttfb 2 + size 1 + compress 2 + images 1 + lazy 1 + blocking 1 + oldtech 1 = 9 / 9 (perf, lcp, cls, tbt unknown) | 100 |
| Brand and entity (12) | 13 / 13 (address na) | 100 |
| Content and answers (12) | 16 / 16 | 100 |
| Structured data (10) | 8 / 8 (local na) | 100 |
| Security (8) | 16 / 17 (csp fail) | 94 |
| Contact and conversion (7) | 11 / 11 (map na) | 100 |
| Sharing (5) | 10 / 10 | 100 |
| Language (4) | 6 / 6 | 100 |

Total = (100×14 + 100×14 + 100×14 + 100×12 + 100×12 + 100×10 + 94×8 + 100×7 + 100×5 + 100×4) / 100 = 9952 / 100 = 99.52 → **99** (rounded down)

Gates K1–K5 and G1 are not triggered: 200 OK, indexable, bots allowed, 1,479 words, HTTPS, robots.txt 200.
Coverage: measured weight 146 / applicable weight 159 = 92 %.
Band: ≥ 92 → Excellent.
</details>
