# Privacy policy: grounded-expert

Last updated: 2026-10-20

grounded-expert is a Claude Code plugin made of a single skill (instructions).
It has no hooks, no MCP servers, no bundled scripts, and no server operated by
the author.

## What it collects

Nothing. The plugin does not collect, store, or transmit personal data (names,
emails, addresses, account details) to the author or any service operated by
the author. It does not read credentials or environment variables.

## What leaves your machine

When the skill runs, Claude spawns a subagent that uses Claude's built-in
WebSearch and WebFetch tools:

- **Search queries** derived from your question are sent to the web search
  provider used by WebSearch.
- **Requests to source pages** (official docs, specs, papers, standards) are
  made by WebFetch to the sites it cites.

These requests go through Claude's own tools under your Claude account and are
governed by Anthropic's terms and privacy policy, and by the policies of the
sites visited. The plugin adds no other destination. Avoid putting sensitive
information in questions you want looked up on the web.

## What it stores

Optional, local only: when the same domain comes up repeatedly, the skill may
save a short note listing which source types were reliable to
`.claude/grounded-expert/reference/<domain>.md` inside your current project.
The note contains source types and a short rationale, not your questions or
personal data. You can delete it at any time.

## Retention

The author receives no data, so nothing is retained by the author.

## Children

The plugin is not intended for users under 18.

## Contact

Questions: open an issue at https://github.com/pko89403/grounded-expert/issues
