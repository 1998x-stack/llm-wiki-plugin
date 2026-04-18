---
type: entity
status: active
confidence: 0.88
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 2
tags: [技术, 研究, 工具与框架]
aliases: ["Prithvi Rajasekaran"]
relates_to:
  - target: "[[Claude-Code]]"
    type: uses
    confidence: 0.95
  - target: "[[生成器-评估器架构]]"
    type: caused
    confidence: 0.95
  - target: "[[Agent Harness模式]]"
    type: extends
    confidence: 0.9
supersedes: null
---

# Prithvi Rajasekaran

## 概述

[[Anthropic]] Labs 团队成员，AI 工程实践研究者，专注于长时自主编码 Agent 的 Harness 设计与前端设计质量提升，提出了 [[生成器-评估器架构]] 和[[Sprint合约制]]等方法。

## 关键内容

1. **研究领域**：前端设计自动化 + 长时自主编码 Agent，两个截然不同的领域——一个由主观品味定义，一个由可验证正确性定义。
2. **核心贡献**：受 GAN 启发，设计了 **[[生成器]] + 评估器** 双 Agent 架构，将主观质量转化为可评分的具体准则，并构建了覆盖前端设计和全栈开发的三 Agent 系统（Planner → [[生成器|Generator]] → Evaluator）。
3. **工程哲学**："每个 Harness 组件都编码了模型还不能自己做到的假设，这些假设值得持续质疑——因为它们可能已经过时。"即 "find the simplest solution possible, and only increase complexity when needed"。
4. **发布文章**：
   - *Harness design for long-running application development*（2026）
   - *Effective context engineering for AI agents*（2026，与 Ethan Dixon、Carly Ryan、Jeremy Hadfield 合著）
   - 前序：*Effective harnesses for long-running agents*（合作）

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/Harness design for long-running application development.md]]
- [[raw/articles/ai-engineering/anthropic-engineering/Effective context engineering for AI agents.md]]

## 相关

- [[生成器-评估器架构]] — caused（GAN 启发的核心架构创新）
- [[Sprint合约制]] — caused（Sprint 前合约谈判机制）
- [[上下文焦虑]] — extends（发现并命名此现象）
- [[Agent Harness模式]] — extends
- [[Claude-Code]] — uses
