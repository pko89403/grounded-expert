#!/usr/bin/env bash
# Fails if hosts/antigravity/SKILL.md and plugin/SKILL.md differ anywhere
# other than the known host-specific tokens below.
# Usage: scripts/check-antigravity-drift.sh   (from any directory)
set -euo pipefail

cd "$(dirname "$0")/.."
CLAUDE_FILE=plugin/SKILL.md
AG_FILE=hosts/antigravity/SKILL.md

for f in "$CLAUDE_FILE" "$AG_FILE"; do
  [ -f "$f" ] || { echo "missing: $f" >&2; exit 1; }
done

# Each host's tokens map to the same placeholder. Keep the two lists in step:
# the Nth rule of one list pairs with the Nth rule of the other.
# read -d '' (not $(cat <<EOF)): bash 3.2 on macOS mis-parses ' inside $( ).
read -r -d '' CLAUDE_RULES <<'EOF' || true
s|Claude Code's Agent tool plus WebSearch/WebFetch|@SPAWN_TOOL@ plus @WEB_TOOLS@|
s|with the Agent tool$|with @SPAWN_TOOL@|
s|Before calling Agent,|Before calling @SPAWN_TOOL@,|
s|`subagent_type: "general-purpose"`|@NEW_SUBAGENT@|
s|via WebSearch/WebFetch|via @WEB_TOOLS@|
s|`\${CLAUDE_PROJECT_DIR}/\.claude/grounded-expert/reference/<domain>\.md`|@REF_PATH@|
s|unless WebFetch actually|unless @FETCH_TOOL@ actually|
EOF

read -r -d '' AG_RULES <<'EOF' || true
s|Antigravity's `invoke_subagent` tool plus the host's web search and URL-fetch tools|@SPAWN_TOOL@ plus @WEB_TOOLS@|
s|with `invoke_subagent`$|with @SPAWN_TOOL@|
s|Before calling `invoke_subagent`,|Before calling @SPAWN_TOOL@,|
s|`invoke_subagent` and the built-in subagent type `self` — Antigravity's docs say `self` shares this agent's system instructions and toolsets, so it is expected, but not yet verified, to have the same web search and URL-fetch tools, whereas `research` is scoped to codebase exploration. Because `self` also inherits this skill, tell it in the prompt not to invoke this skill and not to call `invoke_subagent` itself, but to do the lookups directly. If it reports that it has no web search or URL-fetch tool, don't answer from memory: tell the user the answer is not externally verified —|@NEW_SUBAGENT@|
s|via the host's web search and URL-fetch tools|via @WEB_TOOLS@|
s|`\.agents/grounded-expert/reference/<domain>\.md` in the workspace root (this skill's own convention, not an Antigravity-defined location)|@REF_PATH@|
s|unless the host's URL-fetch tool actually|unless @FETCH_TOOL@ actually|
EOF

if diff -u --label "$CLAUDE_FILE (normalized)" --label "$AG_FILE (normalized)" \
    <(sed -e "$CLAUDE_RULES" "$CLAUDE_FILE") \
    <(sed -e "$AG_RULES" "$AG_FILE"); then
  echo "OK: $AG_FILE matches $CLAUDE_FILE except for host-specific tokens."
else
  echo "DRIFT: the two SKILL.md files differ outside host-specific tokens." >&2
  echo "Apply the same procedure change to both files, or update the rules in $0." >&2
  exit 1
fi
