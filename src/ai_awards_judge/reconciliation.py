from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from ai_awards_judge.models import JudgedEntry, ReconciledEntry, ScoreBreakdown


def load_judged_entries(path: Path) -> list[JudgedEntry]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [JudgedEntry.from_dict(item) for item in data]


def _top_list(items: list[str], fallback: str, limit: int = 5) -> list[str]:
    cleaned = [item.strip() for item in items if item and item.strip()]
    if not cleaned:
        return [fallback]
    counts = Counter(cleaned)
    return [item for item, _ in counts.most_common(limit)]


def _top_value(items: list[str], fallback: str) -> str:
    cleaned = [item.strip() for item in items if item and item.strip()]
    if not cleaned:
        return fallback
    return Counter(cleaned).most_common(1)[0][0]


def _disagreement_level(score_range: int) -> str:
    if score_range >= 40:
        return "high"
    if score_range >= 20:
        return "medium"
    return "low"


def reconcile_entries(judge_results: list[JudgedEntry]) -> list[ReconciledEntry]:
    grouped: dict[str, list[JudgedEntry]] = defaultdict(list)
    for item in judge_results:
        grouped[item.entry_key].append(item)

    reconciled: list[ReconciledEntry] = []
    for entry_key, items in grouped.items():
        anchor = items[0]
        innovation = round(sum(item.scores.innovation for item in items) / len(items))
        impact = round(sum(item.scores.impact for item in items) / len(items))
        execution = round(sum(item.scores.execution for item in items) / len(items))
        results = round(sum(item.scores.results for item in items) / len(items))
        totals = [item.scores.total for item in items]
        verdict_counts = dict(Counter(item.verdict for item in items))
        confidence_counts = dict(Counter(item.confidence for item in items))
        score_range = max(totals) - min(totals)
        reconciled.append(
            ReconciledEntry(
                entry_key=entry_key,
                category=anchor.entry.category,
                entrant=anchor.entry.entrant,
                company=anchor.entry.company,
                product=anchor.entry.product,
                judge_count=len(items),
                judge_ids=sorted({item.judge_id for item in items}),
                scores=ScoreBreakdown(
                    innovation=innovation,
                    impact=impact,
                    execution=execution,
                    results=results,
                ),
                verdict=_top_value([item.verdict for item in items], "Unspecified verdict"),
                confidence=_top_value([item.confidence for item in items], "medium"),
                summary=_top_value([item.concise_summary for item in items], anchor.entry.summary),
                evidence_cited=_top_list([e for item in items for e in item.evidence_cited], "No shared evidence cited."),
                strengths=_top_list([s for item in items for s in item.strengths], "No shared strengths captured."),
                concerns=_top_list([c for item in items for c in item.concerns], "No shared concerns captured."),
                score_range=score_range,
                disagreement_level=_disagreement_level(score_range),
                verdict_counts=verdict_counts,
                confidence_counts=confidence_counts,
            )
        )

    reconciled.sort(key=lambda item: (item.category, -item.scores.total, item.entrant))
    return reconciled


def reconcile_json_files(paths: list[Path]) -> list[ReconciledEntry]:
    loaded: list[JudgedEntry] = []
    for path in paths:
        loaded.extend(load_judged_entries(path))
    return reconcile_entries(loaded)
