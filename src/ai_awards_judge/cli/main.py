from __future__ import annotations

import argparse
import json
from pathlib import Path

from ai_awards_judge.config import load_all_config
from ai_awards_judge.parser import load_entries
from ai_awards_judge.planner import build_manifest, write_manifest
from ai_awards_judge.reporting import write_json, write_markdown
from ai_awards_judge.scoring import rank_by_category, score_entry


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

    judged_entries = [score_entry(entry) for entry in entries]
    category_rankings = rank_by_category(judged_entries)

    write_json(judged_entries, output_dir / "judged_entries.json")
    write_markdown(judged_entries, category_rankings, output_dir / "judging_report.md")

    manifest = build_manifest(input_dir, output_dir)
    manifest.status = "completed"
    write_manifest(manifest, output_dir / "run_manifest.json")

    print(f"Scored {len(judged_entries)} entries")
    print(f"Wrote JSON results to {output_dir / 'judged_entries.json'}")
    print(f"Wrote markdown report to {output_dir / 'judging_report.md'}")
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
    run.set_defaults(func=cmd_run)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
