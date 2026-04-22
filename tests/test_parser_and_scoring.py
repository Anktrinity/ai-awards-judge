import csv
import json
from pathlib import Path

from ai_awards_judge.parser import parse_entry_file
from ai_awards_judge.reconciliation import reconcile_entries
from ai_awards_judge.reporting import write_csv, write_reconciliation_markdown
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
    assert judged[0].concise_summary
    assert judged[0].judge_id == "heuristic"
    assert judged[1].scores.total > 0
    assert "Best AI for Registration & Onboarding" in rankings
    assert "Most Innovative AI Application in Events" in rankings


def test_write_csv_exports_scores(tmp_path: Path) -> None:
    entry = parse_entry_file(REPO_ROOT / "examples/sample_input/sample_entry_01.txt")
    judged = score_entry(entry)
    out_path = tmp_path / "judged_entries.csv"

    write_csv([judged], out_path)

    rows = list(csv.DictReader(out_path.open("r", encoding="utf-8")))
    assert len(rows) == 1
    assert rows[0]["entrant"] == entry.entrant
    assert rows[0]["total"] == str(judged.scores.total)


def test_reconcile_entries_averages_scores_and_tracks_disagreement() -> None:
    entry = parse_entry_file(REPO_ROOT / "examples/sample_input/sample_entry_01.txt")
    judge_a = score_entry(entry)
    payload = judge_a.to_dict()
    payload["judge_id"] = "judge-b"
    payload["scores"]["innovation"] = judge_a.scores.innovation - 10
    payload["scores"]["impact"] = judge_a.scores.impact - 5
    payload["scores"]["results"] = judge_a.scores.results - 15
    payload["verdict"] = "Competitive shortlist contender"
    payload["confidence"] = "medium"
    payload["scores"]["total"] = sum(
        payload["scores"][key] for key in ["innovation", "impact", "execution", "results"]
    )
    judge_b = type(judge_a).from_dict(payload)

    reconciled = reconcile_entries([judge_a, judge_b])

    assert len(reconciled) == 1
    assert reconciled[0].judge_count == 2
    assert reconciled[0].scores.innovation == round((judge_a.scores.innovation + judge_b.scores.innovation) / 2)
    assert reconciled[0].score_range == abs(judge_a.scores.total - judge_b.scores.total)
    assert reconciled[0].disagreement_level in {"low", "medium", "high"}
    assert sum(reconciled[0].verdict_counts.values()) == 2
    assert sum(reconciled[0].confidence_counts.values()) == 2
    assert json.loads(json.dumps(reconciled[0].to_dict()))["judge_count"] == 2


def test_write_reconciliation_markdown_includes_disagreement_summary(tmp_path: Path) -> None:
    entry = parse_entry_file(REPO_ROOT / "examples/sample_input/sample_entry_01.txt")
    judged = score_entry(entry)
    reconciled = reconcile_entries([judged])
    out_path = tmp_path / "reconciliation_report.md"

    write_reconciliation_markdown(reconciled, out_path)

    content = out_path.read_text(encoding="utf-8")
    assert "AI Awards Judge Reconciliation Report" in content
    assert "Disagreement level" in content
    assert judged.entry.entrant in content
