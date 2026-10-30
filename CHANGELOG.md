# Changelog

Version sections are written by [release-please](https://github.com/googleapis/release-please)
from the Conventional Commit messages that land on `main`. Don't hand-edit
them on `main`; to change an entry, edit the open release PR before it is
merged. The `0.1.0` entry below was written by hand.

The project stays in `0.x` (see README Versioning): a breaking change
(`feat!:` or a `BREAKING CHANGE:` footer) bumps the minor version, not the
major one.

## [0.6.0](https://github.com/pko89403/grounded-expert/compare/v0.5.0...v0.6.0) (2026-10-30)


### Features

* show a plan card and ask before starting the subagent ([#32](https://github.com/pko89403/grounded-expert/issues/32)) ([312db15](https://github.com/pko89403/grounded-expert/commit/312db15e3e8a535b4efaa0eea1d3a736818baae3))

## [0.5.0](https://github.com/pko89403/grounded-expert/compare/v0.4.0...v0.5.0) (2026-10-25)


### Features

* handle named-person persona requests and add reference-file fields ([#29](https://github.com/pko89403/grounded-expert/issues/29)) ([03eb6ba](https://github.com/pko89403/grounded-expert/commit/03eb6ba759852371a97987301e32c4d34340c0ab))

## [0.4.0](https://github.com/pko89403/grounded-expert/compare/v0.3.1...v0.4.0) (2026-10-25)


### Features

* limit the step 3 subagent to WebSearch/WebFetch with a plugin agent ([#27](https://github.com/pko89403/grounded-expert/issues/27)) ([9fabcb8](https://github.com/pko89403/grounded-expert/commit/9fabcb8d1ca490314f348a5b57d584260be07321))

## [0.3.1](https://github.com/pko89403/grounded-expert/compare/v0.3.0...v0.3.1) (2026-10-25)


### Bug Fixes

* restrict grounded subagent to web lookup tools ([#25](https://github.com/pko89403/grounded-expert/issues/25)) ([1fb6a16](https://github.com/pko89403/grounded-expert/commit/1fb6a1658a290eee82602eabd538ffd5b227c64f))

## [0.3.0](https://github.com/pko89403/grounded-expert/compare/v0.2.0...v0.3.0) (2026-10-25)


### Features

* **contract:** tag source copies, mark zero-primary levels, allow several disconfirming URLs ([#21](https://github.com/pko89403/grounded-expert/issues/21)) ([2ce0090](https://github.com/pko89403/grounded-expert/commit/2ce00901d8f3c14b95c64cb1f4eb27a838011cd3))

## [0.2.0](https://github.com/pko89403/grounded-expert/compare/v0.1.1...v0.2.0) (2026-10-25)


### Features

* add the claim-table output contract and quote checker ([#14](https://github.com/pko89403/grounded-expert/issues/14)) ([cc5bc85](https://github.com/pko89403/grounded-expert/commit/cc5bc8539c2e85cd0a6e9f395fee7af1f5bc7fdd))

## [0.1.1](https://github.com/pko89403/grounded-expert/compare/v0.1.0...v0.1.1) (2026-10-24)


### Bug Fixes

* only report subagent delegation after the Agent call returns ([#8](https://github.com/pko89403/grounded-expert/issues/8)) ([281c1af](https://github.com/pko89403/grounded-expert/commit/281c1af3d438e1f6614b848257d9fc2c16b369f5))

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
