# AI Awards Judge

A GitHub-ready starter kit for turning awards judging into a reusable, auditable, deployable workflow.

This repo packages the judging logic into a configurable system that can be reused for event tech awards, AI awards, startup competitions, innovation showcases, and shortlist reviews.

## Release model

This repository is prepared for a **hybrid publishing model**:

- **public repo**: framework, code, rubric, templates, docs, sanitized examples
- **private archive**: original submissions, extracted text from real entrants, internal judging outputs, confidential notes

See `docs/hybrid-publishing.md` for the operating model.

## What it includes

- Config-driven rubric and category settings
- Reusable judging methodology docs
- A starter Python CLI for local batch runs
- Templates for reports and master summaries
- Docker-ready structure and environment config
- Sanitized example inputs and outputs
- Reusable OpenClaw skill assets

## Repo layout

```text
ai_awards_judging/
  config/                  # Rubric, category, prompt, and output settings
  docs/                    # Methodology, deployment notes, rubric, GitHub publishing
  examples/                # Sanitized sample input and output artifacts
  private_archive_reference/
  scripts/                 # Helper scripts and bootstrap helpers
  src/ai_awards_judge/     # Starter package and CLI
  templates/               # Report templates
  tests/                   # Starter tests
```

## Current status

This is **v1 scaffolded and ready for GitHub push**.

Ready now:
- standalone git repo on `main`
- docs and config separation
- starter CLI interface
- sanitized sample data
- hybrid publishing guidance

Still to build for a fuller product:
- LLM-backed or rules-plus-LLM scoring execution
- multi-judge reconciliation
- web UI or hosted API layer
- CI publishing workflow

## Quick start

### 1. Install locally

```bash
cd ai_awards_judging
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Run the starter CLI

Preview config:

```bash
ai-awards-judge inspect-config
```

Create a starter run manifest:

```bash
ai-awards-judge plan-run --input-dir ./examples/sample_input --output-dir ./outputs
```

Run the initial scoring engine on sanitized text entries:

```bash
ai-awards-judge run ./examples/sample_input --output-dir ./outputs
```

## Push to GitHub

If you already have a GitHub repo created:

```bash
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

If you use GitHub CLI and are authenticated:

```bash
gh repo create ai-awards-judge --public --source=. --remote=origin --push
```

## Documentation

- `docs/methodology.md`
- `docs/rubric.md`
- `docs/deployment.md`
- `docs/hybrid-publishing.md`
- `docs/github-publish-checklist.md`

## Design principles

- **Auditable**: scoring policy, prompts, and outputs are separate
- **Reusable**: categories and rubric are configurable, not hardcoded
- **Defensible**: evidence quality and tie-breaks are explicit
- **Portable**: local-first, easy to containerize, easy to extend

## Recommended GitHub repo description

> Configurable AI-assisted judging system for award entries, shortlist reviews, and category ranking workflows.

## Current scoring engine

The current `run` command is a v0 heuristic scoring engine for sanitized text entries. It:

- parses text entry files
- assigns rubric scores using evidence and keyword heuristics
- ranks entries within category
- writes JSON and markdown outputs

Example:

```bash
ai-awards-judge run ./examples/sample_input --output-dir ./outputs
```

## Next build step

After this, the strongest upgrade is replacing or augmenting the heuristic engine with model-backed scoring plus multi-judge reconciliation.
