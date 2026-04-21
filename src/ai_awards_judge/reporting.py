from __future__ import annotations

from pathlib import Path
import json

from ai_awards_judge.models import JudgedEntry


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
                f"- Summary: {judged.entry.summary or 'No summary provided.'}",
                "- Evidence:",
            ]
        )
        if judged.entry.evidence:
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
