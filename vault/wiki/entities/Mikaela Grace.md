---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [人物, Anthropic, 工程师, 评测, AI工程]
aliases: ["Mikaela Grace"]
relates_to:
  - target: "[[Anthropic]]"
    type: part_of
  - target: "[[Jeremy Hadfield]]"
    type: compares_to
  - target: "[[评测驱动开发]]"
    type: implements
supersedes: null
---

# Mikaela Grace

## 概述
Mikaela Grace 是 [[Anthropic]] 的工程师，参与了 [[评测驱动开发|Agent 评测]]系统工程的指南撰写，是《Demystifying evals for AI agents》一文的第一作者。

## 关键内容

1. **在 [[Anthropic]] 的工作**：
   - 主导 [[评测驱动开发|Agent 评测]]从零到一的系统工程指南
   - 撰写关于评测生命周期管理的全面技术博客
   - 定义了完整的 [[评测驱动开发|Agent 评测]]术语体系（Task/Trial/[[评分器设计|Grader]]/Transcript/Outcome）

2. **技术贡献**：
   - 提出"没有 eval 的团队陷入被动修复循环，有 eval 的团队能主动驾驭质量"的核心理念
   - 建立四类 Agent（编码、对话、研究、[[计算]]机使用）的具体评测策略
   - 澄清 [[pass@k vs pass^k]] 的统计含义与适用场景

3. **合作者**：与 [[Jeremy Hadfield]]、[[Rodrigo Olivares]]、[[Jiri De Jonghe]] 共同完成评测指南的撰写。

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/12_demystifying_evals.md]] — 第一作者信息

## 相关
- [[Anthropic]] — part_of
- [[Jeremy Hadfield]] — compares_to
- [[评测驱动开发]] — implements
