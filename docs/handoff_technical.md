# AI Awards Judge - Technical Deployment Handoff

## Repository

GitHub:

`https://github.com/Anktrinity/ai-awards-judge`

## Overview

This repository contains a configurable judging workflow for award entries, shortlist reviews, and category ranking.

Current capabilities:

- heuristic scoring engine
- optional LLM-backed scoring with structured outputs
- JSON and CSV export
- multi-judge reconciliation
- disagreement analytics
- GitHub Actions test workflow

## Runtime requirements

- Python 3.11+
- local shell access or deployment environment that supports Python virtual environments

## Basic setup

```bash
git clone https://github.com/Anktrinity/ai-awards-judge.git
cd ai-awards-judge
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## First run

Run heuristic mode first to validate the install without any external model dependency:

```bash
ai-awards-judge run ./examples/sample_input --output-dir ./outputs --scoring-mode heuristic
```

Outputs include:

- `judged_entries.json`
- `judged_entries.csv`
- `judging_report.md`
- `run_manifest.json`

## LLM-backed scoring

LLM scoring is optional and uses a **bring-your-own-key** model.

Required environment variable:

```bash
export OPENAI_API_KEY=your_key_here
```

Optional overrides:

```bash
export AI_AWARDS_JUDGE_MODEL=gpt-4o-mini
export AI_AWARDS_JUDGE_BASE_URL=https://api.openai.com/v1
export AI_AWARDS_JUDGE_ID=judge-name
```

Then run:

```bash
ai-awards-judge run ./examples/sample_input --output-dir ./outputs --scoring-mode llm
```

Or use fallback mode:

```bash
ai-awards-judge run ./examples/sample_input --output-dir ./outputs --scoring-mode auto
```

### Important credential note

The repo does **not** include any bundled API credentials.
Do not expect access to the original maintainer's OpenAI key.
Any deployer or end user who wants LLM scoring must provide their **own** API key through environment variables, a secret manager, or platform config.

## Multi-judge reconciliation

You can merge multiple `judged_entries.json` outputs into a consensus result:

```bash
ai-awards-judge reconcile judge_a/judged_entries.json judge_b/judged_entries.json --output-dir ./outputs/reconciled
```

Reconciliation outputs:

- `reconciled_entries.json`
- `reconciled_entries.csv`
- `reconciliation_report.md`

Each reconciled entry includes:

- averaged consensus scores
- score range across judges
- disagreement level
- verdict distribution
- confidence distribution

## Key files

- `README.md`
- `docs/deployment.md`
- `docs/methodology.md`
- `config/rubric.yaml`
- `config/prompts.yaml`
- `config/categories.yaml`

## GitHub Actions

CI is configured in:

- `.github/workflows/tests.yml`

It runs the Python test suite on push and pull request.

## Recommended deployment approach

1. Clone the repo into the target environment
2. Create and activate a venv
3. Install with `pip install -e '.[dev]'`
4. Run tests
5. Validate heuristic mode
6. Add provider credentials only if LLM scoring is required
7. Store credentials outside the repo

## Suggested technical handoff note

This repo is ready to clone and run locally.

Start by validating the environment with:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
ai-awards-judge run ./examples/sample_input --output-dir ./outputs --scoring-mode heuristic
```

If you want model-backed scoring, inject your own `OPENAI_API_KEY` and use `--scoring-mode llm` or `auto`.
No maintainer API key is included in the repository.
