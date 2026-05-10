---
type: entity
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [公司, AI, 大模型]
aliases: [OpenAI Inc.]
relates_to:
  - target: "[[Codex CLI]]"
    type: part_of
    confidence: 0.95
  - target: "[[Rust]]"
    type: uses
    confidence: 0.85
  - target: "[[Harness-Engineering]]"
    type: developed
    confidence: 0.8
  - target: "[[Humans-steer-Agents-execute]]"
    type: originated
    confidence: 0.8
supersedes: null
---

# OpenAI

美国人工智能研究公司，成立于 2015 年，总部位于旧金山。以 [[GPT 系列]]大模型和 [[ChatGPT]] 闻名，同时开源多个开发者工具。

## 关键内容

1. **开发者工具线**：发布 [[Codex CLI]]——以 [[Rust]] 重写的本地编码 Agent，采用 Policy-First 架构与 OS 级沙箱隔离。
2. **开源策略**：[[Codex CLI]] 以开源方式发布，允许社区审查其安全架构（[[ExecPolicy]]、Sandbox、MCP 层）。
3. **工程哲学**：选择 Rust 而非 [[TypeScript]] 重写 [[Codex CLI|Codex]]，体现了"安全隔离必须在系统调用层做"的底层思维。
4. **[[Harness-Engineering|Harness Engineering]] 先驱**：进行了 3 个工程师 5 个月构建超过 100 万行代码的实验，所有代码均由 [[Codex CLI|Codex]] 生成，提出了"Human steer. [[Agents]] execute."的核心哲学。

## 来源

- [[raw/articles/ai-tools/codex/01_codex_architecture_overview.md]] — 整体架构章节
- [[Harness Engineering的本质是什么？ - riba2534 的回答]] — Harness Engineering 实验介绍

## 相关

- [[Codex CLI]] — OpenAI 开源的本地编码 Agent
- [[Rust]] — OpenAI 选择用于重写 Codex 的系统编程语言
- [[Claude Code]] — 竞品，Anthropic 的编码 Agent
- [[Harness-Engineering]] — OpenAI 推广的 AI 时代工程方法论
- [[Humans-steer-Agents-execute]] — OpenAI 提出的核心哲学
