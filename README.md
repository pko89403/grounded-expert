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
```

## Contributing

- Follow the existing eval case schema when adding a case: `evals/<case>/prompt.md`
  (frontmatter: `max_turns`, `timeout_seconds`, `allowed_tools`, `runs`) plus
  `evals/<case>/graders/*.md`.
- Run `claude plugin validate --strict .` before opening a PR.
- Run `claude plugin eval` with `--judge-model opus` (never sonnet/haiku) if you
  change SKILL.md or any grader.

## License

Not yet decided — this is an explicit open decision for the repo owner, not
something contributors or this plugin's code should assume. Until a LICENSE
file is added, default copyright applies (no reuse rights granted).

## Versioning

SemVer, staying in the `0.x` range while the skill's procedure and eval
suite are still settling — a `0.x` version signals the API/behavior may
still change between minor bumps, without requiring a `1.0.0` promise of
stability we can't yet back up. Move to `1.0.0` once the eval suite is
stable and the plugin has run in production use for a while.
