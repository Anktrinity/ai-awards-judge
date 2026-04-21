# Award Review Workspace

Use this folder for live judging batches.

## Suggested structure
- `originals/` copied source files
- `extracted_text/` text extracted from submissions
- `reports/` one markdown report per entry
- `master-summary.md` batch ranking and shortlist notes

## Current source
`~/Downloads/2026_SPEAKING/2026_AI Awards Judge`

## Reusable workflow
1. Run `scripts/run_award_intake.sh`
2. Review `extracted_text/` for new entries
3. Score each entry using the event-awards-judge skill
4. Write one report per entry in `reports/`
5. Update `master-score-sheet.md`
6. Mark results provisional if the intake is still changing

## Scripts
- `scripts/sync_entries.sh` copies supported files from the source folder into `originals/`
- `scripts/extract_entries.py` extracts text from new or changed PDFs only
- `scripts/run_award_intake.sh` runs both steps and bootstraps a local venv with `pypdf`
