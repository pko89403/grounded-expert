# OpenAI evaluation

Status: **experimental; behavioral release gate not passed**. A correct factual
answer, successful installation, or schema validation does not prove independent
research. This document separates those claims.

## Current contract

The OpenAI skill preserves the canonical `<output-contract>` block byte for byte,
including claim-table layout, primary publishers, source-copy tags, the
`(no primary source)` marker and disconfirming-search URL syntax. Parent findings
and evidence receipts stay in a separate progress/evidence channel before final
handoff. Failure labels keep the canonical first-line placement and exceptions.
The child prompt also states the host's quotation budget explicitly.

These are instructions, not enforced runtime guarantees. The package remains
experimental until the behavioral release gate below is met. Use a checkout of
`main` containing `hosts/openai/`; release tags through `v0.3.0` do not contain it.
The package has not been submitted to the public Plugins Directory.

## Scope and environment

Local smoke checks on 2026-10-22 used Codex CLI 0.162.1 and an already-present
0.163.0 binary, the installed local marketplace package, ephemeral sessions, an
isolated empty Git workspace, and a read-only agent sandbox. Existing default
model/settings were retained; this is not a controlled model/version benchmark.
No paid API service, external account, or production system was added or changed.
The temporary package was refreshed after skill edits. Canonical `plugin/` and
its eval cases were not changed.

Discovery/install smoke on 2026-10-25, Codex CLI 0.162.1: with both catalogs
present, the registered local marketplace selected `./hosts/openai`, not
`./plugin`. The installed manifest/privacy URL and skill matched the checkout
used in that run. This verifies one CLI/local-checkout path, not every host or
the current revision's runtime behavior. The temporary install and marketplace
were removed afterward.

## Observed installed-package behavior

These are individual smoke runs, not repeated full-suite scores. Intermediate
revisions are included to show what failed; they do not validate the final file.
The eight historical runs below predate the current output contract. Their
sanitized event excerpts, thread IDs, final mode-claim lines and original trace
SHA-256 anchors are in [the evidence snapshot](evidence/openai-smoke-2026-10-22.json).
The hashes identify retained private local traces; they are not a public copy of
those traces or proof that unrecorded child execution occurred.

| Case / revision | Observed evidence | Verdict |
|---|---|---|
| Python dict, quick, original port, 0.162.1 | Official Python page opened; correct 3.7 conclusion. Final cited a different, unopened URL and quoted 26 words. Only empty-recipient waits, no recorded successful spawn. | Factual answer supported; evidence handoff and independence not accepted. |
| Python dict, quick, first runtime correction, 0.162.1 | Full skill read, but no recorded page open or spawn; answer claimed independent retrieval. | Fail to substantiate the claimed workflow. |
| JS array length, implicit non-trigger, 0.162.1 | Returned `3`; no skill read, web activity, or collaboration events. | Pass for this one overtrigger smoke case only. |
| HTTP redirects, standard, delegation feature disabled, 0.162.1 | Opened RFC, curl maintainer docs and a WebKit issue; opposing searches recorded. Still claimed a fresh-context child; no recorded spawn. | Retrieval exercised; direct-mode fallback not accepted. |
| Current policy, standard, native web disabled and other retrieval prohibited, 0.162.1 | No source retrieval; explicitly refused external verification and gave no invented citation. Also claimed a child checked availability, without a recorded spawn. | Abstention passed; delegation reporting failed. |
| Python dict, quick, evidence-receipt revision, 0.162.1 | Parent opened the final cited Python page; correct conclusion and explicit quick-mode search omission. Still claimed independence and quoted 26 words. | URL visibility improved in this run; independence and quotation limit not accepted. |
| HTTP redirects, standard, evidence-receipt revision, 0.163.0 | Parent opened RFC/errata, curl docs and Go source; opposing query recorded; tags retained. Final still claimed fresh-context delegation with no recorded collaboration event. | Research supported; independent-workflow claim not accepted. |
| Python dict, quick, final explicit quote-budget revision, 0.163.0 | Parent opened Python docs and used an INFERRED paraphrase without direct quotation, but cited a different URL. Still reported independent lookup without a recorded successful spawn. | Quotation issue absent in this one run; exact-link provenance and independence still not accepted. |

