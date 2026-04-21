#!/bin/zsh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT/.venv"
SRC="${1:-$HOME/Downloads/2026_SPEAKING/2026_AI Awards Judge}"

"$ROOT/scripts/sync_entries.sh" "$SRC"

if [[ ! -d "$VENV" ]]; then
  python3 -m venv "$VENV"
fi
source "$VENV/bin/activate"
pip -q install pypdf >/dev/null
python "$ROOT/scripts/extract_entries.py"

echo "\nIntake complete. Originals: $ROOT/originals, Extracted text: $ROOT/extracted_text"
