<p align="center">
  <img src="assets/logo.svg" width="180" alt="grounded-expert logo: honey badger head in profile">
</p>

# grounded-expert

[![Release](https://img.shields.io/github/v/release/pko89403/grounded-expert)](https://github.com/pko89403/grounded-expert/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**English** | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

A Claude Code plugin that spawns a subagent to answer domain questions by
actually retrieving primary sources (official specs, docs, papers, standards)
in real time and checking its own claims against them — instead of
role-playing an expert persona from memory.

## Why

Handing a subagent a persona ("you are an expert in X") makes it answer from
parametric memory while playing the role, so it states wrong facts as
confidently as right ones. This plugin enforces the procedure a real expert
follows instead: look things up, cite what you found, and correct yourself
when you're wrong.

## Install

```
/plugin install grounded-expert --marketplace pko89403/grounded-expert
```

(Claude Code 2.1.275 or later adds this repo as a marketplace source and
walks you through confirming it and picking an install scope — not a silent
one-step install. For the shell form instead of the slash command,
`claude plugin install grounded-expert --marketplace pko89403/grounded-expert`
needs Claude Code 2.1.292 or later.)

For local development: `claude plugin marketplace add <path-to-this-repo>`,
then `claude plugin install grounded-expert@grounded-expert`.

## Use with Google Antigravity (experimental)

Antigravity support is community-maintained and not covered by the Claude Code
eval suite. It is not yet verified that the `self` subagent it spawns gets web
search and URL-fetch tools. If it does not, the skill is instructed to tell you
the answer is not externally verified instead of answering from memory.

```
git clone https://github.com/pko89403/grounded-expert.git
cd grounded-expert
git checkout <release-tag>   # pin a release so the link does not follow a moving working tree
scripts/install-antigravity.sh --global          # Antigravity App/IDE: ~/.gemini/config/skills/
scripts/install-antigravity.sh --global --cli    # Antigravity CLI: ~/.gemini/antigravity-cli/skills/
cd <your-project> && <clone>/scripts/install-antigravity.sh --workspace   # <project>/.agents/skills/
```

`hosts/antigravity/` first ships in the release after v0.1.0. Until that tag
exists, skip the `git checkout` line and stay on `main`.

The script symlinks `hosts/antigravity/` (not `plugin/`). Add `--uninstall` to
remove the link for the same mode. It never touches a real directory or a link
that points elsewhere. Skill locations follow
[Antigravity's skills docs](https://antigravity.google/docs/skills).

## Usage

The skill fires automatically when a question needs domain-specific factual
accuracy, or when explicitly asked for an expert opinion/review. You can also
invoke it directly:

```
/grounded-expert <question>
```

**Cost note:** each invocation spawns a real subagent that does live
WebSearch/WebFetch calls and (on `standard`/`thorough`) a disconfirming-search
step — this is real API usage, not a cached/local lookup. `thorough` spawns
additional parallel subagents on top of that. Running the eval suite
(`claude plugin eval`) also costs real money per run (judge model + agent
model both bill).

### Levels

Pick (or let it infer) one level per question, not per session:

| Level | Behavior |
|---|---|
| **quick** | 1 source, no disconfirming-evidence search, 1 critique round. |
| **standard** (default) | 2+ independent sources, EXTRACTED/INFERRED tagging, up to 2 critique rounds incl. 1 disconfirming-evidence search. |
| **thorough** | standard, plus one additional subagent per candidate source type in parallel, cross-checked. For safety/legal/money stakes. |

Trigger words: "대충/빨리" → quick, "꼼꼼히/전부 확인해서" or legal/safety stakes →
thorough, nothing specified → standard.

### Example

```
/grounded-expert HTTP 301로 리다이렉트되면 POST를 GET으로 바꿔도 되는지
RFC 기준으로 확인해줘.
```

The subagent retrieves RFC 9110/7231, quotes the relevant section, tags the
claim EXTRACTED or INFERRED, and reports what remains uncertain.

## Plugin structure

```
.claude-plugin/marketplace.json  marketplace manifest; lists the plugin at ./plugin
plugin/                          the plugin itself (what users install)
  .claude-plugin/plugin.json     plugin manifest (name, version, description, author, homepage, repository)
  SKILL.md                       the grounded-expert skill definition (procedure, levels, gotchas)
  evals/                         eval cases (prompt.md + graders/*.md per case) for `claude plugin eval`
  README.md, LICENSE             short plugin-level README and license
README.md                        this file
CONTRIBUTING.md                  eval-gate process for PRs
CHANGELOG.md                     release history
assets/                          logo (SVG + PNG 512/128/32) and social preview
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — a clean `claude plugin validate --strict`
run is not the same claim as a change being behaviorally safe; the
eval-gate process there explains why and what to run instead.

## Privacy

See [plugin/PRIVACY.md](plugin/PRIVACY.md).

## License

MIT — see [LICENSE](LICENSE).

## Versioning

SemVer, staying in the `0.x` range while the skill's procedure and eval
suite are still settling — a `0.x` version signals the API/behavior may
still change between minor bumps, without requiring a `1.0.0` promise of
stability we can't yet back up. Move to `1.0.0` once the eval suite is
stable and the plugin has run in production use for a while.
