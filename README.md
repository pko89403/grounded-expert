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

## Example

```
/grounded-expert HTTP 301로 리다이렉트되면 POST를 GET으로 바꿔도 되는지
RFC 기준으로 확인해줘.
```

**결론:** 현행 RFC 9110에서는 POST 요청이 301 또는 302를 받으면 사용자 에이전트가 리다이렉트된 요청을 GET으로 바꿔도 됩니다(MAY, "역사적인 이유로"라고 명시). 의무는 아니고 허용입니다.

Level: standard
Domain: http

| # | Claim | Tag | Quote | Source | URL |
|---|---|---|---|---|---|
| 1 | RFC 9110은 301 응답 뒤 POST를 GET으로 바꾸는 것을 허용한다(MAY) | EXTRACTED | "For historical reasons, a user agent MAY change the request method from POST to GET for the subsequent request." | RFC 9110 §15.4.2 301 Moved Permanently | https://www.rfc-editor.org/rfc/rfc9110.html |
| 4 | 307에서는 자동 리다이렉트 시 메서드를 바꾸면 안 된다(MUST NOT) | EXTRACTED | "the user agent MUST NOT change the request method if it performs an automatic redirection to that URI." | RFC 9110 §15.4.8 307 Temporary Redirect | https://www.rfc-editor.org/rfc/rfc9110.html |
| 5 | 308은 301과 비슷하지만 POST에서 GET으로의 변경을 허용하지 않는다 | EXTRACTED | "except that it does not allow changing the request method from POST to GET." | RFC 7538 §3 308 Permanent Redirect (Note) | https://www.rfc-editor.org/rfc/rfc7538.html |

Disconfirming search: found — https://www.rfc-editor.org/rfc/rfc2616.html

This is a real output from grounded-expert v0.5.0 (an eval run, one run per case). The excerpt keeps the conclusion, three of the claim rows and the disconfirming search; the full answer is below. The run used this Korean prompt; the skill answers in the language of the question.

<details>
<summary>Full answer</summary>

**결론:** 현행 RFC 9110에서는 POST 요청이 301 또는 302를 받으면 사용자 에이전트가 리다이렉트된 요청을 GET으로 바꿔도 됩니다(MAY, "역사적인 이유로"라고 명시). 의무는 아니고 허용입니다.

- **307:** RFC 9110 §15.4.8이 "MUST NOT change the request method"라고 명시적으로 금지합니다.
- **308:** 이번에 연 RFC 9110 페이지의 §15.4.9 본문에서는 "MUST NOT" 문장을 확인하지 못했습니다. 대신 RFC 7538(308의 원래 정의)이 "POST에서 GET으로 바꾸는 것을 허용하지 않는다"고 적고 있고, RFC 9110 §15.4.2도 그런 변경을 원하지 않으면 308을 쓰라고 합니다. 그러니 "307/308은 메서드 변경을 금지한다"는 말은 맞습니다. 다만 금지 표현의 강도는 307(MUST NOT)과 308(허용하지 않음)이 다릅니다.
- **303:** RFC 9110에서 303은 POST 처리 결과를 다른 리소스로 보낼 때 쓰는 코드입니다. 사용자 에이전트는 그 URI로 조회 요청(HTTP라면 GET이나 HEAD)을 보낼 수 있다고 되어 있습니다.
- **브라우저 동작 명세:** WHATWG Fetch의 HTTP-redirect fetch는 두 경우에 메서드를 GET으로 바꾸고 본문을 null로 만듭니다. (1) 301/302이고 메서드가 POST일 때, (2) 303이고 메서드가 GET/HEAD가 아닐 때입니다.
- **과거 RFC 2616:** 301/302에서 GET/HEAD가 아닌 요청은 사용자 확인 없이 자동으로 리다이렉트하면 안 된다(MUST NOT)고 했습니다. POST를 GET으로 바꾸는 동작은 "erroneously"(잘못된 것)로 기록했습니다.

Level: standard  
Domain: http

