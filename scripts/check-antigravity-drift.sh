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
# the Nth rule of one list pairs with the Nth rule of the other. The final
# delete rules drop Antigravity-only lines (the "Antigravity note:" paragraph
# plus its trailing blank line, and list item 7); on the Claude side they match
# nothing and only keep the lists paired.
# read -d '' (not $(cat <<EOF)): bash 3.2 on macOS mis-parses ' inside $( ).
read -r -d '' CLAUDE_RULES <<'EOF' || true
s|Claude Code's Agent tool plus WebSearch/WebFetch|@SPAWN_TOOL@ plus @WEB_TOOLS@|
s|with the Agent tool$|with @SPAWN_TOOL@|
s|`subagent_type: "grounded-expert:grounded-researcher"`, or `subagent_type: "general-purpose"` if that type is not found|@NEW_SUBAGENT@|
s|via WebSearch/WebFetch|via @WEB_TOOLS@|
s|`\${CLAUDE_PROJECT_DIR}/\.claude/grounded-expert/reference/<domain>\.md`|@REF_PATH@|
s|unless WebFetch actually|unless @FETCH_TOOL@ actually|
s|\. As a Claude Code plugin it calls .* not enforcement\.|@GOTCHA_TAIL@|
/^Antigravity note: /{N;d;}
/^7\. Antigravity only: /d
EOF

read -r -d '' AG_RULES <<'EOF' || true
s|Antigravity's `invoke_subagent` tool plus the host's web search and URL-fetch tools|@SPAWN_TOOL@ plus @WEB_TOOLS@|
s|with `invoke_subagent`$|with @SPAWN_TOOL@|
s|`invoke_subagent` and the built-in subagent type `self`|@NEW_SUBAGENT@|
s|via the host's web search and URL-fetch tools|via @WEB_TOOLS@|
s|`\.agents/grounded-expert/reference/<domain>\.md` in the workspace root (this skill's own convention, not an Antigravity-defined location)|@REF_PATH@|
s|unless the host's URL-fetch tool actually|unless @FETCH_TOOL@ actually|
s|, but nothing limits the subagent to them, so the step 3 tool rule is a prompt rule, not enforcement\. No separate MCP server or plugin component is needed at this scope\.|@GOTCHA_TAIL@|
/^Antigravity note: /{N;d;}
/^7\. Antigravity only: /d
EOF

# The diff below passes when a new sentence naming a Claude-only tool is copied
# verbatim into both files, so reject those names in the Antigravity file.
# Case-sensitive; Agent/Skill only as whole words, so "agent", "subagent" and
# "Skills" pass. POSIX classes instead of \b so GNU and BSD grep agree.
W='[^[:alnum:]_]'
CLAUDE_ONLY="WebSearch|WebFetch|general-purpose|subagent_type|CLAUDE_PROJECT_DIR|(^|$W)(Agent|Skill)($W|\$)"
if grep -nE "$CLAUDE_ONLY" "$AG_FILE" >&2; then
  echo "CLAUDE TOKEN: $AG_FILE uses the Claude Code-only names above; use the Antigravity equivalents." >&2
  exit 1
fi

if diff -u --label "$CLAUDE_FILE (normalized)" --label "$AG_FILE (normalized)" \
    <(sed -e "$CLAUDE_RULES" "$CLAUDE_FILE") \
    <(sed -e "$AG_RULES" "$AG_FILE"); then
  echo "OK: $AG_FILE matches $CLAUDE_FILE except for host-specific tokens."
else
  echo "DRIFT: the two SKILL.md files differ outside host-specific tokens." >&2
  echo "Apply the same procedure change to both files, or update the rules in $0." >&2
  exit 1
fi
