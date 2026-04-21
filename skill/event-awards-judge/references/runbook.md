# Runbook

## Use case
Use this runbook when judging a live batch of award entries, especially when files are still arriving and the review will be rerun later.

## Standard operating procedure

1. Intake
- Confirm the source folder.
- Copy source files into a workspace review folder if needed.
- Record file list and timestamps.
- Note missing or partially downloaded files.

2. Normalize
- Extract readable text from PDFs or other submission formats.
- Keep extracted text alongside originals for repeatability.
- Preserve filename to maintain category and entrant context.

3. Review individually
- Read each entry on its own merits first.
- Fill one report per entry using the shared template.
- Score all four criteria with short rationales.

4. Compare by category
- Group entries by category.
- Rank by total score.
- Add a narrative note about where leaders outperform others.
- Flag near-ties and subjective calls.

5. Publish outputs
- Per-entry reports
- Master category summary
- Optional shortlist recommendation

## Folder pattern

```text
award_review/
  originals/
  extracted_text/
  reports/
  master-summary.md
```

## Naming pattern
- Keep original filenames whenever possible.
- For reports, use a clean slug plus `-report.md`.

## Recommended deliverables

### Per-entry report
Short, defensible, evidence-based.

### Master summary
Include:
- category
- entrant
- total /400
- rank in category
- short decision note

## Provisional language
Use wording like:
- "Provisional, as additional entries may still be downloading."
- "Based on the materials provided in this file."
- "Score reflects current evidence rather than assumed future performance."

## Good judging behavior
- Be consistent.
- Be direct.
- Avoid being seduced by slick decks without proof.
- Avoid underrating less polished but genuinely differentiated entries with credible traction.
