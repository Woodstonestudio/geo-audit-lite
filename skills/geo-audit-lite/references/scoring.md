# Scoring

## Signal values
pass = 1 · partial = 0.5 · fail = 0 · `na` and `unknown` are left out (not counted as fail).

## Area score (0–100)
area = floor( Σ(value × weight) / Σ(weight) × 100 ) (round down) over the **measured** signals of that area.
An area with no measured signal has no score and is left out of the total.

## Area weights (sum 100)
| Area | Weight |
|---|---|
| AI access | 14 |
| Technical SEO | 14 |
| Speed | 14 |
| Brand and entity | 12 |
| Content and answers | 12 |
| Structured data | 10 |
| Security | 8 |
| Contact and conversion | 7 |
| Sharing | 5 |
| Language | 4 |

## Total
total = floor( Σ(area score × area weight) / Σ(area weight) ) over measured areas — always round **down**, so a site with any `fail` or `partial` never shows 100 (99.52 → 99).

## Gates (caps applied after the total)
| Gate | Condition | Max total |
|---|---|---|
| K1 | Homepage returns an error (no 2xx) | 20 |
| K2 | Homepage has noindex (meta or X-Robots-Tag) | 30 |
| K3 | All search bots blocked in robots.txt (also caps the AI area at 20) | 49 |
| K4 | Server HTML has almost no text (< 50 words; also caps the Content area at 30) | 59 |
| K5 | Site does not load over HTTPS | 49 |
| G1 | robots.txt returns a 5xx server error | 70 |

## Bands
< 35 Critical · < 60 Weak · < 80 Needs work · < 92 Good · ≥ 92 Excellent
Turkish labels (use exactly these): < 35 Kritik · < 60 Zayıf · < 80 Gelişmeli · < 92 İyi · ≥ 92 Çok iyi

## Coverage
coverage = measured weight ÷ applicable weight. If coverage < 70 %, print it next to the score: "Score based on 64 % of the signals (PageSpeed could not be measured)".
