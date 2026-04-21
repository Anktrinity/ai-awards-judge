# Deployment Notes

## Local developer setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Docker direction for v1

Recommended container behavior:
- mount an input folder
- mount an output folder
- pass config paths with env vars or flags

Example future usage:

```bash
docker build -t ai-awards-judge .
docker run --rm \
  -v $(pwd)/entries:/app/entries \
  -v $(pwd)/outputs:/app/outputs \
  ai-awards-judge plan-run --input-dir /app/entries --output-dir /app/outputs
```

## Hosted deployment later

Good next deployment options:
- FastAPI service on Render or Fly.io
- containerized worker for batch runs
- Supabase or Postgres for multi-judge result storage

## GitHub release checklist

- README complete
- license added
- config files externalized
- sample input and output included
- .env.example included
- package installs cleanly
- first tag created
