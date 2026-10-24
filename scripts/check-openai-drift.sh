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
[[ -s "$ADAPTATION" ]] || { echo "empty adaptation: $ADAPTATION" >&2; exit 1; }

for dependency in patch mktemp diff awk; do
  command -v "$dependency" >/dev/null 2>&1 || {
    echo "error: required command unavailable: $dependency" >&2
    exit 127
  }
done

count_deletions() {
  awk '/^-/ && !/^--- / {count++} END {print count+0}'
}
current_deletions="$(count_deletions < "$ADAPTATION")"
echo "OpenAI adaptation deleted lines: $current_deletions"
if [[ -n "${OPENAI_PATCH_BASE_REF:-}" ]]; then
  git -C "$REPO_DIR" rev-parse --verify "$OPENAI_PATCH_BASE_REF^{commit}" >/dev/null 2>&1 || {
    echo "error: unavailable patch baseline: $OPENAI_PATCH_BASE_REF" >&2
    exit 2
  }
  baseline_deletions=0
  if git -C "$REPO_DIR" cat-file -e "$OPENAI_PATCH_BASE_REF:scripts/openai-skill.patch" 2>/dev/null; then
    baseline_deletions="$(git -C "$REPO_DIR" show "$OPENAI_PATCH_BASE_REF:scripts/openai-skill.patch" | count_deletions)"
  fi
  echo "OpenAI adaptation deletion delta: $baseline_deletions -> $current_deletions ($((current_deletions - baseline_deletions)))"
fi

CHECK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/grounded-expert-drift.XXXXXX")"
cleanup() {
  local result=$?
  # Only the known generated files, never a recursive directory removal.
  rm -f "$CHECK_DIR/expected.md" "$CHECK_DIR/expected.md.rej" "$CHECK_DIR/expected.md.orig" "$CHECK_DIR/patch.log" || true
  rmdir "$CHECK_DIR" 2>/dev/null || true
  return "$result"
}
trap cleanup EXIT

# No fuzzy context matching or reverse-patch inference. Source edits affecting
# an adaptation require an explicit update to the reviewed patch.
if patch --batch --forward --fuzz=0 --output="$CHECK_DIR/expected.md" \
    "$CLAUDE_FILE" "$ADAPTATION" > "$CHECK_DIR/patch.log" 2>&1; then
  :
else
  result=$?
  cat "$CHECK_DIR/patch.log" >&2
  if [[ "$result" -ne 1 ]]; then
    echo "error: patch could not run successfully (status $result)." >&2
    exit "$result"
  fi
  echo "DRIFT: update the reviewed OpenAI adaptation for the changed source." >&2
  exit 1
fi

if diff -u --label 'reviewed OpenAI adaptation' --label 'OpenAI SKILL.md' \
    "$CHECK_DIR/expected.md" "$OPENAI_FILE"; then
  echo 'OK: OpenAI skill exactly matches the reviewed adaptation.'
else
  result=$?
  if [[ "$result" -ne 1 ]]; then
    echo "error: comparison failed (status $result)." >&2
    exit "$result"
  fi
  echo 'DRIFT: unreviewed OpenAI skill or trigger change.' >&2
  exit 1
fi
