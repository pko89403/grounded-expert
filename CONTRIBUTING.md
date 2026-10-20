# Contributing

## Before opening a PR

The plugin lives in `plugin/`; the repository root holds the marketplace
manifest and the docs.

1. `claude plugin validate --strict plugin` (the plugin) and
   `claude plugin validate --strict .` (the marketplace) — manifest/schema check. Required, but
   not sufficient on its own: it validates structure only. It does not run
   any eval case and cannot catch a trigger-matching or behavior regression.
2. If you changed `plugin/SKILL.md`'s frontmatter `description`, any eval case, or
   any grader: run the real suite —
   `claude plugin eval plugin --judge-model opus` (never sonnet/haiku for
   grading). Run the **full case suite**, using each case's own `runs:`
   count from its `prompt.md` frontmatter — do not judge a change on a
   single case or a single run.
3. Compare with/without scores per case against the last known-good run. A
   case regressing blocks the PR even if `validate` succeeded — a clean
   `validate` and correct behavior are not the same claim.

## Branching and releases

- Trunk-based: `main` is the trunk. Work on a short-lived branch named
  `feat/…`, `fix/…`, `docs/…` or `chore/…` and open a PR to `main`.
- PRs are squash-merged, and the squash commit uses the PR title, so the
  title must follow [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat: …`, `fix: …`, `docs: …`, `chore: …`; `feat!:` for breaking changes).
  release-please reads these titles to pick the next version and write
  `CHANGELOG.md`.
- The `validate` CI check (both `claude plugin validate --strict` commands
  above) must succeed before merge. The link check runs too but does not block
  yet.
- A change to `plugin/SKILL.md`, an eval case or a grader still needs the
  eval evidence from "Before opening a PR" in the PR description. CI does not
  run the eval suite.
- Releases come only from release-please PRs. The owner merges the release PR;
  release-please then tags `vX.Y.Z` and creates the GitHub release. The owner
  then publishes that tag in the plugin directory portal by hand (auto-publish
  stays off).

## Adding an eval case

Follow the existing schema: `plugin/evals/<case>/prompt.md` (frontmatter:
`max_turns`, `timeout_seconds`, `allowed_tools`, `runs`) plus
`plugin/evals/<case>/graders/*.md`.

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
