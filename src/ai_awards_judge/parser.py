from __future__ import annotations

from pathlib import Path

from ai_awards_judge.models import Entry


def _extract_field(text: str, label: str) -> str:
    prefix = f"{label}:"
    for line in text.splitlines():
        if line.strip().startswith(prefix):
            return line.split(":", 1)[1].strip()
    return ""


def _extract_block(text: str, label: str, next_labels: list[str]) -> str:
    lines = text.splitlines()
    capture = False
    collected: list[str] = []
    target = f"{label}:"
    stop_tokens = [f"{item}:" for item in next_labels]

    for line in lines:
        stripped = line.strip()
        if not capture and stripped == target:
            capture = True
            continue
        if capture and any(stripped.startswith(token) for token in stop_tokens):
            break
        if capture:
            collected.append(line.rstrip())
    return "\n".join(collected).strip()


def parse_entry_file(path: Path) -> Entry:
    raw_text = path.read_text(encoding="utf-8")
    summary = _extract_block(raw_text, "Summary", ["Evidence", "Notes"])
    evidence_block = _extract_block(raw_text, "Evidence", ["Notes"])
    evidence = [line.strip("- ").strip() for line in evidence_block.splitlines() if line.strip()]
    notes = _extract_block(raw_text, "Notes", [])

    return Entry(
        path=str(path),
        category=_extract_field(raw_text, "Category") or "Uncategorized",
        entrant=_extract_field(raw_text, "Entrant") or path.stem,
        company=_extract_field(raw_text, "Company") or "Unknown",
        product=_extract_field(raw_text, "Product") or "Unknown",
        summary=summary,
        evidence=evidence,
        notes=notes,
        raw_text=raw_text,
    )


def load_entries(input_dir: Path) -> list[Entry]:
    return [parse_entry_file(path) for path in sorted(input_dir.rglob("*.txt"))]
