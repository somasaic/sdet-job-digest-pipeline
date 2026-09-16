# Step 2 — Dedup

**Goal:** never show myself the same posting twice, across sources, across days, indefinitely.

## How it works

Every candidate — including title-only postings where the full JD text couldn't be read — gets fingerprinted before anything else happens:

1. Build a string: `company | role | first ~120 characters of the JD text (or the title, if no text was readable)`, lowercased.
2. Strip everything except letters, digits, spaces, and the `|` separator.
3. Hash it (SHA-1) and take the first 16 hex characters as the fingerprint.
4. Check that fingerprint against a persistent ledger of every posting ever seen.
5. If it's already there: don't show it again. Update its `last_seen` date and count it as a blocked duplicate for the day.
6. If it's new: proceed to scoring.

See [`snippets/fingerprint.py`](../snippets/fingerprint.py) for the actual function.

## The rule I added for staffing agencies

Some staffing/consulting companies post the same role 3 or more times a day, each listing worded just differently enough to generate a different fingerprint — different client-facing title, slightly reworded JD snippet, same actual job. Individually fingerprinting each one meant they'd all pass the dedup check as "new," flooding the list with what was functionally one posting repeated five times.

The fix: group by company first. If one company has 3+ distinct new postings on the same day, they collapse into a single entry with a flag — "N postings today, confirm the real end client and role before investing time" — rather than being listed and scored individually. This is a company-level signal (high-volume reposting correlates with staffing/consulting shops), not a judgment on any specific role.

## Result, 15 days

- **Zero postings shown twice**, across 430 unique entries in the ledger, over 15 active days — structurally guaranteed by the fingerprint check, not just a claim.
- Multiple staffing-agency clusters caught and collapsed into single entries instead of cluttering the list.
