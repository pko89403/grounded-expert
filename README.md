# grounded-expert

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

(Claude Code 2.1.275 or later installs directly from the GitHub marketplace
in one step. For local development, add this repo as a marketplace source
with `claude plugin marketplace add <path>` and install from it the same
way.)

## Usage

The skill fires automatically when a question needs domain-specific factual
accuracy, or when explicitly asked for an expert opinion/review. You can also
invoke it directly:

```
/grounded-expert <question>
```

**Cost note:** each invocation spawns a real subagent that does live
WebSearch/WebFetch calls and (on `standard`/`thorough`) a disconfirming-search
pass — this is real API usage, not a cached/local lookup. `thorough` spawns
additional parallel subagents on top of that. Running the eval suite
(`claude plugin eval`) also costs real money per run (judge model + agent
model both bill).

### Levels

Pick (or let it infer) one level per question, not per session:

| Level | Behavior |
|---|---|
| **quick** | 1 source, no disconfirming-evidence search, 1 critique pass. |
| **standard** (default) | 2+ independent sources, EXTRACTED/INFERRED tagging, up to 2 critique passes incl. 1 disconfirming-evidence search. |
| **thorough** | standard, plus one additional subagent per candidate source type in parallel, cross-checked. For safety/legal/money stakes. |

Trigger words: "대충/빨리" → quick, "꼼꼼히/전부 확인해서" or legal/safety stakes →
thorough, nothing specified → standard.

### Example

```
/grounded-expert HTTP 301로 리다이렉트되면 POST를 GET으로 바꿔도 되는지
RFC 기준으로 확인해줘.
```

The subagent retrieves RFC 9110/7231, quotes the relevant passage, tags the
claim EXTRACTED or INFERRED, and reports what remains uncertain.

## Plugin structure

```
.claude-plugin/plugin.json   plugin manifest (name, version, description, author, homepage, repository)
SKILL.md                     the grounded-expert skill definition (procedure, levels, gotchas)
evals/                       eval cases (prompt.md + graders/*.md per case) for `claude plugin eval`
README.md                    this file
CONTRIBUTING.md              eval-gate process for PRs
CHANGELOG.md                 release history
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — `claude plugin validate --strict`
passing is not the same claim as a change being behaviorally safe; the
eval-gate process there explains why and what to run instead.

## License

MIT — see [LICENSE](LICENSE).

## Versioning

SemVer, staying in the `0.x` range while the skill's procedure and eval
suite are still settling — a `0.x` version signals the API/behavior may
still change between minor bumps, without requiring a `1.0.0` promise of
stability we can't yet back up. Move to `1.0.0` once the eval suite is
stable and the plugin has run in production use for a while.
