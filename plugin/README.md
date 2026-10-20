# grounded-expert

A Claude Code skill that answers domain questions by having a subagent actually
retrieve primary sources (official specs, docs, papers, standards) in real time
and check its own claims against them, instead of role-playing an expert persona
from memory.

## What it does

When a question needs domain-specific factual accuracy, or you ask for an expert
opinion or review, the skill:

1. Pins down the domain, the exact question, and a level (quick / standard /
   thorough).
2. Decides which source types a real expert in that domain would cite.
3. Spawns a subagent that looks those sources up with WebSearch/WebFetch, tags
   every claim EXTRACTED (with the exact quoted text) or INFERRED, and runs a
   self-critique, including a search for disconfirming evidence on standard and
   thorough.
4. Hands the answer back with its citations and tags, plus what remains
   uncertain.

## What it runs and fetches

- No hooks, no MCP servers, no bundled scripts, and no credentials.
- The subagent makes live web requests (WebSearch/WebFetch) to the sources it
  cites, so each invocation is real API usage. `thorough` runs extra subagents
  in parallel.
- Optionally, it saves the source types that worked for a domain to a
  project-local note under `.claude/grounded-expert/reference/`, only when the
  same domain comes up repeatedly.

Full documentation, translations (한국어, 日本語, 简体中文), and contribution
guidelines: https://github.com/pko89403/grounded-expert

## License

MIT. See [LICENSE](LICENSE).
