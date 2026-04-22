from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from ai_awards_judge.models import JudgedEntry, ReconciledEntry


def write_json(entries: list[JudgedEntry], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [entry.to_dict() for entry in entries]
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_markdown(entries: list[JudgedEntry], category_rankings: dict[str, list[JudgedEntry]], path: Path) -> None:
    lines: list[str] = ["# AI Awards Judge Run", "", "## Category Rankings", ""]
    for category, ranked_entries in category_rankings.items():
        lines.append(f"### {category}")
        for index, judged in enumerate(ranked_entries, start=1):
            lines.append(
                f"{index}. **{judged.entry.entrant}** ({judged.entry.company}, {judged.entry.product}) - {judged.scores.total}/400, {judged.verdict}"
            )
        lines.append("")

    lines.extend(["## Entry Reviews", ""])
    for judged in entries:
        lines.extend(
            [
                f"### {judged.entry.entrant}",
                f"- Category: {judged.entry.category}",
                f"- Company: {judged.entry.company}",
                f"- Product: {judged.entry.product}",
                f"- Judge: {judged.judge_id}",
                f"- Scoring mode: {judged.scoring_mode}",
                f"- Summary: {judged.concise_summary or judged.entry.summary or 'No summary provided.'}",
                "- Evidence:",
            ]
        )
        if judged.evidence_cited:
            lines.extend([f"  - {item}" for item in judged.evidence_cited])
        elif judged.entry.evidence:
            lines.extend([f"  - {item}" for item in judged.entry.evidence])
        else:
            lines.append("  - No explicit evidence listed")
        lines.extend(
            [
                "- Strengths:",
                *[f"  - {item}" for item in judged.strengths],
                "- Concerns:",
                *[f"  - {item}" for item in judged.concerns],
                f"- Scores: Innovation {judged.scores.innovation}, Impact {judged.scores.impact}, Execution {judged.scores.execution}, Results {judged.scores.results}",
                f"- Total: {judged.scores.total}/400",
                f"- Verdict: {judged.verdict}",
                f"- Confidence: {judged.confidence}",
                "",
            ]
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(entries: list[JudgedEntry], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "entry_key",
        "judge_id",
        "scoring_mode",
        "category",
        "entrant",
        "company",
        "product",
        "innovation",
        "impact",
        "execution",
        "results",
        "total",
        "verdict",
        "confidence",
        "concise_summary",
        "evidence_cited",
        "strengths",
        "concerns",
        "source_path",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for judged in entries:
            writer.writerow(
                {
                    "entry_key": judged.entry_key,
                    "judge_id": judged.judge_id,
                    "scoring_mode": judged.scoring_mode,
                    "category": judged.entry.category,
                    "entrant": judged.entry.entrant,
                    "company": judged.entry.company,
                    "product": judged.entry.product,
                    "innovation": judged.scores.innovation,
                    "impact": judged.scores.impact,
                    "execution": judged.scores.execution,
                    "results": judged.scores.results,
                    "total": judged.scores.total,
                    "verdict": judged.verdict,
                    "confidence": judged.confidence,
                    "concise_summary": judged.concise_summary,
                    "evidence_cited": " | ".join(judged.evidence_cited),
                    "strengths": " | ".join(judged.strengths),
                    "concerns": " | ".join(judged.concerns),
                    "source_path": judged.entry.path,
                }
            )


def write_reconciliation_json(entries: list[ReconciledEntry], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([entry.to_dict() for entry in entries], indent=2), encoding="utf-8")


def write_reconciliation_csv(entries: list[ReconciledEntry], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "entry_key",
        "category",
        "entrant",
        "company",
        "product",
        "judge_count",
        "judge_ids",
        "innovation",
        "impact",
        "execution",
        "results",
        "total",
        "score_range",
        "disagreement_level",
        "verdict",
        "verdict_counts",
        "confidence",
        "confidence_counts",
        "summary",
        "evidence_cited",
        "strengths",
        "concerns",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in entries:
            writer.writerow(
                {
                    "entry_key": item.entry_key,
                    "category": item.category,
                    "entrant": item.entrant,
                    "company": item.company,
                    "product": item.product,
                    "judge_count": item.judge_count,
                    "judge_ids": " | ".join(item.judge_ids),
                    "innovation": item.scores.innovation,
                    "impact": item.scores.impact,
                    "execution": item.scores.execution,
                    "results": item.scores.results,
                    "total": item.scores.total,
                    "score_range": item.score_range,
                    "disagreement_level": item.disagreement_level,
                    "verdict": item.verdict,
                    "verdict_counts": json.dumps(item.verdict_counts, sort_keys=True),
                    "confidence": item.confidence,
                    "confidence_counts": json.dumps(item.confidence_counts, sort_keys=True),
                    "summary": item.summary,
                    "evidence_cited": " | ".join(item.evidence_cited),
                    "strengths": " | ".join(item.strengths),
                    "concerns": " | ".join(item.concerns),
                }
            )


def write_reconciliation_markdown(entries: list[ReconciledEntry], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = ["# AI Awards Judge Reconciliation Report", ""]

    high = [item for item in entries if item.disagreement_level == "high"]
    medium = [item for item in entries if item.disagreement_level == "medium"]
    low = [item for item in entries if item.disagreement_level == "low"]

    lines.extend(
        [
            "## Overview",
            f"- Reconciled entries: {len(entries)}",
            f"- High disagreement: {len(high)}",
            f"- Medium disagreement: {len(medium)}",
            f"- Low disagreement: {len(low)}",
            "",
        ]
    )

    if entries:
        lines.extend(["## Highest disagreement entries", ""])
        for item in sorted(entries, key=lambda row: row.score_range, reverse=True)[:5]:
            lines.append(
                f"- **{item.entrant}** ({item.category}) - total {item.scores.total}/400, range {item.score_range}, disagreement {item.disagreement_level}"
            )
        lines.append("")

    by_category: dict[str, list[ReconciledEntry]] = {}
    for item in entries:
        by_category.setdefault(item.category, []).append(item)

    lines.extend(["## Category consensus rankings", ""])
    for category, items in by_category.items():
        ranked = sorted(items, key=lambda row: row.scores.total, reverse=True)
        lines.append(f"### {category}")
        for index, item in enumerate(ranked, start=1):
            lines.append(
                f"{index}. **{item.entrant}** ({item.company}, {item.product}) - {item.scores.total}/400, {item.verdict}, disagreement {item.disagreement_level}"
            )
        lines.append("")

    lines.extend(["## Entry reconciliation details", ""])
    for item in entries:
        lines.extend(
            [
                f"### {item.entrant}",
                f"- Category: {item.category}",
                f"- Company: {item.company}",
                f"- Product: {item.product}",
                f"- Judges: {', '.join(item.judge_ids)}",
                f"- Judge count: {item.judge_count}",
                f"- Consensus total: {item.scores.total}/400",
                f"- Score range: {item.score_range}",
                f"- Disagreement level: {item.disagreement_level}",
                f"- Verdict: {item.verdict}",
                f"- Verdict distribution: {json.dumps(item.verdict_counts, sort_keys=True)}",
                f"- Confidence: {item.confidence}",
                f"- Confidence distribution: {json.dumps(item.confidence_counts, sort_keys=True)}",
                f"- Summary: {item.summary or 'No summary provided.'}",
                "- Evidence:",
                *[f"  - {value}" for value in item.evidence_cited],
                "- Shared strengths:",
                *[f"  - {value}" for value in item.strengths],
                "- Shared concerns:",
                *[f"  - {value}" for value in item.concerns],
                "",
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")
