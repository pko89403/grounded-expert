<p align="center">
  <img src="assets/logo.svg" width="180" alt="grounded-expert 标志：侧面的蜜獾头像">
</p>

# grounded-expert

[![Release](https://img.shields.io/github/v/release/pko89403/grounded-expert)](https://github.com/pko89403/grounded-expert/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | **简体中文**

> 本译文已用 grounded-expert 审校并修订（standard 级别），详见文末[译文审校](#译文审校)。

一个 Claude Code 插件：回答领域问题时，它不会凭记忆扮演专家人设，而是启动一个 subagent，由它真正去实时查找一手资料（官方规范、文档、论文、标准），并用这些资料核对自己的说法。

## 为什么需要

给 subagent 设定人设（“你是 X 领域的专家”），它就会一边扮演这个角色，一边凭参数记忆作答，因此陈述错误事实时和陈述正确事实时一样笃定。本插件强制执行真正专家遵循的流程：去查资料、引用查到的内容、发现错误就自我纠正。

## 安装

```
/plugin install grounded-expert --marketplace pko89403/grounded-expert
```

（Claude Code v2.1.275 或更高版本会把本仓库作为插件市场（marketplace）来源添加，引导你确认后选择安装作用域（scope），并非无需确认的一步安装。如果不用会话内的 `/plugin` 命令而在 shell 中运行 `claude plugin install grounded-expert --marketplace pko89403/grounded-expert`，需要 Claude Code v2.1.292 或更高版本。）

本地开发：先运行 `claude plugin marketplace add <本仓库路径>`，再运行 `claude plugin install grounded-expert@grounded-expert`。

## 用法

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

### 示例

```
/grounded-expert HTTP 301 重定向时，客户端能否把 POST 改成 GET？
请依据 RFC 核实。
```

subagent 会查阅 RFC 9110/7231，引用相关段落，为该说法标注 EXTRACTED 或 INFERRED，并报告仍不确定的部分。

## 插件结构

```
.claude-plugin/marketplace.json  市场清单（marketplace manifest），将插件登记为 ./plugin
plugin/                          插件本体（用户安装的部分）
  .claude-plugin/plugin.json     插件清单（name, version, description, author, homepage, repository）
  SKILL.md                       grounded-expert skill 定义（流程、级别、注意事项）
  evals/                         `claude plugin eval` 用的 eval case（每个 case 含 prompt.md + graders/*.md）
  README.md, LICENSE             插件用的简短 README 和许可证
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
