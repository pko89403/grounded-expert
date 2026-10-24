# Changelog

Version sections are written by [release-please](https://github.com/googleapis/release-please)
from the Conventional Commit messages that land on `main`. Don't hand-edit
them on `main`; to change an entry, edit the open release PR before it is
merged. The `0.1.0` entry below was written by hand.

The project stays in `0.x` (see README Versioning): a breaking change
(`feat!:` or a `BREAKING CHANGE:` footer) bumps the minor version, not the
major one.

## [0.1.0] - initial public release

### Added
- `grounded-expert` skill: no-persona subagent procedure (pin domain + level,
  decide source types before searching, spawn subagent with a source-count
  floor and a self-critique/disconfirming-search step, hand off answer with
  EXTRACTED/INFERRED-tagged citations verbatim).
- Levels: quick / standard (default) / thorough.
- Eval suite: dgm-taxonomy-tension, http-redirect-method, python-dict-order,
  gdpr-pseudonymization, js-array-length (should-not-fire case).
- README, MIT LICENSE, plugin manifest metadata (homepage, repository,
  license).

### Fixed
- Skill not firing on quick-phrased or spec-check-phrased requests: the
  frontmatter `description` was missing those trigger signals.
- `EXTRACTED` citation tag's footnote-marker exception narrowed so it only
  strips a trailing footnote marker, not any other character mismatch.
- Overtrigger risk: added a trivial-question skip condition to the
  description, then fixed a regression that same addition caused (an
  unrelated eval case's quick-phrased prompt started skipping the skill
  again) by reordering the clause and narrowing the skip condition to
  concrete in-context-only examples. Verified via a full eval-suite,
  multi-run re-check before merging, not a single case or run.
