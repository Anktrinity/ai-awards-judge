#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
ORIGINALS = ROOT / 'originals'
EXTRACTED = ROOT / 'extracted_text'
STATE = ROOT / '.extract_state.json'
EXTRACTED.mkdir(parents=True, exist_ok=True)

state = {}
if STATE.exists():
    try:
        state = json.loads(STATE.read_text())
    except Exception:
        state = {}

try:
    from pypdf import PdfReader
except Exception:
    print('Missing dependency: pypdf. Install in a venv before running.', file=sys.stderr)
    sys.exit(1)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

processed = 0
skipped = 0

for path in sorted(ORIGINALS.rglob('*')):
    if not path.is_file():
        continue
    ext = path.suffix.lower()
    if ext != '.pdf':
        continue
    rel = str(path.relative_to(ORIGINALS))
    digest = sha256(path)
    out = EXTRACTED / (path.stem + '.txt')
    if state.get(rel) == digest and out.exists():
        skipped += 1
        print(f'SKIP\t{rel}')
        continue

    reader = PdfReader(str(path))
    parts = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ''
        except Exception as e:
            text = f'\n[ERROR extracting page {i}: {e}]\n'
        parts.append(f'\n\n===== PAGE {i} =====\n\n{text}')
    out.write_text(''.join(parts))
    state[rel] = digest
    processed += 1
    print(f'OK\t{rel}\tpages={len(reader.pages)}\tout={out.name}')

STATE.write_text(json.dumps(state, indent=2, sort_keys=True))
print(f'Processed: {processed}, skipped: {skipped}')