| # | Claim | Tag | Quote | Source | URL |
|---|---|---|---|---|---|
| 1 | RFC 9110은 301 응답 뒤 POST를 GET으로 바꾸는 것을 허용한다(MAY) | EXTRACTED | "For historical reasons, a user agent MAY change the request method from POST to GET for the subsequent request." | RFC 9110 §15.4.2 301 Moved Permanently | https://www.rfc-editor.org/rfc/rfc9110.html |
| 2 | 302에도 같은 허용 문장이 있다 | EXTRACTED | "For historical reasons, a user agent MAY change the request method from POST to GET for the subsequent request." | RFC 9110 §15.4.3 302 Found | https://www.rfc-editor.org/rfc/rfc9110.html |
| 3 | RFC 9110 §15.4.2는 그런 변경을 원하지 않으면 308을 쓰라고 한다 | EXTRACTED | "If this behavior is undesired, the 308 (Permanent Redirect) status code can be used instead." | RFC 9110 §15.4.2 | https://datatracker.ietf.org/doc/html/rfc9110 |
| 4 | 307에서는 자동 리다이렉트 시 메서드를 바꾸면 안 된다(MUST NOT) | EXTRACTED | "the user agent MUST NOT change the request method if it performs an automatic redirection to that URI." | RFC 9110 §15.4.8 307 Temporary Redirect | https://www.rfc-editor.org/rfc/rfc9110.html |
| 5 | 308은 301과 비슷하지만 POST에서 GET으로의 변경을 허용하지 않는다 | EXTRACTED | "except that it does not allow changing the request method from POST to GET." | RFC 7538 §3 308 Permanent Redirect (Note) | https://www.rfc-editor.org/rfc/rfc7538.html |
| 6 | 303은 POST 처리 결과로 사용자 에이전트를 다른 리소스로 보낼 때 주로 쓰인다 | EXTRACTED | "is primarily used to allow the output of a POST action to redirect the user agent to a different resource." | RFC 9110 §15.4.4 303 See Other | https://www.rfc-editor.org/rfc/rfc9110.html |
| 7 | 303을 받은 사용자 에이전트는 그 URI로 GET 또는 HEAD 조회 요청을 보낼 수 있다 | EXTRACTED | "A user agent can perform a retrieval request targeting that URI (a GET or HEAD request if using HTTP)" | RFC 9110 §15.4.4 303 See Other | https://datatracker.ietf.org/doc/html/rfc9110 |
| 8 | Fetch 표준은 301/302 + POST일 때 메서드를 GET으로 바꾼다 | EXTRACTED | "internalResponse’s status is 301 or 302 and request’s method is `POST`" | WHATWG Fetch §4.5 HTTP-redirect fetch, step 12 | https://fetch.spec.whatwg.org/ |
| 9 | Fetch 표준은 303 + GET/HEAD가 아닌 메서드일 때도 GET으로 바꾼다 | EXTRACTED | "internalResponse’s status is 303 and request’s method is not `GET` or `HEAD`" | WHATWG Fetch §4.5 HTTP-redirect fetch, step 12 | https://fetch.spec.whatwg.org/ |
| 10 | 위 조건에 해당하면 메서드를 GET으로, 본문을 null로 설정한다 | EXTRACTED | "Set request’s method to `GET` and request’s body to null." | WHATWG Fetch §4.5 HTTP-redirect fetch | https://fetch.spec.whatwg.org/ |
| 11 | RFC 2616은 301/302에서 GET/HEAD가 아닌 요청을 사용자 확인 없이 자동으로 리다이렉트하는 것을 금지했다 | EXTRACTED | "MUST NOT automatically redirect the request unless it can be confirmed by the user" | RFC 2616 §10.3.2 / §10.3.3 | https://www.rfc-editor.org/rfc/rfc2616.html |
| 12 | RFC 2616은 301에서 POST를 GET으로 바꾸는 HTTP/1.0 클라이언트를 "잘못된" 동작으로 기록했다 | EXTRACTED | "some existing HTTP/1.0 user agents will erroneously change it into a GET request." | RFC 2616 §10.3.2 Note | https://www.rfc-editor.org/rfc/rfc2616.html |
| 13 | RFC 2616은 대부분의 구현이 302를 303처럼 처리한다고 기록했다 | EXTRACTED | "most existing user agent implementations treat 302 as if it were a 303 response" | RFC 2616 §10.3.3 Note | https://www.rfc-editor.org/rfc/rfc2616.html |
| 14 | RFC 2616의 303은 새 URI에서 GET으로 조회해야 한다(SHOULD)고 했다 | EXTRACTED | "SHOULD be retrieved using a GET method on that resource." | RFC 2616 §10.3.4 303 See Other | https://www.rfc-editor.org/rfc/rfc2616.html |
| 15 | RFC 7231(2014)이 301/302의 POST에서 GET으로의 재작성을 처음으로 규격 준수 동작으로 만들었다 | not confirmed | - | RFC 7231 §6.4 (검색 스니펫에서만 봄, 페이지는 열지 않음) | - |

