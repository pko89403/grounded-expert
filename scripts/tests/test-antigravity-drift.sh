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

# Case 2: Claude-only tool names in the Antigravity copy must fail the guard.
expect_guard_fail() {
  local dir="$WORK/leak$1"
  copy_tree "$dir"
  printf '\n%s\n' "$2" >> "$dir/hosts/antigravity/SKILL.md"
  local out
  if out="$("$dir/scripts/check-antigravity-drift.sh" 2>&1)"; then
    echo "FAIL: accepted Claude-only text: $2" >&2
    exit 1
  fi
  grep -q 'CLAUDE TOKEN' <<< "$out" || { echo "FAIL: rejected, but not by the token guard: $2" >&2; echo "$out" >&2; exit 1; }
  echo "PASS: rejected: $2"
}
expect_guard_fail 1 '- Fetch pages with WebFetch.'
expect_guard_fail 2 'Use Agent to start the lookup.'
expect_guard_fail 3 'Call Agent(prompt) once.'
expect_guard_fail 4 'If the Agent call fails, say so.'
expect_guard_fail 5 'Load it with the Skill tool.'

# Case 3: ordinary lowercase words must pass when added to both files alike.
copy_tree "$WORK/plain"
for f in plugin/SKILL.md hosts/antigravity/SKILL.md; do
  printf '\n%s\n' 'Here the agent decides which subagent Skills to load.' >> "$WORK/plain/$f"
done
"$WORK/plain/scripts/check-antigravity-drift.sh" > /dev/null
echo "PASS: lowercase agent/subagent and Skills accepted"
