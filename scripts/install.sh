#!/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SOURCE_SKILL="$ROOT_DIR/skills/lean-sdlc"
DEST_ROOT="${LEAN_SDLC_INSTALL_ROOT:-${CODEX_HOME:-$HOME/.codex}}"
DEST_DIR="$DEST_ROOT/skills"
TARGET="$DEST_DIR/lean-sdlc"
FORCE=0

LEGACY_SKILLS="
lean-sdlc-core
lean-brainstorm
lean-refine
lean-architecture
lean-task-planning
lean-execution
lean-debugging
lean-implementation
lean-verification
lean-traceability
lean-versioning
lean-doc-maintenance
"

if [ "${1:-}" = "--force" ]; then
  FORCE=1
elif [ "${1:-}" != "" ]; then
  echo "Usage: $0 [--force]" >&2
  exit 1
fi

if [ ! -f "$SOURCE_SKILL/SKILL.md" ]; then
  echo "Missing source skill: $SOURCE_SKILL" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"

CONFLICTS=""
if [ -e "$TARGET" ]; then
  CONFLICTS="$CONFLICTS lean-sdlc"
fi

for skill_name in $LEGACY_SKILLS; do
  if [ -e "$DEST_DIR/$skill_name" ]; then
    CONFLICTS="$CONFLICTS $skill_name"
  fi
done

if [ -n "$CONFLICTS" ] && [ "$FORCE" -ne 1 ]; then
  echo "Existing Lean-SDLC installation detected:$CONFLICTS" >&2
  echo "Re-run with --force to replace it with the single lean-sdlc skill." >&2
  exit 1
fi

if [ "$FORCE" -eq 1 ]; then
  if [ -e "$TARGET" ]; then
    rm -rf "$TARGET"
    echo "Removed lean-sdlc"
  fi
  for skill_name in $LEGACY_SKILLS; do
    legacy_target="$DEST_DIR/$skill_name"
    if [ -e "$legacy_target" ]; then
      rm -rf "$legacy_target"
      echo "Removed legacy $skill_name"
    fi
  done
fi

cp -R "$SOURCE_SKILL" "$TARGET"
echo "Installed lean-sdlc -> $TARGET"
echo "Restart Codex to pick up the skill."
