<p align="center">
  <img src="assets/logo.svg" width="180" alt="grounded-expert 标志：侧面的蜜獾头像">
</p>

# grounded-expert

[![Release](https://img.shields.io/github/v/release/pko89403/grounded-expert)](https://github.com/pko89403/grounded-expert/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | **简体中文**

> 本译文已用 grounded-expert 本身审校并修订（standard 级别），详见文末[译文审校](#译文审校)。

一个 Claude Code 插件：回答领域问题时，它不会凭记忆扮演专家人设，而是启动一个 subagent，由它实时查找一手资料（官方规范、文档、论文、标准），并用这些资料核对自己的结论。

## 为什么需要

给 subagent 设定人设（“你是 X 领域的专家”），模型就会一边扮演这个角色，一边凭参数记忆作答，因此陈述错误事实时和陈述正确事实时一样笃定。本插件强制执行真正专家遵循的流程：去查资料、引用查到的内容、发现错误就自我纠正。

## 安装

```
/plugin install grounded-expert --marketplace pko89403/grounded-expert
```

（Claude Code 2.1.275 及以上版本会把本仓库添加为插件市场（marketplace）源，引导你确认后选择安装作用域（scope），并非无需确认的一步安装。如果不用 slash command 而用 shell 命令 `claude plugin install grounded-expert --marketplace pko89403/grounded-expert`，需要 Claude Code 2.1.292 及以上版本。）

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
| **thorough** | 在 standard 基础上，按每种候选来源类型并行增加一个 subagent，并交叉核对。适用于涉及安全、法律责任或金钱的问题。 |

触发词（韩语原文，括号内为中文释义）：“대충/빨리”（大概/快点）→ quick；“꼼꼼히/전부 확인해서”（仔细/全部核实）或涉及法律、安全的问题 → thorough；未指定 → standard。

### 示例

```
/grounded-expert HTTP 301 重定向时，客户端能否把 POST 改成 GET？
请依据 RFC 核实。
```

subagent 会查阅 RFC 9110/7231，引用相关段落，为每个结论标注 EXTRACTED 或 INFERRED，并报告仍不确定的部分。

## 插件结构

```
.claude-plugin/plugin.json       插件清单（name, version, description, author, homepage, repository）
.claude-plugin/marketplace.json  市场清单（marketplace manifest），使 `/plugin install ... --marketplace` 能找到本插件
SKILL.md                         grounded-expert skill 定义（流程、级别、注意事项）
evals/                           `claude plugin eval` 用的 eval case（每个 case 含 prompt.md + graders/*.md）
README.md                        英文 README
CONTRIBUTING.md                  PR 的 eval 把关流程
CHANGELOG.md                     发布历史
assets/                          标志（SVG + PNG 512/128/32）和社交预览图
```

## 贡献

请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。`claude plugin validate --strict` 通过并不等于改动在行为上是安全的；原因以及应改为运行什么，都写在那里。

## 许可证

MIT，见 [LICENSE](LICENSE)。

## 版本策略

遵循 SemVer。由于 skill 流程和 eval suite 尚未定型，版本保持在 `0.x` 范围。`0.x` 表示 minor 版本之间 API/行为仍可能变化，以免承诺我们尚无法保证的 `1.0.0` 级别稳定性。待 eval suite 稳定、并在生产环境中运行一段时间后再升到 `1.0.0`。

## 译文审校

本译文由 grounded-expert（standard 级别）审校：subagent 实际查阅下列资料，对照英文原文提出修改，每条依据都标注了 EXTRACTED 或 INFERRED，并做了一次反证检索。据此修订了误译和遗漏（如 “production” 未译出）、标点与加粗写法、术语（scope → 作用域，manifest → 清单）以及中文段落的软换行。

- [中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines/blob/master/README.zh-Hans.md)
- [中文技术文档写作规范 · 标点符号（ruanyf）](https://github.com/ruanyf/document-style-guide/blob/master/docs/marks.md)
- [W3C 中文排版需求（clreq）](https://www.w3.org/TR/clreq/)
- [Claude Code 插件概览（zh-CN）](https://code.claude.com/docs/zh-CN/plugins)
- [CommonMark Spec 0.31.2](https://spec.commonmark.org/0.31.2/)
