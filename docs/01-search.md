# Step 1 — Search

**Goal:** find every genuinely relevant new posting, from as many sources as will actually return usable data, without wasting calls on sources that don't.

## Sources checked every run

- **Indeed** — the highest-yield source by a wide margin (~49% of everything screened). Full JD text and a "posted on" date are both readable, which feeds directly into the staleness check in Step 5.
- **LinkedIn + Naukri, via Gmail job-alert parsing** — LinkedIn and Naukri's own listing pages are robots.txt-blocked from direct fetching, so this source reads the alert emails they already send me instead, which aren't blocked. Second-highest yield.
- **Instahyre** — its search/listing pages are JavaScript-rendered and unfetchable, but individual job detail pages return usable structured data (company, role, location, experience band, skill tags) even when the long-form description doesn't load. Worth the extra step of discovering job URLs via search first, then fetching each one directly.
- **Cutshort, Wellfound** — listing pages plus individual job fetches, lower but consistent yield.
- **LinkedIn + Naukri, public search** — a secondary, lower-confidence path for postings the alert parsing misses. Titles and links are readable; full JD text usually isn't, so these get logged separately as "found, not yet scored" rather than fully evaluated.

## A source I deliberately excluded

One popular job board turned out to be entirely JavaScript-rendered on both the search page and individual job pages — a fetch returns only the site's navigation shell, never actual job content. Rather than keep burning calls hoping it'd work, I excluded it as a direct-fetch source entirely. If it turns up in a broader search, it gets logged in the "found but not yet scored, open manually" bucket instead.

## The rule I added after week one

The first version searched exact-phrase titles only — "SDET", "Automation Test Engineer", etc. Within a week it became clear recruiters title the identical role five different ways ("Quality Engineer," "Test Automation Engineer," bare "SDET" with no other qualifier), and exact-phrase matching was quietly missing real, relevant postings. I widened the query set to catch adjacent titles, run across the same location variants (Bengaluru, Hyderabad, remote) as the original queries.

## Result, 15 days

- 430 postings screened across 317 companies
- ~29 postings/day average
- 6+ sources cross-checked automatically, every single morning, with zero manual searching on my part
