# AI Awards Judge - Non-Technical Handoff

## What this is

This is a ready-to-use judging framework for awards, shortlist reviews, and category ranking.

It can:

- score submissions using built-in heuristic logic
- optionally use an LLM for more structured scoring
- export results as JSON and CSV
- compare results from multiple judges
- flag where judges disagree most

## Where it lives

GitHub repository:

`https://github.com/Anktrinity/ai-awards-judge`

## What someone needs to know before using it

- It already works in a basic mode without any AI API key.
- If someone wants LLM-backed scoring, they must connect **their own** API key.
- The repository does **not** contain my personal OpenAI key.
- The project is meant to be cloned from GitHub and run in the user's own environment.

## Simplest way to describe it

"This is a configurable judging toolkit. You can run it as-is with built-in scoring, or connect your own OpenAI-compatible API key if you want model-backed judging. It also supports reconciliation across multiple judges."

## What they need to do

1. Clone the GitHub repository
2. Install Python and the project dependencies
3. Run it in heuristic mode first
4. Optionally connect their own API key for LLM scoring
5. Review the README and deployment docs

## Important reassurance

If they are non-technical, the key point is:

- they do **not** need to manage my credentials
- they do **not** need access to my local machine
- they can deploy or run it from the GitHub repo in their own setup
- if they do want AI scoring, they use **their own** provider account and key

## Suggested message to send

Hi — I’ve put the judging system on GitHub here:

`https://github.com/Anktrinity/ai-awards-judge`

It already supports:
- standard heuristic scoring
- optional LLM-backed scoring
- CSV and JSON exports
- multi-judge reconciliation
- disagreement tracking

You can run it without any API key in heuristic mode.
If you want LLM-backed scoring, you’ll need to connect your own OpenAI-compatible API key in your own environment.

The repo does not include any of my personal keys or credentials.

Start with the `README.md`, then check `docs/deployment.md`.
