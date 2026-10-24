#!/usr/bin/env bash
# Self-test for scripts/check-antigravity-drift.sh: the real files pass, and a
# Claude-only tool name in the Antigravity copy fails with the token guard.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd -P)"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/ag-drift-test.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

copy_tree() {
  mkdir -p "$1/scripts" "$1/plugin" "$1/hosts/antigravity"
  cp "$REPO_DIR/scripts/check-antigravity-drift.sh" "$1/scripts/"
  cp "$REPO_DIR/plugin/SKILL.md" "$1/plugin/"
  cp "$REPO_DIR/hosts/antigravity/SKILL.md" "$1/hosts/antigravity/"
}

# Case 1: unmodified files must pass.
copy_tree "$WORK/clean"
"$WORK/clean/scripts/check-antigravity-drift.sh" > /dev/null
echo "PASS: clean copy accepted"

# Case 2: a Claude-only tool name in the Antigravity copy must fail the guard.
copy_tree "$WORK/leak"
printf '\n- Fetch pages with WebFetch.\n' >> "$WORK/leak/hosts/antigravity/SKILL.md"
if out="$("$WORK/leak/scripts/check-antigravity-drift.sh" 2>&1)"; then
  echo "FAIL: WebFetch in the Antigravity copy was accepted" >&2
  exit 1
fi
grep -q 'CLAUDE TOKEN' <<< "$out" || { echo "FAIL: rejected, but not by the token guard:" >&2; echo "$out" >&2; exit 1; }
echo "PASS: Claude-only token rejected"
