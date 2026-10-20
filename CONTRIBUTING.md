# Contributing

## Before opening a PR

1. `claude plugin validate --strict .` — manifest/schema check. Required, but
   not sufficient on its own: it validates structure only. It does not run
   any eval case and cannot catch a trigger-matching or behavior regression.
2. If you changed `SKILL.md`'s frontmatter `description`, any eval case, or
   any grader: run the real suite —
   `claude plugin eval . --judge-model opus` (never sonnet/haiku for
   grading). Run the **full case suite**, using each case's own `runs:`
   count from its `prompt.md` frontmatter — do not judge a change on a
   single case or a single run.
3. Compare with/without scores per case against the last known-good run. A
   case regressing blocks the PR even if `validate` passed — `validate`
   passing and the behavior being correct are not the same claim.

## Adding an eval case

Follow the existing schema: `evals/<case>/prompt.md` (frontmatter:
`max_turns`, `timeout_seconds`, `allowed_tools`, `runs`) plus
`evals/<case>/graders/*.md`.

## Why this is strict

`description` in `SKILL.md`'s frontmatter is the *only* input Claude Code
uses for automatic skill-trigger matching — the body (Levels table, "When to
use this" conditions, procedure) is invisible to that decision. A one-sentence
addition to `description` once fixed a real overtrigger gap and, in the same
change, silently reintroduced a previously-fixed undertrigger bug in an
unrelated eval case — not because the sentence was factually wrong, but
because of where it sat relative to another clause. `validate --strict` and
a single-case spot-check both passed on that change; the regression only
showed up once the full case suite was re-run with multiple runs per case.
Treat any `description` edit as the highest-risk change in this repo, and
verify it at that level every time, not just the first time.
