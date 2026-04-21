# AI Awards Judge Project Index

This repository is now the **public-safe core** of the judging system.

## Key public files
- `README.md`
- `JUDGE_SCORING_GUIDE.md`
- `config/rubric.yaml`
- `config/categories.yaml`
- `config/prompts.yaml`
- `docs/methodology.md`
- `docs/hybrid-publishing.md`
- `src/ai_awards_judge/cli/main.py`

## Sanitized examples
- `examples/sample_input/`
- `examples/sample_output/`

## Private archive reference
Confidential intake files, real entrant submissions, extracted text, and internal judging outputs were intentionally moved out of this public repo.

Reference:
- `private_archive_reference/README.md`

## Intended next implementation step
Build the scoring engine behind:

`ai-awards-judge run ./entries --config ./config/rubric.yaml --out ./outputs`
