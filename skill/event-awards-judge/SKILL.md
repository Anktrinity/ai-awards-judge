---
name: event-awards-judge
description: Judge award entries for event technology or AI awards using a consistent rubric, per-entry scorecards, category-level comparisons, and shortlist recommendations. Use when reviewing a folder of submissions (PDF, DOCX, slide exports, or extracted text), when entries are still arriving and the review needs to be rerun later, or when creating structured judge reports that balance rubric-based scoring with cross-entry context.
---

# Event Awards Judge

Use this skill to turn a batch of award submissions into a consistent judging workflow.

## Workflow

1. Normalize the intake
- Collect entries in one folder.
- Prefer one file per entry, or one subfolder per entry.
- Preserve original filenames because category and entrant details often live there.
- If files are outside the workspace, copy them into the workspace before analysis.

2. Build the working set
- Group entries by category before scoring.
- Track incomplete downloads and mark any report provisional if the batch is still changing.
- Create extracted text copies when needed so later passes are faster and more repeatable.

3. Score each entry against the rubric first
- Score Innovation, Impact, Execution, and Results from 0 to 100 each.
- Judge primarily against the rubric, not only relative to the field.
- Do not penalize early-stage entries for being early; reward credible traction, product clarity, pilot evidence, and believable path to impact.

4. Write a per-entry report
- Use the report template in `assets/report-template.md`.
- Keep reports concise but evidence-based.
- Separate observed evidence from inference.
- Call out gaps, unsupported claims, or weak metrics directly but fairly.

5. Compare within each category
- After individual scoring, compare entrants inside the same category.
- Note where the leader wins: originality, proof, product maturity, customer validation, or commercial traction.
- Flag close calls and tie-break factors.

6. Produce a master summary
- Create a category table with totals and ranking.
- Add a shortlist recommendation and a short note on confidence level.
- If entries are still arriving, state that rankings are provisional.

## Scoring guidance

Read `references/scoring-guide.md` before scoring.

## Output pattern

For each entry, include:
- Category
- Entrant / company / product
- Concise summary
- Evidence cited
- Strengths
- Concerns or gaps
- Innovation /100 with rationale
- Impact /100 with rationale
- Execution /100 with rationale
- Results /100 with rationale
- Total /400
- Short verdict

Then include:
- Within-category comparison
- Provisional category leader(s)
- Overall notes on fairness, evidence quality, and any incomplete intake

## Practical rules

- Reward specificity over hype.
- Reward credible numbers, pilots, testimonials, letters of intent, partnerships, and product maturity signals.
- Treat vague claims, missing baselines, and unsupported ROI carefully.
- Separate "interesting idea" from "well evidenced outcome."
- Distinguish true workflow innovation from simple LLM add-ons.
- Preserve a paper trail so the scoring can be defended later.

## Resources

- `references/scoring-guide.md`: score bands and judging heuristics.
- `references/runbook.md`: repeatable operating procedure for batch reviews.
- `assets/report-template.md`: reusable per-entry report structure.
- `assets/master-summary-template.md`: category and shortlist summary structure.
