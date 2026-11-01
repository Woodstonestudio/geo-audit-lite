# 24 key signals (free edition)

The full edition has all 78 signals, fix templates, prospecting and the independent reviewer: woodstonestudio.com


## AI access (area weight 14)

### `ai.robots_search` · 5 (Critical)
**robots.txt lets Google and Bing read the homepage**  
Why: If Google and Bing can't read the site you won't show up in search; ChatGPT and Copilot rely heavily on Bing for web search.  
Fix: Remove the 'Disallow: /' line for Googlebot / Bingbot / * in robots.txt.

### `ai.robots_ai` · 3 (Important)
**robots.txt allows AI search bots**  
Why: ChatGPT, Claude and Perplexity read source pages with their own search bots; if they're blocked your name won't appear in answers.  
Fix: Don't block OAI-SearchBot, ChatGPT-User, Claude-SearchBot or PerplexityBot. To opt out of training only, blocking GPTBot, ClaudeBot and Google-Extended is enough.

### `ai.live_ai` · 3 (Important)
**AI search bots can actually reach the homepage**  
Why: Even if robots.txt allows them, a CDN or firewall (e.g. Cloudflare) may return errors or a challenge page to these bots.  
Fix: Check bot settings in your CDN/firewall. On Cloudflare's AI Crawl Control choose 'Disallow AI training' instead of 'Block' and keep search bots allowed.

### `ai.parity` · 3 (Important)
**Bots get the same content as browsers**  
Why: If bots receive an empty or different page, AI and search engines describe you incompletely; in some cases it counts as cloaking.  
Fix: Serve the full page to bot requests too; turn off bot-specific variants in cache/plugin settings.

### `ai.ssr` · 5 (Critical)
**Page text arrives from the server (no JavaScript needed)**  
Why: Most AI bots don't run JavaScript; if text only appears in the browser, the page is empty to them.  
Fix: Use server-side rendering (SSR) or static output; at minimum ship the title, description and main text in the HTML.

## Brand and entity (area weight 12)

### `brand.org` · 3 (Important)
**Organization / business structured data exists**  
Why: This data gives AI and Google an exact answer to 'whose site is this, what do they do, where'; knowledge panels and AI answers use it.  
Fix: Add Organization or a LocalBusiness schema that fits your business: name, logo, address, phone, social profiles.

### `brand.contact` · 3 (Important)
**Phone or email visible on the page**  
Why: Both visitors and AI look for 'how do I reach them' on the page.  
Fix: Write the phone and email as plain text in the header or footer.

## Content and answers (area weight 12)

### `content.h1` · 3 (Important)
**The page has a single H1**  
Why: The H1 states the page's main topic; missing or multiple H1s blur it.  
Fix: Use one H1 that says what you do; make other headings H2/H3.

### `content.words` · 3 (Important)
**The homepage has enough text**  
Why: A page with little text is 'unclear what they do' to Google and AI; there's nothing to rank or quote.  
Fix: At least 300 words on the homepage: what you do, for whom, where, why you, FAQ.

## Technical SEO (area weight 14)

### `tech.status` · 5 (Critical)
**The homepage loads successfully (2xx)**  
Why: If the homepage errors, neither visitors nor search engines can see your site.  
Fix: Check hosting and DNS settings; pause ads until the site works.

### `tech.indexable` · 5 (Critical)
**The homepage can appear in search (no noindex)**  
Why: A noindex tag tells Google and Bing not to show the page; it's often a setting forgotten at launch.  
Fix: Remove the <meta name="robots" content="noindex"> tag or the X-Robots-Tag header (WordPress: Settings → Reading → 'Discourage search engines' must be off).

### `tech.title` · 3 (Important)
**Page title exists with a good length**  
Why: The title is the blue line people click in results; too short or long and it gets cut or rewritten by Google.  
Fix: Write a 10–60 character title with what you do and your brand (e.g. 'Downtown Hair Salon | Brand').

### `tech.description` · 3 (Important)
**Meta description exists with a good length**  
Why: It's the two lines under the title in search results and affects click decisions.  
Fix: Write a 50–160 character description of your service and location.

### `tech.viewport` · 3 (Important)
**Mobile viewport setting exists**  
Why: Without it, phones show a shrunken desktop page; Google ranks the mobile version.  
Fix: Add <meta name="viewport" content="width=device-width, initial-scale=1"> and check the design on mobile.

## Speed (area weight 14)

### `speed.perf` · 5 (Critical)
**Mobile PageSpeed score 90+**  
Why: Half of mobile visitors leave slow pages without waiting; Google uses speed in ranking.  
Fix: Convert and resize images to WebP, remove unused plugins and scripts, use caching and a CDN.

### `speed.lcp` · 3 (Important)
**Main content appears within 2.5 s (LCP)**  
Why: LCP is when the largest element (usually the hero image) appears; it's a core Google experience metric.  
Fix: Shrink the hero image and load it with priority (fetchpriority=high), lighten web fonts.

### `speed.cls` · 3 (Important)
**The page doesn't shift while loading (CLS)**  
Why: Buttons that move while loading cause mis-clicks and frustration; Google measures it.  
Fix: Give images width/height and reserve space for ads and embeds.

## Structured data (area weight 10)

### `schema.present` · 3 (Important)
**Structured data (JSON-LD) exists**  
Why: Structured data gives page facts (business, services, FAQ, prices) in a format machines read without errors.  
Fix: Add a schema.org JSON-LD block and validate it with Google's Rich Results Test.

### `schema.valid` · 3 (Important)
**All JSON-LD blocks are valid**  
Why: A single comma error causes the whole block to be ignored.  
Fix: Validate blocks in the Rich Results Test; generate hand-written ones with a plugin.

## Security (area weight 8)

### `sec.https` · 5 (Critical)
**The site loads over HTTPS**  
Why: Without HTTPS browsers show 'Not secure'; visitors won't fill forms and Google ranks it lower.  
Fix: Install free SSL (Let's Encrypt or Cloudflare).

### `sec.redirect` · 3 (Important)
**http:// permanently redirects to https**  
Why: Without a permanent (301/308) redirect, old links go to the insecure version and ranking strength isn't passed on.  
Fix: Redirect all http requests to https with a 301 on the server.

## Contact and conversion (area weight 7)

### `contact.form` · 3 (Important)
**Contact or booking form present**  
Why: Visitors want to reach out right away; most give up rather than copy an email address.  
Fix: Add a short form (name, phone, message) or online booking.

### `contact.tel` · 3 (Important)
**Tap-to-call link present (tel:)**  
Why: Mobile visitors tap to call instead of copying the number.  
Fix: Make the phone number a link with <a href="tel:+…">.

## Sharing (area weight 5)

### `social.image` · 3 (Important)
**Share image (og:image) present**  
Why: Shares without an image get far fewer clicks.  
Fix: Add a 1200×630 og:image.

