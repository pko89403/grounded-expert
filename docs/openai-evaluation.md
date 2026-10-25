# OpenAI evaluation

Status: **experimental; behavioral release gate not passed**. A correct factual
answer, successful installation, or schema validation does not prove independent
research. This document separates those claims.

## 2026-10-25 v0.2.0 main synchronization

Rebased on main's v0.2.0 output-contract and quote-checker changes. The canonical
`plugin/`, Antigravity host, `tools/` and generated CHANGELOG remain unchanged.
The OpenAI copy preserves the complete `<output-contract>` block byte for byte:
claim-table layout, primary-publisher list, `INFERRED (via <host>)` and
`INFERRED (figure N)` variants, language rules and exact final-line forms.
Parent findings and evidence receipts must stay outside the final answer, in a
separate progress/evidence channel before handoff. Failure labels retain the
canonical first-line placement and the no-level/no-source exceptions.

The adaptation still deletes **8 canonical lines**. Six new host-contract tests
exercise exact block preservation and the upstream checker, bringing the local
deterministic suite to **24 passing tests**. The upstream quote-checker self-test
also passes; OpenAI CI now runs it and watches `tools/` changes. These are
deterministic checks, not new installed-host trigger, delegation or ChatGPT
runtime results. The behavioral release gate remains unpassed.

## Earlier 2026-10-25 review response (before v0.2.0)

This historical revision predates the output contract above. Rebased on the
then-current main, preserving Antigravity support and release-please's
generated CHANGELOG unchanged. The canonical Claude package is unchanged from
that base. The OpenAI copy now preserves canonical step 3/4's source floors,
EXTRACTED matching-quote validity, multiple-source-only INFERRED meaning, verbatim
child handoff and three fixed failure labels. Single-source paraphrases without
matching quotes are not INFERRED: they are omitted or `not confirmed`. Parent
validation notes remain separate; a noncompliant child response requires a child
revision or withholding, never silent parent repair. The canonical fetch-once
instruction is retained; the previous extra-fetch permission was removed.

Description metadata restores the Korean verification/quick trigger examples
and makes delegation conditional. These are source corrections, **not** new
passing trigger/runtime scores. Repeated trigger and updated workflow execution
remain part of the behavioral release gate below.

The regenerated adaptation now retains context and deletes **8 canonical lines,
down from 14** in the reviewed revision. None of the tag-definition, invalid-tag,
verbatim-handoff or failure-branch lines is deleted by the patch. CONTRIBUTING
requires review of the patch diff itself, and CI reports deletion-count changes;
those counts cannot certify semantic equivalence. Local deterministic coverage
is now **18 passing tests**: 11 drift/tool/cleanup cases and 7 package resource
cases. Both strict Claude manifest/marketplace validators also passed.

The new offline package checker validates JSON structure and referenced resources,
not the entire portable JSON Schema. CI watches manifest/marketplace/license
changes too, uses a distinct `openai-drift` job id and runs ShellCheck. ShellCheck
was absent from the local PATH during the earlier 2026-10-22 checks; that was a
historical local-environment limitation, not a claim that the script had no
ShellCheck findings or that a reviewer could not run it.

The public catalog does not contain this package. Use a checkout containing the
OpenAI host and register that **local** marketplace; do not install an older main
or release tag expecting these files. OpenAI privacy documentation is now
host-specific. Its manifest version is maintained separately; release-please
does not update the OpenAI package automatically.

Discovery/install smoke on 2026-10-25, Codex CLI 0.162.1: with both
`.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json` present,
the registered local marketplace selected `./hosts/openai`, not `./plugin`.
Installing that entry yielded the OpenAI manifest/privacy URL and a skill copy
byte-identical to this checkout. This verifies that one CLI/local-checkout path,
not precedence in every host or desktop runtime behavior. The temporary install
and marketplace were removed after the check.

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
The eight historical runs below predate the review corrections above. Their
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

## Initial hardening (superseded where noted above)

- Use actual exposed delegation schemas, not one assumed namespace or parameter.
  Require a successful spawn/child identity before waiting or reporting delegation;
  handle ID-less mailbox waiting without inventing an ID.
- Declare direct research when delegation fails and external non-verification
  when retrieval is unavailable. Never change host models/permissions to force it.
- Request child evidence receipts and disclose missing child tool records.
- Check actual opened URLs, exact excerpts and aggregate quote budgets before
  handoff. The final instruction makes a 25-word/source default explicit; that
  instruction is not an enforced runtime guarantee.
- Distinguish independent provenance from mirrors/repeated authorities. Report
  source shortfalls; the initial INFERRED paraphrase broadening was rejected in
  review and reverted to canonical semantics.
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
alone are not a claim that remote CI passed. ShellCheck was unavailable locally
on that original evaluation date; current CI runs it separately.

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
