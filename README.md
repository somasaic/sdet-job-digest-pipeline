# SDET Job Digest — an AI-agent-orchestrated job search pipeline

I'm an SDET (3.6+ years, Playwright/TypeScript, AI-assisted QA). My job search kept costing me the same manual review every morning — open a job board, skim a JD, guess at fit, half-remember if I'd seen it before. That's exactly the kind of repetitive, rule-based process I spend my day job eliminating, so I pointed the same instinct at my own search.

This repo documents the system: what it does, the rules behind each step, and the real numbers from running it for 15 days straight.

![Pipeline overview](assets/pipeline-infographic.png)

## What this is — and isn't

**This is an AI-agent-orchestrated pipeline, not a hand-coded framework.** I designed every rule below — what counts as a duplicate, what counts as a real skill gap versus just phrasing, how to weigh fit against ATS match, when a posting is stale. An AI agent (running on a daily schedule) implements those rules, executes the pipeline, and maintains a persistent data store between runs. I review the rules and the output; I did not hand-write the orchestration code line by line.

I think that distinction is worth stating plainly rather than implying otherwise. Directing an agent to build and iteratively refine a working data pipeline is, to me, a more current and more relevant skill for the AI-assisted QA roles I'm targeting than solo-scripting the same thing would be — but only if I'm honest about which one it is.

**What it does automatically:** searches multiple job boards, deduplicates every posting against a persistent ledger, classifies requirement gaps, scores fit and ATS match, flags stale/contract/logistics issues, and reports a daily summary.

**What stays entirely manual, by design:** submitting any application, editing my resume, and suggesting any skill I can't genuinely back up in an interview. Automating the search isn't automating the judgment.

## What this actually fixes, and how it differs from typical "auto-apply" tools

Most AI job-search tools optimize for application *volume*. That's the root of almost every well-documented complaint about them, so it's worth being specific about what this system deliberately does not do.

**The known failure modes of auto-apply tools:**
- **Mass, undirected applications.** Tools that fire dozens of applications an hour with no human review routinely apply to roles wildly outside the candidate's actual fit — wrong seniority, wrong domain — because volume, not judgment, is the optimization target.
- **ATS flags and cross-company blacklisting.** Recruiters and ATS platforms actively detect bot-like patterns — many applications to one company in a short window, identical boilerplate phrasing reused across unrelated roles, application velocity no human could produce. Once a profile is flagged, that reputation can follow across every company using the same ATS vendor.
- **Content that falls apart under scrutiny.** Auto-generated cover letters and form answers frequently contradict the resume, misstate basic facts (wrong company name, wrong visa status), or use language so generic recruiters read it as automated on sight.
- **Undefendable claims in the interview.** If a tool tailors a resume by inserting keywords the candidate can't actually speak to, the mismatch surfaces the moment an interviewer asks a follow-up question — the worst possible time to discover it.
- **Platform bans.** LinkedIn and similar platforms increasingly detect automation by behavior, not just by tool signature — scraping, bulk actions, and background application-firing risk account restrictions or suspension. The one consistently safe pattern across every source I checked: automation that drafts or screens, with a human clicking send on every action, is treated as assistance; automation that acts *for* the human, unreviewed, is what gets flagged.

**Where this pipeline sits, deliberately, on the other side of every one of those:**

| Typical failure mode | How this system avoids it |
|---|---|
| Fires applications automatically | Never submits anything — every application is a manual click, after manual review |
| Generic, contradictory application content | Doesn't generate cover letters or fill forms at all — resume edits are suggested, never auto-applied |
| Keyword-stuffs resumes with unverifiable skills | Hard rule: any suggested keyword I don't genuinely have gets an explicit caveat, or the posting gets skipped instead |
| Blind keyword-match scoring (false positives/negatives) | Every gap explicitly classified as real / phrasing / stretch before anything is scored |
| Scrapes or bulk-acts on LinkedIn/Naukri, risking a ban | Never scrapes or logs in — only public search results and the alert emails already sitting in my own inbox |
| No memory between runs — same postings re-reviewed endlessly | Persistent fingerprint ledger — zero postings shown twice across 430 entries and 15 days |
| Treats every posting as equally "live" | Explicit staleness check after a 6-month-old ghost listing surfaced as if active |

## Risks, and how they're handled

Being honest about what this doesn't fully solve is part of the point of documenting it this way.

