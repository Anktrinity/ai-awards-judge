from __future__ import annotations

import re
from collections import defaultdict

from ai_awards_judge.models import Entry, JudgedEntry, ScoreBreakdown


POSITIVE_INNOVATION = ["ai", "novel", "innovative", "distinct", "searchable", "cluster", "intelligence"]
POSITIVE_EXECUTION = ["deployed", "pilot", "workflow", "integration", "check-in", "production", "enterprise"]
RESULT_SIGNALS = ["reduced", "increase", "improved", "renewal", "%", "roi", "satisfaction", "adoption"]
RISK_TERMS = ["early-stage", "portfolio-level", "not feature-isolated", "pilot", "limited"]


def _count_keywords(text: str, keywords: list[str]) -> int:
    lowered = text.lower()
    return sum(1 for keyword in keywords if keyword in lowered)


def _count_metrics(text: str) -> int:
    return len(re.findall(r"\b\d+(?:\.\d+)?%?\b", text))


def score_entry(entry: Entry) -> JudgedEntry:
    joined = "\n".join([entry.summary, *entry.evidence, entry.notes, entry.raw_text])
    innovation = min(95, 60 + _count_keywords(joined, POSITIVE_INNOVATION) * 5 + min(_count_metrics(joined), 4))
    impact = min(95, 58 + _count_metrics(joined) * 4 + _count_keywords(joined, RESULT_SIGNALS) * 3)
    execution = min(95, 60 + _count_keywords(joined, POSITIVE_EXECUTION) * 5 + len(entry.evidence) * 2)
    results = min(95, 52 + _count_metrics(joined) * 5 + _count_keywords(joined, RESULT_SIGNALS) * 4)

    risk_hits = _count_keywords(joined, RISK_TERMS)
    if risk_hits:
        results = max(45, results - risk_hits * 4)
        impact = max(50, impact - max(0, risk_hits - 1) * 2)

    strengths: list[str] = []
    concerns: list[str] = []

    if _count_metrics(joined) >= 3:
        strengths.append("Includes multiple concrete metrics or evidence points.")
    if "pilot" in joined.lower() or "deployed" in joined.lower():
        strengths.append("Shows evidence of real-world rollout or testing.")
    if entry.category and entry.category.lower() in joined.lower():
        strengths.append("Strong category alignment in the submission framing.")

    if "early-stage" in joined.lower():
        concerns.append("Entry appears early-stage, so long-term proof is still limited.")
    if "portfolio-level" in joined.lower() or "not feature-isolated" in joined.lower():
        concerns.append("Some evidence may be broader than the single feature being judged.")
    if len(entry.evidence) < 2:
        concerns.append("Thin evidence set, which lowers confidence.")

    total = innovation + impact + execution + results
    if total >= 340:
        verdict = "Strong finalist"
    elif total >= 300:
        verdict = "Competitive shortlist contender"
    elif total >= 260:
        verdict = "Promising, but under the leaders"
    else:
        verdict = "Needs stronger evidence or positioning"

    confidence = "high" if len(entry.evidence) >= 3 and _count_metrics(joined) >= 3 else "medium"
    if len(entry.evidence) < 2:
        confidence = "low"

    return JudgedEntry(
        entry=entry,
        scores=ScoreBreakdown(
            innovation=innovation,
            impact=impact,
            execution=execution,
            results=results,
        ),
        strengths=strengths or ["Relevant use case with some judging potential."],
        concerns=concerns or ["No major concern captured from the current heuristic pass."],
        verdict=verdict,
        confidence=confidence,
    )


def rank_by_category(entries: list[JudgedEntry]) -> dict[str, list[JudgedEntry]]:
    grouped: dict[str, list[JudgedEntry]] = defaultdict(list)
    for entry in entries:
        grouped[entry.entry.category].append(entry)
    for category, items in grouped.items():
        grouped[category] = sorted(items, key=lambda item: item.scores.total, reverse=True)
    return dict(grouped)
