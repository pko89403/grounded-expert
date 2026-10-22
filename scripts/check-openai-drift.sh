#!/usr/bin/env bash
# Apply the explicitly reviewed host adaptation to a temporary copy, then
# compare the entire file, including trigger metadata. Never edits plugin/.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
CLAUDE_FILE="$REPO_DIR/plugin/SKILL.md"
OPENAI_FILE="$REPO_DIR/hosts/openai/skills/grounded-expert/SKILL.md"
ADAPTATION="$REPO_DIR/scripts/openai-skill.patch"

for file in "$CLAUDE_FILE" "$OPENAI_FILE" "$ADAPTATION"; do
  [[ -f "$file" ]] || { echo "missing: $file" >&2; exit 1; }
done

CHECK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/grounded-expert-drift.XXXXXX")"
cleanup() {
  # Only the known generated files, never a recursive directory removal.
  rm -f "$CHECK_DIR/expected.md" "$CHECK_DIR/expected.md.rej" "$CHECK_DIR/patch.log"
  rmdir "$CHECK_DIR"
}
trap cleanup EXIT

# No fuzzy context matching or reverse-patch inference. Source edits affecting
# an adaptation require an explicit update to the reviewed patch.
if ! patch --batch --forward --fuzz=0 --output="$CHECK_DIR/expected.md" \
    "$CLAUDE_FILE" "$ADAPTATION" > "$CHECK_DIR/patch.log" 2>&1; then
  cat "$CHECK_DIR/patch.log" >&2
  echo "DRIFT: update the reviewed OpenAI adaptation for the changed source." >&2
  exit 1
fi

if diff -u --label 'reviewed OpenAI adaptation' --label 'OpenAI SKILL.md' \
    "$CHECK_DIR/expected.md" "$OPENAI_FILE"; then
  echo 'OK: OpenAI skill exactly matches the reviewed adaptation.'
else
  echo 'DRIFT: unreviewed OpenAI skill or trigger change.' >&2
  exit 1
fi
