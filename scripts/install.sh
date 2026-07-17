#!/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SRC_DIR="$ROOT_DIR/skills"
DEST_ROOT="${CODEX_HOME:-$HOME/.codex}"
DEST_DIR="$DEST_ROOT/skills"
FORCE=0

if [ "${1:-}" = "--force" ]; then
  FORCE=1
elif [ "${1:-}" != "" ]; then
  echo "Usage: $0 [--force]" >&2
  exit 1
fi

if [ ! -d "$SRC_DIR" ]; then
  echo "Missing source skills directory: $SRC_DIR" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"

for skill_dir in "$SRC_DIR"/lean-*; do
  [ -d "$skill_dir" ] || continue
  skill_name=$(basename "$skill_dir")
  target="$DEST_DIR/$skill_name"

  if [ -e "$target" ]; then
    if [ "$FORCE" -ne 1 ]; then
      echo "Refusing to overwrite existing skill: $target" >&2
      echo "Re-run with --force to replace installed Lean-SDLC skills." >&2
      exit 1
    fi
    rm -rf "$target"
  fi

  cp -R "$skill_dir" "$target"
  echo "Installed $skill_name -> $target"
done

echo "Lean-SDLC install complete."
echo "Restart Codex to pick up new skills."