**남은 불확실성**
- 이번에 받은 RFC 9110 §15.4.9 본문에서는 "does not allow changing the request method from POST to GET" 같은 문장을 직접 확인하지 못했습니다. 그래서 308이 메서드를 보존한다는 근거로 RFC 7538과 RFC 9110 §15.4.2를 인용했습니다.
- RFC 7231 §6.4는 직접 열지 않았습니다.
- RFC 2616 인용문은 fetch 도구가 돌려준 발췌입니다. 원문 전체 문장의 앞뒤 맥락(예: "If the 301 status code is received in response to a request other than GET or HEAD")은 직접 확인하지 못했습니다.
- RFC 2616은 이미 폐기된 문서입니다. 현행 규범은 RFC 9110입니다.

Disconfirming search: found — https://www.rfc-editor.org/rfc/rfc2616.html

</details>

Claude Code plugin. Google Antigravity and ChatGPT/Codex support are experimental. Claims it could not verify are marked `not confirmed`.

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

Use `v0.1.1` or a later release tag: `v0.1.0` predates `hosts/antigravity/`.

The script symlinks `hosts/antigravity/` (not `plugin/`). Add `--uninstall` to
remove the link for the same mode. It never touches a real directory or a link
that points elsewhere. Skill locations follow
[Antigravity's skills docs](https://antigravity.google/docs/skills).

## Use with ChatGPT and Codex

The repository also ships an experimental portable Agent Plugins package for ChatGPT and
Codex. It stays outside `plugin/`, so the existing Claude Code package and eval
surface are unchanged.

```bash
codex plugin marketplace add /absolute/path/to/this-checkout
codex plugin add grounded-expert@grounded-expert
```

Use a checkout of `main` containing `hosts/openai/`; release tags through
`v0.3.0` do not contain it. This package has **not** been submitted to the
public Plugins Directory. ChatGPT local-source installation and execution have
not been verified end to end here. In Codex, explicitly request
`$grounded-expert:grounded-expert`; automatic trigger coverage is not certified.
The skill requests a fresh/no-history child only when the exposed tool supports
it, and discloses weaker isolation otherwise. Without delegation it must report
direct research; without source-retrieval tools it must report that external
verification was not possible. These are instructions, not enforced runtime
guarantees. See [OpenAI evaluation](docs/openai-evaluation.md) for observed failures,
reproduction steps, and the remaining release gate.

## Usage (Claude Code)

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

## Plugin structure

```
.claude-plugin/marketplace.json  marketplace manifest; lists the plugin at ./plugin
.agents/plugins/marketplace.json ChatGPT/Codex marketplace manifest
plugin/                          the plugin itself (what users install)
  .claude-plugin/plugin.json     plugin manifest (name, version, description, author, homepage, repository)
  SKILL.md                       the grounded-expert skill definition (procedure, levels, gotchas)
  evals/                         eval cases (prompt.md + graders/*.md per case) for `claude plugin eval`
  README.md, LICENSE             short plugin-level README and license
hosts/openai/                    portable ChatGPT/Codex plugin and skill copy
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

Claude Code: [plugin/PRIVACY.md](plugin/PRIVACY.md).
OpenAI host: [hosts/openai/PRIVACY.md](hosts/openai/PRIVACY.md).

## License

MIT — see [LICENSE](LICENSE).

## Versioning

SemVer, staying in the `0.x` range while the skill's procedure and eval
suite are still settling — a `0.x` version signals the API/behavior may
still change between minor bumps, without requiring a `1.0.0` promise of
stability we can't yet back up. Move to `1.0.0` once the eval suite is
stable and the plugin has run in production use for a while.
