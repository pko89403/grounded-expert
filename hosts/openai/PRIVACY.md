# Privacy: OpenAI host package

Last updated: 2026-10-25

This community-maintained package contains skill instructions. It bundles no
MCP server, hooks, runtime collection script or author-operated backend. It does
not add an automatic telemetry destination for the maintainer.

The host processes your question and the context supplied to its agents. When
available and permitted, host web tools send search queries to their search
provider and request pages from cited sites. Host logs, conversation retention,
account/workspace settings and connected-tool permissions are controlled by the
host and its providers, not this package. Consult those providers' terms,
privacy policies and settings; these instructions cannot override them. Avoid
including secrets or personal data in questions sent for external lookup.

For repeated domains, the skill may save a short local source-type note under
`.agents/grounded-expert/reference/` in the current project, shared with the
Antigravity host. Notes should contain source types and rationale, not sensitive
questions. The project controls whether notes are versioned or ignored; deleting
a note does not delete host conversation logs. This repo ignores that notes path,
not the OpenAI marketplace metadata.

If you choose to report a problem on GitHub, only include information you intend
to share publicly. The package does not submit those reports automatically.
Contact: https://github.com/pko89403/grounded-expert/issues
