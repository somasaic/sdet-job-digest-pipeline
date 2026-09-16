# Rules changelog

Most of the rules in this system exist because something specific broke, slipped through, or got noticed in production — not because I anticipated them on day one. This is the actual history, in order.

## Initial build
- Multi-source search (Indeed, Wellfound, Cutshort, LinkedIn/Naukri, We Work Remotely)
- Fingerprint-based dedup against a persistent ledger
- Real / phrasing / stretch gap classification
- Fit % scoring with a 65%+ recommend bar

## +Instahyre as a source
Discovered its search/listing pages are JavaScript-rendered and unfetchable, but individual job detail pages return usable structured data even without the long-form description loading. Added as a source; excluded its listing pages specifically, not the site as a whole.

## +Hirist exclusion
Tested and found both the search page and individual job pages are JavaScript-rendered with no server-rendered content at all — a fetch returns only navigation shell. Excluded entirely as a direct-fetch source rather than continuing to burn calls on it.

## +3 additional search query variants
Found that exact-phrase title matching was missing real postings because recruiters title the same role inconsistently. Widened the query set to catch adjacent titles across the same location variants.

## +High-volume-poster grouping
Staffing/consulting companies were posting the same role 3+ times a day under slightly reworded titles, each generating a different fingerprint and passing dedup individually. Added a company-level check: 3+ new postings from one company in a day collapse into a single flagged entry instead of being listed separately.

## +Staleness check
A "remote" posting dated six months earlier was still surfacing in results as if actively live. Added a 21-day threshold — anything older gets tagged stale and dropped from the daily recommended count, shown but never presented as a fresh pick.

## +ATS score, verdict tiers, and tweak points (Step 4)
Realized Fit % alone didn't answer "does my resume actually need editing for this specific JD." Added a separate, stricter keyword-match score, verdict tiers based on it, and a concrete tweak-point list for anything below 70 — with a hard rule that any suggested keyword I can't genuinely back up gets an explicit caveat, never a bare suggestion.

## +Comp intelligence on top picks only
Added a targeted, cheap comp-data check (one search per company) — but only for the handful of true recommended picks, not backups or excluded postings, to keep it from becoming its own bottleneck.

## +Follow-up window reminders
Added a scan for previously-recommended postings sitting in the 5-10 day-since-first-seen window — the point where a follow-up nudge is actually useful, phrased conditionally since the system has no way to know whether I actually applied.

## +Contract vs. permanent as its own policy field
Employment type was getting buried inside general "logistics friction" notes. Split it out as its own explicit field, same tier as location or comp, so contract-only roles get tagged rather than silently counted alongside permanent ones.

## +"Best Bet" tag
After enough real data existed to see how Fit% and ATS% actually diverged in practice, added one small additive tag: postings where both scores are independently 75+ get flagged, without changing either underlying number or the existing verdict logic. A signal layered on top, not a replacement for the two-number system.

---

The pattern across all of these: almost none were designed in ahead of time. Each one exists because a specific failure mode showed up in real runs, got noticed, and got a rule written against it.
