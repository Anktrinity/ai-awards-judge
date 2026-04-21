from pathlib import Path

from ai_awards_judge.parser import parse_entry_file
from ai_awards_judge.scoring import rank_by_category, score_entry


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_parse_entry_file_extracts_fields(tmp_path: Path) -> None:
    sample = tmp_path / "entry.txt"
    sample.write_text(
        """Category: Best AI for Registration & Onboarding
Entrant: ExampleFlow
Company: Example Labs
Product: ExampleFlow Check-In AI

Summary:
Fast onboarding workflow.

Evidence:
- Reduced check-in time by 50%
- Deployed across 3 events

Notes:
Early-stage but promising.
""",
        encoding="utf-8",
    )

    entry = parse_entry_file(sample)

    assert entry.category == "Best AI for Registration & Onboarding"
    assert entry.entrant == "ExampleFlow"
    assert len(entry.evidence) == 2


def test_score_and_rank_entries() -> None:
    first = parse_entry_file(REPO_ROOT / "examples/sample_input/sample_entry_01.txt")
    second = parse_entry_file(REPO_ROOT / "examples/sample_input/sample_entry_02.txt")

    judged = [score_entry(first), score_entry(second)]
    rankings = rank_by_category(judged)

    assert judged[0].scores.total > 0
    assert judged[1].scores.total > 0
    assert "Best AI for Registration & Onboarding" in rankings
    assert "Most Innovative AI Application in Events" in rankings
