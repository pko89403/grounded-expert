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
   `claude plugin eval plugin --judge-model opus --allow-tools WebFetch WebSearch`
   (never sonnet/haiku for grading). The `--allow-tools` grant is required:
   without it the run removes WebFetch and WebSearch, every grounded case
   answers with no source opened, and the scores are meaningless.
   Run the **full case suite**, using each case's own `runs:`
   count from its `prompt.md` frontmatter — do not judge a change on a
   single case or a single run.
3. Compare with/without scores per case against the last known-good run. A
   case regressing blocks the PR even if `validate` succeeded — a clean
   `validate` and correct behavior are not the same claim.
4. If `plugin/SKILL.md` or the OpenAI host copy changes, run
   `scripts/check-openai-drift.sh` and
   `python3 -m unittest discover -s scripts/tests -v`. The guard applies the
   explicitly reviewed `scripts/openai-skill.patch` to a temporary source copy
   and compares the entire result, including trigger descriptions. It never
   edits `plugin/`. If a source or host adaptation changes, review and regenerate
   the patch with `diff -u --label plugin/SKILL.md --label
   hosts/openai/skills/grounded-expert/SKILL.md plugin/SKILL.md
   hosts/openai/skills/grounded-expert/SKILL.md > scripts/openai-skill.patch`
   (diff exit 1 means differences, not a generation failure). Updating this
   allowlist is not evidence that a behavior change is safe.
   **The patch diff itself must be reviewed** whenever it is regenerated. A
   missing shared procedure can otherwise be absorbed as an allowed deletion.
   Inspect every deleted canonical line and retained context; do not use `-U0`.
   CI prints deleted-line counts and their change against the PR base. A lower
   count is not proof of semantic equivalence either. `.gitattributes` exempts
   this patch's required blank context markers from trailing-space checking only.
5. If you changed `tools/` or the `<output-contract>` block in
   `plugin/SKILL.md`: `python3 tools/check_quotes.py --self-test`. CI runs it too.

## OpenAI host changes

Keep `plugin/` and its Claude eval gate unchanged for an OpenAI-only change.
Run `python3 scripts/validate_openai_package.py` and the checks above, then follow
[OpenAI evaluation](docs/openai-evaluation.md). An OpenAI description change
requires repeated explicit/implicit trigger and non-trigger cases; a body
change requires the affected behavior cases. Do not infer OpenAI behavior from
Claude scores, metadata validation, or one correct factual answer. Check the
tool trace for successful child creation, opened URLs, disconfirming searches,
and honest capability fallbacks. Record failures and missing host coverage.
The package checker validates offline JSON/resources, not the full portable
schema. The OpenAI CI path filter
covers its manifest, marketplace, license and privacy resources too.

Keep the canonical `<output-contract>` block byte-identical in the OpenAI copy.
The host tests compare it and exercise the upstream quote checker with Korean
answers, secondary-source tags, document aliases and failure labels. Parent
validation notes belong in a separate progress message before handoff; appending
an evidence receipt after `Disconfirming search:` breaks the contract. Changes
to `tools/` also trigger the OpenAI checks, including the upstream self-test.

OpenAI's package version is independent of `plugin/` and remains experimental.
The current release-please configuration does not bump it. Maintainers must
review/update that version explicitly before publishing a changed OpenAI package;
let release-please manage generated CHANGELOG sections. Reference notes share the
Antigravity `.agents/grounded-expert/reference/` path; existing Claude notes are
not migrated or merged automatically.

## Branching and releases

- Trunk-based: `main` is the trunk. Work on a short-lived branch named
  `feat/…`, `fix/…`, `docs/…` or `chore/…` and open a PR to `main`.
- PRs are squash-merged, and the squash commit uses the PR title, so the
  title must follow [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat: …`, `fix: …`, `docs: …`, `chore: …`; `feat!:` for breaking changes).
  release-please reads these titles to pick the next version and write
  `CHANGELOG.md`.
- The squash commit message is the PR body, and release-please parses it too.
  A body paragraph that starts with a commit type (`fix:`, `feat:`, `chore:`
  and so on) is read as an extra commit. A `BREAKING CHANGE:` line is read as
  a breaking change. Either one can add a changelog entry or bump the version,
  so don't start body lines that way unless you mean it.
- Only commits that touch `plugin/` trigger a release. A change to the root
  `.claude-plugin/marketplace.json` or the docs alone does not. If such a
  change must ship, include a `plugin/` change in the same PR, or the owner
  cuts the release by hand.
- The `validate` CI check (both `claude plugin validate --strict` commands
  above) must succeed before merge. It runs on every PR, but branch rules
  will only enforce it after the PR that adds the workflow is merged and the
  check is marked as required. The link check runs too but does not block
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

## Checking quotes

`tools/check_quotes.py ANSWER` checks one final answer against the output
contract in `plugin/SKILL.md`: table layout, tags, primary hosts, source floor,
the last line, and every quote against the page text in `tools/fixtures/`. It
is a report for reviewers and is not part of the eval score. Verdicts per row:
`OK`, `UNVERIFIED` (no fixture for the URL, or the quote lies outside an
excerpt) and `INVALID`. A fixture is a `.txt` file with one or more `url:` lines
(the first is canonical, the others are aliases), `scope: excerpt` or `scope:
full`, `source:` and `licence:` lines, a `---` line and the page text. Commit
only small excerpts together with their licence; keep full pages local and pass
them with `--fixtures DIR`.

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
