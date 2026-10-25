<p align="center">
  <img src="assets/logo.svg" width="180" alt="grounded-expert 标志：侧面的蜜獾头像">
</p>

# grounded-expert

[![Release](https://img.shields.io/github/v/release/pko89403/grounded-expert)](https://github.com/pko89403/grounded-expert/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | **简体中文**

> 本译文已用 grounded-expert 审校并修订（standard 级别），详见文末[译文审校](#译文审校)。

一个 Claude Code 插件：回答领域问题时，它不会凭记忆扮演专家人设，而是启动一个 subagent，由它真正去实时查找一手资料（官方规范、文档、论文、标准），并用这些资料核对自己的说法。

## 示例

```
/grounded-expert HTTP 301 重定向时，客户端能否把 POST 改成 GET？
请依据 RFC 核实。
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

以下是 grounded-expert v0.5.0 的真实输出（eval 运行，每个用例运行一次）。节选只保留结论、3 行说法和反证搜索，完整回答折叠在下方。

<details>
<summary>查看完整回答</summary>

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

这是一个 Claude Code 插件。对 Google Antigravity 和 ChatGPT/Codex 的支持是实验性的。无法核实的说法会标记为 `not confirmed`。

## 为什么需要

给 subagent 设定人设（“你是 X 领域的专家”），它就会一边扮演这个角色，一边凭参数记忆作答，因此陈述错误事实时和陈述正确事实时一样笃定。本插件强制执行真正专家遵循的流程：去查资料、引用查到的内容、发现错误就自我纠正。

## 安装

```
/plugin install grounded-expert --marketplace pko89403/grounded-expert
```

（Claude Code v2.1.275 或更高版本会把本仓库作为插件市场（marketplace）来源添加，引导你确认后选择安装作用域（scope），并非无需确认的一步安装。如果不用会话内的 `/plugin` 命令而在 shell 中运行 `claude plugin install grounded-expert --marketplace pko89403/grounded-expert`，需要 Claude Code v2.1.292 或更高版本。）

本地开发：先运行 `claude plugin marketplace add <本仓库路径>`，再运行 `claude plugin install grounded-expert@grounded-expert`。

## 在 Google Antigravity 中使用（实验性）

Antigravity 支持由社区维护，未经 Claude Code eval suite 验证。该技能启动的 `self` subagent 是否具备 web search 和 URL-fetch 工具尚未验证。如果不具备，技能被指示不凭记忆作答，而是告知答案未经外部来源验证。

```
git clone https://github.com/pko89403/grounded-expert.git
cd grounded-expert
git checkout <release-tag>   # 固定到某个发布版本，避免链接跟随不断变化的工作区
scripts/install-antigravity.sh --global          # Antigravity App/IDE: ~/.gemini/config/skills/
scripts/install-antigravity.sh --global --cli    # Antigravity CLI: ~/.gemini/antigravity-cli/skills/
cd <your-project> && <clone>/scripts/install-antigravity.sh --workspace   # <project>/.agents/skills/
```

请使用 `v0.1.1` 或更新的发布标签。`v0.1.0` 中没有 `hosts/antigravity/`。

脚本创建的是指向 `hosts/antigravity/`（而非 `plugin/`）的符号链接。对同一模式加上 `--uninstall` 即可只删除该链接。脚本不会改动真实目录，也不会改动指向其他位置的链接。技能目录位置以 [Antigravity skills 文档](https://antigravity.google/docs/skills)为准。

## 在 ChatGPT 和 Codex 中使用

本仓库还提供面向 ChatGPT 和 Codex 的可移植 Agent Plugins 软件包。
OpenAI 软件包位于 `plugin/` 之外，因此不会改变现有 Claude Code 软件包和
eval 范围。

```bash
codex plugin marketplace add /absolute/path/to/this-checkout
codex plugin add grounded-expert@grounded-expert
```

请检出包含 `hosts/openai/` 的 `main`。`v0.3.0` 及更早的发布标签
不包含该目录。OpenAI 包仍处于实验阶段，未提交到公开插件目录。
ChatGPT 本地来源的安装与执行尚未验证。Codex 请明确调用
`$grounded-expert:grounded-expert`；自动触发范围尚未验证。仅在工具支持时请求不继承
对话的子会话，否则披露独立性限制。不能委派时应说明是直接研究；不能获取
来源时应说明未经外部验证。这些是指令，并非运行环境强制保证。
已观察到的失败、复现步骤及剩余发布条件见 [OpenAI 验证记录](docs/openai-evaluation.md)。
OpenAI 的 [隐私说明](hosts/openai/PRIVACY.md) 与 Claude 版本分开。

## 用法 (Claude Code)

当问题需要领域内的事实准确性，或明确要求专家意见/评审时，skill 会自动触发。也可以直接调用：

```
/grounded-expert <问题>
```

**费用说明**：每次调用都会启动真实的 subagent，实时调用 WebSearch/WebFetch；在 `standard`/`thorough` 级别还会额外做一次反证检索。这是真实的 API 用量，不是缓存或本地查询。`thorough` 还会额外并行启动多个 subagent。运行 eval suite（`claude plugin eval`）每次也会产生实际费用（judge 模型和 agent 模型都计费）。

### 级别

按问题而不是按会话选择一个级别（也可以自动推断）：

| 级别 | 行为 |
|---|---|
| **quick** | 1 个来源，不做反证检索，审查 1 次。 |
| **standard**（默认） | 2 个以上独立来源，EXTRACTED/INFERRED 标注，最多 2 次审查，其中包括 1 次反证检索。 |
| **thorough** | 在 standard 基础上，按每种候选来源类型并行增加一个 subagent，并交叉核对。适用于安全、法律或金钱利害攸关的问题。 |

触发词（韩语原文，括号内为中文释义）：“대충/빨리”（大概/快点）→ quick；“꼼꼼히/전부 확인해서”（仔细/全部核实）或涉及法律、安全的问题 → thorough；未指定 → standard。

## 插件结构

```
.claude-plugin/marketplace.json  市场清单（marketplace manifest），将插件登记为 ./plugin
.agents/plugins/marketplace.json ChatGPT/Codex 市场清单
plugin/                          插件本体（用户安装的部分）
  .claude-plugin/plugin.json     插件清单（name, version, description, author, homepage, repository）
  SKILL.md                       grounded-expert skill 定义（流程、级别、注意事项）
  evals/                         `claude plugin eval` 用的 eval case（每个 case 含 prompt.md + graders/*.md）
  README.md, LICENSE             插件用的简短 README 和许可证
hosts/openai/                    可移植 ChatGPT/Codex 插件及 skill 副本
README.md                        英文 README
CONTRIBUTING.md                  PR 的 eval 把关流程
CHANGELOG.md                     发布历史
assets/                          标志（SVG + PNG 512/128/32）和社交预览图
```

## 贡献

请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。`claude plugin validate --strict` 通过并不等于改动在行为上是安全的；那里的 eval 把关流程说明了原因以及应改为运行什么。

## 许可证

MIT，见 [LICENSE](LICENSE)。

## 版本策略

遵循 SemVer。由于 skill 流程和 eval suite 尚未定型，版本保持在 `0.x` 范围。`0.x` 表示次版本号升级之间 API/行为仍可能变化，同时无需做出我们目前还无法兑现的 `1.0.0` 稳定性承诺。待 eval suite 稳定、并在生产环境中运行一段时间后再升到 `1.0.0`。

## 译文审校

本译文通过调用 `/grounded-expert` skill 以 standard 级别审校：skill 启动的 subagent 实际查阅下列资料，对照英文原文提出修改，每条依据都标注了 EXTRACTED 或 INFERRED，并做了反证检索。据此修订了：

- 误译和遗漏：“production”未译出、“claim”误作“结论”、主语错位、“without requiring”误作“以免”
- 标点与加粗写法、中文段落的软换行
- 术语：scope → 作用域、manifest → 清单、marketplace source → 来源（依据插件概览页；官方文档各页用词并不统一，如安装页多用“范围”）

审校共进行两轮：第一轮由手动照搬 skill 流程的 subagent 完成；第二轮正式调用 skill，并复核了第一轮的修改。

- [中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines/blob/master/README.zh-Hans.md)
- [GB/T 15834-2011 标点符号用法（经 W3C clreq 等核对）](https://www.w3.org/TR/clreq/)
- [Claude Code 安装和管理插件（zh-CN）](https://code.claude.com/docs/zh-CN/discover-plugins)
- [语义化版本 2.0.0（zh-CN）](https://semver.org/lang/zh-CN/)
- [中文技术文档写作规范 · 标点符号（ruanyf）](https://github.com/ruanyf/document-style-guide/blob/master/docs/marks.md)
- [W3C 中文排版需求（clreq）](https://www.w3.org/TR/clreq/)
- [Claude Code 插件概览（zh-CN）](https://code.claude.com/docs/zh-CN/plugins)
- [CommonMark Spec 0.31.2](https://spec.commonmark.org/0.31.2/)
