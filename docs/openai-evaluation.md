# OpenAI evaluation

Status: **experimental; behavioral release gate not passed**. A correct factual
answer, successful installation, or schema validation does not prove independent
research. This document separates those claims.

## Scope and environment

Local smoke checks on 2026-10-22 used Codex CLI 0.162.1 and an already-present
0.163.0 binary, the installed local marketplace package, ephemeral sessions, an
isolated empty Git workspace, and a read-only agent sandbox. Existing default
model/settings were retained; this is not a controlled model/version benchmark.
No paid API service, external account, or production system was added or changed.
The temporary package was refreshed after skill edits. Canonical `plugin/` and
its eval cases were not changed.

## Observed installed-package behavior

These are individual smoke runs, not repeated full-suite scores. Intermediate
revisions are included to show what failed; they do not validate the final file.

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

## Changes prompted by these observations

- Use actual exposed delegation schemas, not one assumed namespace or parameter.
  Require a successful spawn/child identity before waiting or reporting delegation;
  handle ID-less mailbox waiting without inventing an ID.
- Declare direct research when delegation fails and external non-verification
  when retrieval is unavailable. Never change host models/permissions to force it.
- Request child evidence receipts. If child records are unavailable, the parent
  opens the supporting passage and reports the visibility limit.
- Check actual opened URLs, exact excerpts and aggregate quote budgets before
  handoff. The final instruction makes a 25-word/source default explicit; that
  instruction is not an enforced runtime guarantee.
- Distinguish independent provenance from mirrors/repeated authorities. Report a
  source shortfall rather than inventing a second source; allow supported cited
  paraphrases under INFERRED without pretending corroboration.
- Bound thorough fan-out to the host limit; prohibit recursive research children.

## Deterministic checks

The drift guard previously discarded the whole description and normalized a
small list of replacements. It could miss changes to trigger metadata. It now
applies `scripts/openai-skill.patch` to a temporary canonical copy, with no fuzzy
matching, then compares the complete expected host file. The patch is an explicit
reviewed adaptation, not an automatic approval of behavior changes.

Seven stdlib regression tests exercise the guard with real temporary copies:
valid adaptation without source mutation, host description change, canonical
description change, host procedure change, source-only procedure change, shared
change outside adaptation, and missing patch. All seven passed locally.

Also passed: skill `quick_validate.py`, the drift guard, `bash -n`,
`git diff --check`, and byte comparison of canonical `plugin/` against the base.
The GitHub workflow runs the guard and regression tests on Ubuntu; local results
alone are not a claim that remote CI passed. ShellCheck was unavailable.

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
