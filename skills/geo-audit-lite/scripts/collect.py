#!/usr/bin/env python3
"""
WoodstoneStudio GEO Agent Team — evidence collector.

Collects raw, verifiable evidence about ONE website's homepage so the auditor
can score the 78 signals without guessing. Python 3.8+ standard library only.

Usage:
    python3 collect.py https://example.com [--psi] [--out evidence.json]

--psi   also query Google PageSpeed Insights (mobile). Optional env PAGESPEED_API_KEY.
        Without a key Google rate-limits; if it fails, speed signals are "unknown".

The output is facts only (status codes, headers, extracted tags, counts).
It never decides pass/fail; that is the auditor's job, using references/signals.*.md.
"""
import argparse
import gzip
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib
from html.parser import HTMLParser

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
BOT_UAS = {
    "Googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Bingbot": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "OAI-SearchBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot",
    "ChatGPT-User": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot",
    "Claude-SearchBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Claude-SearchBot/1.0; +https://www.anthropic.com)",
    "PerplexityBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)",
}
AI_SEARCH_BOTS = ["OAI-SearchBot", "ChatGPT-User", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User"]
AI_TRAINING_BOTS = ["GPTBot", "ClaudeBot", "Google-Extended", "CCBot", "Applebot-Extended", "meta-externalagent", "__usage_ai-training"]
SEARCH_BOTS = ["Googlebot", "Bingbot"]
TIMEOUT = 15
MAX_BYTES = 3_000_000


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def fetch(url, ua=BROWSER_UA, method="GET", follow=True, max_bytes=MAX_BYTES):
    """Returns dict(status, url, headers, body(str), bytes, ttfb_ms, total_ms, error)."""
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "tr,en;q=0.8",
    })
    handlers = [urllib.request.HTTPSHandler(context=ssl.create_default_context())]
    if not follow:
        handlers.append(NoRedirect())
    opener = urllib.request.build_opener(*handlers)
    t0 = time.time()
    try:
        resp = opener.open(req, timeout=TIMEOUT)
        status, final, hdrs = resp.status, resp.geturl(), resp
    except urllib.error.HTTPError as e:
        status, final, hdrs, resp = e.code, url, e, e
    except Exception as e:  # DNS, TLS, timeout
        return {"status": None, "url": url, "headers": {}, "body": "", "bytes": 0,
                "ttfb_ms": None, "total_ms": int((time.time() - t0) * 1000), "error": f"{type(e).__name__}: {e}"}
    ttfb = int((time.time() - t0) * 1000)
    raw = b""
    try:
        raw = resp.read(max_bytes) if method != "HEAD" else b""
    except Exception:
        pass
    headers = {k.lower(): v for k, v in hdrs.headers.items()} if hasattr(hdrs, "headers") else {}
    enc = headers.get("content-encoding", "")
    try:
        if "gzip" in enc:
            raw = gzip.decompress(raw)
        elif "deflate" in enc:
            raw = zlib.decompress(raw)
    except Exception:
        pass
    charset = "utf-8"
    m = re.search(r"charset=([\w-]+)", headers.get("content-type", ""), re.I)
    if m:
        charset = m.group(1)
    try:
        body = raw.decode(charset, errors="replace")
    except LookupError:
        body = raw.decode("utf-8", errors="replace")
    return {"status": status, "url": final, "headers": headers, "body": body, "bytes": len(raw),
            "ttfb_ms": ttfb, "total_ms": int((time.time() - t0) * 1000), "error": None}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta, self.links, self.a, self.imgs, self.scripts = [], [], [], [], []
        self.h = {"h1": [], "h2": [], "h3": []}
        self.title, self.lang, self.forms, self.iframes = "", None, 0, []
        self.jsonld, self._buf, self._in, self._skip = [], [], None, 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "meta":
            self.meta.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag == "a":
            self.a.append(a.get("href", ""))
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "form":
            self.forms += 1
        elif tag == "iframe":
            self.iframes.append(a.get("src", ""))
        elif tag == "script":
            self.scripts.append(a)
            if "ld+json" in a.get("type", "").lower():
                self._in, self._buf = "jsonld", []
            else:
                self._skip += 1
        elif tag == "style":
            self._skip += 1
        elif tag in ("title", "h1", "h2", "h3"):
            self._in, self._buf = tag, []

    def handle_endtag(self, tag):
        if tag == "script":
            if self._in == "jsonld":
                self.jsonld.append("".join(self._buf))
                self._in = None
            elif self._skip:
                self._skip -= 1
        elif tag == "style" and self._skip:
            self._skip -= 1
        elif tag == self._in:
            txt = re.sub(r"\s+", " ", "".join(self._buf)).strip()
            if tag == "title":
                self.title = txt
            else:
                self.h[tag].append(txt)
            self._in = None

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)
        if not self._skip and self._in != "jsonld":
            self.text.append(data)


