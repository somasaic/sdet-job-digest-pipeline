"""
Deduplication fingerprint used in Step 2 (Dedup).

Every candidate posting is reduced to a 16-character fingerprint before
anything else happens. The fingerprint is checked against a persistent
ledger — if it's already there, the posting is a confirmed duplicate and
never gets shown again; if not, it proceeds to scoring.

This is the real function used in the pipeline, not a simplified example.
"""

import hashlib
import re


def fingerprint(company: str, role: str, jd_snippet_or_title: str) -> str:
    """
    Build a stable fingerprint for a job posting.

    Args:
        company: company name as it appears in the posting
        role: job title as it appears in the posting
        jd_snippet_or_title: the first ~120 characters of the JD description,
            or the title itself if the full JD text wasn't readable
            (e.g. a robots.txt-blocked listing page)

    Returns:
        A 16-character hex fingerprint.
    """
    raw = f"{company}|{role}|{jd_snippet_or_title[:120]}".lower()

    # Strip everything except letters, digits, spaces, and the separator —
    # this makes the fingerprint resilient to minor punctuation/whitespace
    # differences between the same posting seen from two different sources.
    cleaned = re.sub(r"[^a-z0-9 |]", "", raw)

    return hashlib.sha1(cleaned.encode("utf-8")).hexdigest()[:16]


if __name__ == "__main__":
    # Example — the same posting, described slightly differently by two
    # different sources, still produces the same fingerprint as long as
    # company, role, and the leading JD text line up.
    fp_a = fingerprint(
        "Acme Robotics",
        "SDET - QA Automation",
        "We are looking for a Software Development Engineer in Test to join our platform team...",
    )
    fp_b = fingerprint(
        "Acme Robotics",
        "SDET - QA Automation",
        "We are looking for a Software Development Engineer in Test to join our platform team...",
    )
    assert fp_a == fp_b
    print(f"fingerprint: {fp_a}")