| Risk | How it's handled |
|---|---|
| The AI agent misclassifies a gap as "phrasing" when it's actually real (or vice versa) | Every classification and its reasoning is shown in the daily output, not hidden behind a single score — wrong calls are visible and correctable, not silently trusted |
| Temptation to let the system suggest resume keywords I can't back up, just to raise the ATS score | Treated as a hard rule, not a guideline: unverifiable keywords always carry an explicit caveat, and a posting gets skipped rather than the resume padded |
| Automation getting flagged or restricted on LinkedIn/Naukri | No scraping, no login automation, no bulk actions — sourcing is limited to public search and personal inbox alerts, the pattern every source above confirms as safe |
| Wasting time on dead or ghost listings | 21-day staleness threshold, added specifically after a 6-month-old listing was still surfacing as live |
| Same posting reviewed repeatedly across sources and days | Persistent fingerprint-based ledger, checked before anything else runs |
| Personal data (resume, comp figures, real company-by-company notes) leaking into a public repo | This repo ships placeholder data only — the fingerprint function and schema are real, the dashboard screenshot and examples throughout are fictional |
| The system silently going stale as job-market patterns shift | Rules get added in response to specific observed failures (see [docs/rules-changelog.md](docs/rules-changelog.md)), and the repo's `Status` section is kept honest about what's current |

## Where the time actually goes

Screening, not applying, is the expensive part of a job search — and it's also the part that's fully mechanical once the judgment rules are written down. Concretely, this system removes:

- **Manual searching** across 6+ separate sites every morning — down to one automated pass.
- **Re-reading postings I'd already seen** — down to zero, structurally, via the dedup ledger.
- **Guessing at fit from a skim** — replaced with an explicit, auditable real/phrasing/stretch judgment on every requirement.
- **Manually checking whether a posting is still active** — the staleness check does this before I ever open the listing.
- **Wondering whether my resume needs edits for a specific JD** — the tweak-point list answers that directly, with the honesty caveat built in.

What it doesn't remove, on purpose: deciding what to apply for, writing anything in my own words, and showing up to the interview. That split is the actual design goal, not a limitation.

## The numbers (15 days, real data)

| Metric | Value |
|---|---|
| Postings screened | 430 |
| Unique companies | 317 |
| Sources checked automatically | 6+ |
| Genuine matches surfaced | 63 (40 top picks + 23 backups) |
| Filtered out with a stated reason | 183 (43%) |
| Average fit / ATS score on surfaced matches | 76% / 72% |
| Stale postings caught (oldest: 6 months) | 15 |
| Estimated manual screening time reclaimed | ~25–30 hours |

*Sample dashboard view below uses anonymized placeholder data — the live system runs against my real, private job search and isn't published.*

![Sample dashboard view](assets/dashboard-sample.png)

## The pipeline — six steps, every morning at 8AM

| Step | What it does | Docs |
|---|---|---|
| 1. Search | Pulls fresh postings from 6+ sources | [docs/01-search.md](docs/01-search.md) |
| 2. Dedup | Fingerprints and checks every posting against a persistent ledger | [docs/02-dedup.md](docs/02-dedup.md) |
| 3. Classify | Sorts every requirement gap as real / phrasing / stretch | [docs/03-classify.md](docs/03-classify.md) |
| 4. Score | Two independent numbers — Fit % and ATS % — never merged | [docs/04-score.md](docs/04-score.md) |
| 5. Flag | Catches staleness, contract-only roles, and logistics friction | [docs/05-flag.md](docs/05-flag.md) |
| 6. Report | Publishes a dashboard and sends one push notification | [docs/06-report.md](docs/06-report.md) |

See [docs/rules-changelog.md](docs/rules-changelog.md) for how these rules actually evolved — most of them exist because something specific broke or slipped through in production, not because I anticipated it up front.

## Code in this repo

- [`snippets/fingerprint.py`](snippets/fingerprint.py) — the real deduplication fingerprint function.
- [`snippets/ledger_schema.json`](snippets/ledger_schema.json) — the real shape of a ledger document (values are placeholders).

## Status

This is a living personal tool, actively running daily. This repo is a point-in-time writeup of the rules and design as of September 2026 — I'll update `rules-changelog.md` as the system changes, rather than guaranteeing every future rule gets documented the same day it ships.

## About me

SDET / QA Automation Engineer, Playwright + TypeScript, actively building in AI-assisted QA (MCP, AI testing agents, LLM evaluation). Open to SDET / QA Automation Engineer roles — Bengaluru, Hyderabad, or remote.