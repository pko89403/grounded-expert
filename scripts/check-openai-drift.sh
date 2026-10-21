#!/usr/bin/env bash
# Fails if the Claude Code and OpenAI skill copies differ anywhere other than
# the host-specific tool and workspace-path tokens below.
set -euo pipefail

cd "$(dirname "$0")/.."
CLAUDE_FILE=plugin/SKILL.md
OPENAI_FILE=hosts/openai/skills/grounded-expert/SKILL.md

for file in "$CLAUDE_FILE" "$OPENAI_FILE"; do
  [[ -f "$file" ]] || { echo "missing: $file" >&2; exit 1; }
done

read -r -d '' CLAUDE_RULES <<'EOF' || true
s|Claude Code's Agent tool plus WebSearch/WebFetch|@SPAWN_TOOL@ plus @WEB_TOOLS@|
s|with the Agent tool$|with @SPAWN_TOOL@|
s|Before calling Agent,|Before calling @SPAWN_TOOL@,|
s|`subagent_type: "general-purpose"`|@NEW_SUBAGENT@|
s|via WebSearch/WebFetch|via @WEB_TOOLS@|
s|`\${CLAUDE_PROJECT_DIR}/\.claude/grounded-expert/reference/<domain>\.md`|@REF_PATH@|
s|unless WebFetch actually|unless @FETCH_TOOL@ actually|
EOF

read -r -d '' OPENAI_RULES <<'EOF' || true
s|the OpenAI host's independent subagent tool plus its web search and page-opening tools|@SPAWN_TOOL@ plus @WEB_TOOLS@|
s|with the OpenAI host's independent subagent tool$|with @SPAWN_TOOL@|
s|Before calling the independent subagent tool,|Before calling @SPAWN_TOOL@,|
s|`collaboration.spawn_agent` with `fork_turns: "none"` in Codex, or the equivalent independent/no-history delegation option in ChatGPT|@NEW_SUBAGENT@|
s|via the host's web search and page-opening tools|via @WEB_TOOLS@|
s|`\.agents/grounded-expert/reference/<domain>\.md` in the workspace root|@REF_PATH@|
s|unless the host's page-opening tool actually|unless @FETCH_TOOL@ actually|
EOF

normalize_claude_frontmatter() {
  awk '
    /^description: / {
      print "description: @DESCRIPTION@"
      next
    }
    { print }
  ' "$CLAUDE_FILE"
}

normalize_openai_frontmatter() {
  awk '
    $0 == "description: >-" {
      getline
      print "description: @DESCRIPTION@"
      next
    }
    { print }
  ' "$OPENAI_FILE"
}

if diff -u --label "$CLAUDE_FILE (normalized)" --label "$OPENAI_FILE (normalized)" \
    <(normalize_claude_frontmatter | sed -e "$CLAUDE_RULES") \
    <(normalize_openai_frontmatter | sed -e "$OPENAI_RULES"); then
  echo "OK: $OPENAI_FILE matches $CLAUDE_FILE except for host-specific tokens."
else
  echo "DRIFT: the two SKILL.md files differ outside host-specific tokens." >&2
  echo "Apply the same procedure change to both files, or update this check." >&2
  exit 1
fi
