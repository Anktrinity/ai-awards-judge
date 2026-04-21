# Push to GitHub

## Option A, GitHub CLI

Authenticate first:

```bash
gh auth login -h github.com
```

Then from the repo root:

```bash
gh repo create ai-awards-judge --public --source=. --remote=origin --push
```

## Option B, existing GitHub repo URL

If the repo already exists:

```bash
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

## Recommended repo metadata

- Name: `ai-awards-judge`
- Visibility: Public
- Description: `Configurable AI-assisted judging system for award entries, shortlist reviews, and category ranking workflows.`
- Topics: `ai`, `awards`, `judging`, `evaluation`, `event-tech`, `open-source`

## Private companion repo

Create a second private repo for confidential project materials, for example:

- Name: `ai-awards-judge-private-data`
- Visibility: Private

Store the private archive there, not in the public repo.
