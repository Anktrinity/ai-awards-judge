from __future__ import annotations

import argparse
import json
from pathlib import Path

from ai_awards_judge.config import load_all_config
from ai_awards_judge.parser import load_entries
from ai_awards_judge.planner import build_manifest, write_manifest
from ai_awards_judge.reconciliation import reconcile_json_files
from ai_awards_judge.reporting import (
    write_csv,
    write_json,
    write_markdown,
    write_reconciliation_csv,
    write_reconciliation_json,
    write_reconciliation_markdown,
)
from ai_awards_judge.scoring import rank_by_category, score_entry_auto


def cmd_inspect_config(_: argparse.Namespace) -> int:
    print(json.dumps(load_all_config(), indent=2))
    return 0


def cmd_plan_run(args: argparse.Namespace) -> int:
    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    if not input_dir.exists() or not input_dir.is_dir():
        raise SystemExit(f"Input directory not found: {input_dir}")

    manifest = build_manifest(input_dir, output_dir)
    manifest_path = output_dir / "run_manifest.json"
    write_manifest(manifest, manifest_path)
    print(f"Wrote run manifest to {manifest_path}")
    print(f"Discovered {len(manifest.discovered_files)} files")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    if not input_dir.exists() or not input_dir.is_dir():
        raise SystemExit(f"Input directory not found: {input_dir}")

    entries = load_entries(input_dir)
    if not entries:
        raise SystemExit(f"No .txt entries found in {input_dir}")

    config = load_all_config()
    judged_entries = [
        score_entry_auto(
            entry,
            rubric=config["rubric"],
            prompts=config["prompts"],
            scoring_mode=args.scoring_mode,
        )
        for entry in entries
    ]
    category_rankings = rank_by_category(judged_entries)

    write_json(judged_entries, output_dir / "judged_entries.json")
    write_csv(judged_entries, output_dir / "judged_entries.csv")
    write_markdown(judged_entries, category_rankings, output_dir / "judging_report.md")

    manifest = build_manifest(input_dir, output_dir)
    manifest.status = "completed"
    write_manifest(manifest, output_dir / "run_manifest.json")

    print(f"Scored {len(judged_entries)} entries using {args.scoring_mode} mode")
    print(f"Wrote JSON results to {output_dir / 'judged_entries.json'}")
    print(f"Wrote CSV results to {output_dir / 'judged_entries.csv'}")
    print(f"Wrote markdown report to {output_dir / 'judging_report.md'}")
    return 0


def cmd_reconcile(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir).resolve()
    inputs = [Path(item).resolve() for item in args.inputs]
    missing = [str(path) for path in inputs if not path.exists()]
    if missing:
        raise SystemExit(f"Missing judged entry files: {', '.join(missing)}")

    reconciled = reconcile_json_files(inputs)
    write_reconciliation_json(reconciled, output_dir / "reconciled_entries.json")
    write_reconciliation_csv(reconciled, output_dir / "reconciled_entries.csv")
    write_reconciliation_markdown(reconciled, output_dir / "reconciliation_report.md")

    print(f"Reconciled {len(reconciled)} entries from {len(inputs)} judge files")
    print(f"Wrote JSON results to {output_dir / 'reconciled_entries.json'}")
    print(f"Wrote CSV results to {output_dir / 'reconciled_entries.csv'}")
    print(f"Wrote markdown report to {output_dir / 'reconciliation_report.md'}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-awards-judge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_config = subparsers.add_parser("inspect-config", help="Print merged config as JSON")
    inspect_config.set_defaults(func=cmd_inspect_config)

    plan_run = subparsers.add_parser("plan-run", help="Create a starter manifest for a judging run")
    plan_run.add_argument("--input-dir", required=True, help="Folder containing entry files")
    plan_run.add_argument("--output-dir", default="./outputs", help="Folder to receive generated outputs")
    plan_run.set_defaults(func=cmd_plan_run)

    run = subparsers.add_parser("run", help="Score sanitized text entries and generate reports")
    run.add_argument("input_dir", help="Folder containing .txt entry files")
    run.add_argument("--output-dir", default="./outputs", help="Folder to receive generated outputs")
    run.add_argument(
        "--scoring-mode",
        choices=["heuristic", "llm", "auto"],
        default="heuristic",
        help="heuristic uses the local engine, llm uses an OpenAI-compatible API, auto falls back to heuristics if the API is unavailable",
    )
    run.set_defaults(func=cmd_run)

    reconcile = subparsers.add_parser("reconcile", help="Merge multiple judged_entries.json files into a consensus view")
    reconcile.add_argument("inputs", nargs="+", help="One or more judged_entries.json files")
    reconcile.add_argument("--output-dir", default="./outputs", help="Folder to receive reconciled outputs")
    reconcile.set_defaults(func=cmd_reconcile)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
