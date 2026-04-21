#!/bin/zsh
set -euo pipefail

SRC_DEFAULT="$HOME/Downloads/2026_SPEAKING/2026_AI Awards Judge"
SRC="${1:-$SRC_DEFAULT}"
DEST_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ORIGINALS="$DEST_DIR/originals"

mkdir -p "$ORIGINALS"

if [[ ! -d "$SRC" ]]; then
  echo "Source folder not found: $SRC" >&2
  exit 1
fi

rsync -a --ignore-existing \
  --include='*.pdf' \
  --include='*.docx' \
  --include='*.pptx' \
  --include='*.txt' \
  --include='*/' \
  --exclude='*' \
  "$SRC/" "$ORIGINALS/"

echo "Synced files into: $ORIGINALS"
find "$ORIGINALS" -type f | sort