The JSONL streams sometimes contain a completed event shaped like:

```json
{"type":"collab_tool_call","tool":"wait","receiver_thread_ids":[],"agents_states":{},"status":"completed"}
```

That is not evidence that a child was created. The streams did not establish
successful spawn/child identity or child web retrieval. This may involve host
tool availability or trace visibility; it does **not** prove where the failure
originates. Until independently correlated records are available, do not score
the independence claim as a pass. Prompt instructions alone did not reliably
remove these unsupported claims in these runs.

Explicit plugin invocation also emitted a main-prompt context truncation warning
in this configured environment. The agent then read the entire installed
`SKILL.md` with its file tool. Those runs therefore exercise the full instructions
but do not certify clean automatic prompt injection. Plugin packaging validation
does not resolve this host-context limitation.

## Deterministic checks

Run `python3 -m unittest discover -s scripts/tests -v` for the drift, package and
host-contract suites, and `python3 -I tools/check_quotes.py --self-test` for the
upstream checker. The suites cover temporary-copy drift/tool/cleanup failures,
JSON/resource validation, exact contract preservation, Korean answers, secondary
source and copy tags, source floors, no-web labels and the final-line grammar.

`scripts/check-openai-drift.sh` applies the reviewed contextual adaptation to a
temporary canonical copy without fuzzy matching, then compares the whole host
file, including its description. Review the patch itself when regenerating it;
deleted-line counts cannot establish semantic equivalence. The package checker
validates offline JSON/resources, not the entire portable schema. CI runs these
checks and ShellCheck; passing them does not establish installed-host behavior.

## Reproduce safely

Inspect existing plugin/marketplace state first; do not overwrite or uninstall a
user's existing installation. In an environment where this package is absent:

```bash
codex --version
codex plugin list --json
codex plugin marketplace add /absolute/path/to/grounded-expert --json
codex plugin add grounded-expert@grounded-expert --json
EVAL_DIR="$(mktemp -d "${TMPDIR:-/tmp}/grounded-expert-eval.XXXXXX")"
git -C "$EVAL_DIR" init -q
cd "$EVAL_DIR"
codex exec --ephemeral --json -s read-only -c 'web_search="live"' \
  -o answer.md \
  'Use installed $grounded-expert:grounded-expert at quick level. Python dict insertion order became a language guarantee in Python 3.6 or 3.7? Verify one official source, answer briefly. Do not modify any files.' \
  > trace.jsonl 2> diagnostics.log
```

Inspect the final answer **and** completed tool events. Confirm a real child
identity, no-history request only if supported, opened URLs, short matching
excerpts, tags and honest level/mode reporting. An empty wait is not a spawn;
search results alone are not opened evidence. When finished, remove only the
temporary installation/marketplace added for this evaluation.

For standard, use the HTTP redirect question in the table and request both RFC
and independently originated maintainer evidence. Repeat with
`--disable multi_agent` for the direct-mode case. For no-web, use
`-c 'web_search="disabled"'` and explicitly forbid shell-network, browser and MCP
retrieval fallbacks; expect external non-verification, not a current factual answer.
For implicit non-triggering, ask only for the length of `[10,20,30]` without naming
the skill. Agent runs use real account usage; they are not part of lightweight CI.

## Remaining gate

- Repeat quick/standard and capability-fallback cases until trace and final
  claims agree; resolve or explicitly constrain the host trace/creation gap.
- Evaluate thorough concurrency/recursion behavior and multiple explicit/implicit
  trigger and non-trigger cases. No full trigger benchmark was run here.
- Run ChatGPT desktop discovery, installation and behavior with authorized access.
  Computer-use access to that app was blocked during this evaluation; no workaround
  or end-to-end ChatGPT success is claimed.
- Rerun Claude evals only under its existing contribution gate when its package,
  descriptions, eval cases or graders change; OpenAI checks are not a substitute.

The read-only subprocesses also failed the local user's notification command.
That sandbox/configuration issue is separate from research behavior; no notification
settings were changed. Raw traces may contain local paths/configuration and are
kept as local test artifacts rather than committed to this public repository.

Packaging and capability references: [OpenAI plugin build guide](https://developers.openai.com/plugins/build/plugins),
[ChatGPT Work subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
These describe host support, not the observed success of this particular package.