def parse_robots(txt):
    """Returns {agent_lower: [(directive, path), ...]} using standard group semantics."""
    groups, cur, last_was_agent = {}, [], False
    for line in txt.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        k, v = [x.strip() for x in line.split(":", 1)]
        k = k.lower()
        if k == "user-agent":
            if not last_was_agent:
                cur = []
            cur.append(v.lower())
            groups.setdefault(v.lower(), [])
            last_was_agent = True
        else:
            last_was_agent = False
            if k in ("allow", "disallow"):
                for ag in cur:
                    groups.setdefault(ag, []).append((k, v))
    return groups


def robots_verdict(groups, agent, path="/"):
    """Is `path` allowed for `agent`? Longest-match rule, Allow wins ties. Falls back to '*'."""
    rules = groups.get(agent.lower())
    used = agent
    if rules is None:
        rules, used = groups.get("*", []), "*"
    best = None
    for d, p in rules:
        if p == "":
            continue
        pat = re.escape(p).replace(r"\*", ".*")
        if pat.endswith(r"\$"):
            pat = pat[:-2] + "$"
        if re.match(pat, path):
            if best is None or len(p) > len(best[1]) or (len(p) == len(best[1]) and d == "allow"):
                best = (d, p)
    return {"allowed": best is None or best[0] == "allow", "group": used, "rule": best}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--psi", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args()

    url = args.url.strip()
    if not re.match(r"^https?://", url, re.I):
        url = "https://" + url
    u = urllib.parse.urlparse(url)
    if u.scheme not in ("http", "https") or not u.hostname:
        sys.exit("Only http(s) URLs")
    origin = f"{u.scheme}://{u.netloc}"
    host = u.hostname
    ev = {"input": args.url, "collected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "notes": []}

    home = fetch(url)
    ev["home"] = {k: home[k] for k in ("status", "url", "bytes", "ttfb_ms", "total_ms", "error")}
    ev["home"]["headers"] = {k: v for k, v in home["headers"].items() if k in (
        "content-type", "content-encoding", "strict-transport-security", "x-content-type-options",
        "x-frame-options", "content-security-policy", "referrer-policy", "server", "x-powered-by",
        "x-robots-tag", "cache-control", "cf-ray", "x-vercel-id")}
    ev["home"]["header_keys"] = sorted(home["headers"].keys())
    if home["status"] is None:
        ev["notes"].append("Homepage could not be fetched at all: gate K1 applies.")
    html = home["body"]
    bot_wall = bool(re.search(r"just a moment|cf-challenge|attention required|captcha|access denied|are you a robot", html[:20000], re.I))
    ev["home"]["bot_protection_page"] = bot_wall and (home["status"] in (403, 429, 503) or len(html) < 20000)

    p = Page()
    try:
        p.feed(html)
    except Exception as e:
        ev["notes"].append(f"HTML parse warning: {e}")
    meta = lambda name: next((m.get("content", "") for m in p.meta if m.get("name", "").lower() == name or m.get("property", "").lower() == name), None)
    text = re.sub(r"\s+", " ", " ".join(p.text)).strip()
    words = len(re.findall(r"\w{2,}", text))
    canon = next((l.get("href") for l in p.links if "canonical" in l.get("rel", "").lower()), None)
    hreflang = [{"lang": l.get("hreflang"), "href": l.get("href")} for l in p.links if l.get("hreflang")]
    icons = [l.get("href") for l in p.links if "icon" in l.get("rel", "").lower()]
    jsonld, jsonld_errors, types = [], 0, []

    def walk(o):
        if isinstance(o, dict):
            t = o.get("@type")
            if t:
                types.extend(t if isinstance(t, list) else [t])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    for block in p.jsonld:
        try:
            obj = json.loads(block)
            jsonld.append(obj)
            walk(obj)
        except Exception:
            jsonld_errors += 1
    imgs = p.imgs
    img_src = [i.get("src", "") + " " + i.get("srcset", "") for i in imgs]
    hrefs = [h for h in p.a if h]
    internal = [h for h in hrefs if h.startswith("/") or host in h]
    years = [int(y) for y in re.findall(r"(?:©|&copy;|copyright)\s*(?:\d{4}\s*[-–]\s*)?(20\d\d)", html, re.I)]
    blocking = [s for s in p.scripts if s.get("src") and "async" not in s and "defer" not in s and s.get("type", "") != "module"]
    ev["page"] = {
        "title": p.title, "title_len": len(p.title),
        "description": meta("description"), "description_len": len(meta("description") or ""),
        "robots_meta": meta("robots"), "viewport": meta("viewport"), "generator": meta("generator"),
        "charset_meta": bool(re.search(r"<meta[^>]+charset", html[:5000], re.I)),
        "lang": p.lang, "hreflang": hreflang,
        "canonical": canon, "favicon": icons,
        "h1": p.h["h1"], "h2": p.h["h2"][:30], "h3_count": len(p.h["h3"]),
        "question_headings": [h for h in p.h["h2"] + p.h["h3"] if h.endswith("?")][:20],
        "word_count": words, "text_sample": text[:600],
        "images": len(imgs), "images_without_alt": sum(1 for i in imgs if "alt" not in i),
        "images_modern_format": sum(1 for s in img_src if re.search(r"\.(webp|avif)\b", s, re.I)),
        "images_lazy": sum(1 for i in imgs if i.get("loading", "").lower() == "lazy"),
        "links_total": len(hrefs), "links_internal": len(internal),
        "tel_links": [h for h in hrefs if h.lower().startswith("tel:")][:5],
        "mailto_links": [h for h in hrefs if h.lower().startswith("mailto:")][:5],
        "whatsapp_links": [h for h in hrefs if re.search(r"wa\.me|whatsapp\.com|api\.whatsapp", h, re.I)][:5],
        "map_links": [h for h in hrefs + p.iframes if re.search(r"google\.[a-z.]+/maps|maps\.app\.goo\.gl|goo\.gl/maps|maps\.google", h, re.I)][:5],
        "social_links": sorted({re.sub(r"^https?://(www\.)?", "", h).split("/")[0] for h in hrefs if re.search(r"instagram\.com|facebook\.com|linkedin\.com|x\.com|twitter\.com|youtube\.com|tiktok\.com", h, re.I)}),
        "about_links": [h for h in hrefs if re.search(r"about|hakkimizda|hakk%C4%B1m%C4%B1zda|hakkımızda|kurumsal", h, re.I)][:5],
        "forms": p.forms,
        "jsonld_blocks": len(p.jsonld), "jsonld_invalid": jsonld_errors, "jsonld_types": sorted(set(map(str, types))),
        "jsonld": jsonld[:6],
        "og": {k: meta(k) for k in ("og:title", "og:description", "og:image", "og:type", "og:url", "og:site_name", "og:locale")},
        "meta_keys": sorted({(m.get("property") or m.get("name") or "").lower() for m in p.meta if (m.get("property") or m.get("name"))}),
        "twitter_card": meta("twitter:card"),
        "scripts_total": len(p.scripts), "scripts_render_blocking": len(blocking),
        "old_tech": [t for t, rx in (("jQuery 1.x", r"jquery[-.]1\.\d"), ("Bootstrap 3", r"bootstrap/3\.|bootstrap-3"), ("Flash", r"\.swf\b|shockwave"), ("frameset", r"<frameset")) if re.search(rx, html, re.I)],
        "copyright_latest_year": max(years) if years else None,
        "mixed_content": sorted(set(re.findall(r'(?:src|href)=["\'](http://[^"\']+\.(?:js|css|png|jpe?g|gif|webp|svg))', html, re.I)))[:10] if home["url"].startswith("https") else [],
    }

    # robots.txt
    rb = fetch(origin + "/robots.txt")
    groups = parse_robots(rb["body"]) if rb["status"] == 200 else {}
    ev["robots"] = {
        "status": rb["status"], "error": rb["error"], "size": rb["bytes"],
        "sitemaps": re.findall(r"(?im)^\s*sitemap:\s*(\S+)", rb["body"]) if rb["status"] == 200 else [],
        "groups": sorted(groups.keys()),
        "verdicts": {b: robots_verdict(groups, b) for b in SEARCH_BOTS + AI_SEARCH_BOTS + AI_TRAINING_BOTS} if groups else {},
        "raw_head": rb["body"][:3000] if rb["status"] == 200 else "",
    }

    # sitemap
    sm_url = (ev["robots"]["sitemaps"] or [origin + "/sitemap.xml"])[0]
    sm = fetch(sm_url, max_bytes=500_000)
    ev["sitemap"] = {"url": sm_url, "status": sm["status"], "is_xml": "<urlset" in sm["body"] or "<sitemapindex" in sm["body"], "url_count": sm["body"].count("<loc>")}

    # llms.txt
    ll = fetch(origin + "/llms.txt", max_bytes=200_000)
    llms_links = re.findall(r"\((https?://[^)\s]+)\)", ll["body"])[:8] if ll["status"] == 200 else []
    ev["llms"] = {"status": ll["status"], "looks_like_html": "<html" in ll["body"][:500].lower(), "size": ll["bytes"],
                  "links_checked": [{"url": x, "status": fetch(x, method="HEAD")["status"]} for x in llms_links[:5]]}

    # soft 404
    nf = fetch(origin + "/bu-sayfa-yok-" + str(int(time.time())))
    ev["not_found_test"] = {"status": nf["status"]}

    # http -> https and www variants
    if u.scheme == "https":
        r = fetch("http://" + u.netloc + "/", follow=False)
        ev["http_redirect"] = {"status": r["status"], "location": r["headers"].get("location")}
    alt = host[4:] if host.startswith("www.") else "www." + host
    r = fetch(f"{u.scheme}://{alt}/", follow=False)
    ev["www_variant"] = {"host": alt, "status": r["status"], "location": r["headers"].get("location"), "error": r["error"]}

    # live bot tests (a hint only: WAFs may reject spoofed user agents on purpose)
    base_words = words
    ev["bot_tests"] = {}
    for name, ua in BOT_UAS.items():
        b = fetch(url, ua=ua)
        bp = Page()
        try:
            bp.feed(b["body"])
        except Exception:
            pass
        bw = len(re.findall(r"\w{2,}", " ".join(bp.text)))
        ev["bot_tests"][name] = {"status": b["status"], "words": bw, "error": b["error"],
                                 "same_content": base_words > 0 and abs(bw - base_words) / base_words < 0.3}
    ev["notes"].append("Bot tests use spoofed user agents from one IP. A firewall may refuse them on purpose; treat a refusal as a hint and say so.")

    # og:image reachable
    ogi = ev["page"]["og"].get("og:image")
    if ogi:
        ev["og_image_status"] = fetch(urllib.parse.urljoin(home["url"], ogi), method="HEAD")["status"]

    # PageSpeed (optional)
    if args.psi:
        import os
        q = {"url": home["url"] or url, "strategy": "mobile", "category": "performance"}
        if os.environ.get("PAGESPEED_API_KEY"):
            q["key"] = os.environ["PAGESPEED_API_KEY"]
        ps = fetch("https://www.googleapis.com/pagespeedonline/v5/runPagespeed?" + urllib.parse.urlencode(q), ua="geo-audit")
        try:
            lh = json.loads(ps["body"])["lighthouseResult"]
            au = lh["audits"]
            ev["pagespeed"] = {
                "score": round(lh["categories"]["performance"]["score"] * 100),
                "lcp_s": round(au["largest-contentful-paint"]["numericValue"] / 1000, 1),
                "cls": round(au["cumulative-layout-shift"]["numericValue"], 3),
                "tbt_ms": round(au["total-blocking-time"]["numericValue"]),
            }
        except Exception:
            ev["pagespeed"] = {"error": f"PageSpeed failed (status {ps['status']}). Speed signals = unknown."}

    out = json.dumps(ev, ensure_ascii=False, indent=2)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(out)
        print(f"evidence written to {args.out}")
    else:
        print(out)


if __name__ == "__main__":
    main()
