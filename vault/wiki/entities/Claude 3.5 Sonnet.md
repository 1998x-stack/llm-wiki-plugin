---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [AI, LLM, Anthropic, 模型, AI工程]
aliases:
- Claude 3.5 Sonnet
- Claude 3.5 Sonnet 模型
relates_to:
- target: '[[Anthropic]]'
  type: part_of
  confidence: 0.95
- target: '[[SWE-bench]]'
  type: uses
  confidence: 0.9
- target: '[[Claude Code]]'
  type: extends
  confidence: 0.85
- target: '[[Agent 架构与设计原则]]'
  type: implements
  confidence: 0.8
supersedes: null
---

# Claude 3.5 Sonnet

## 概述
[[Claude_Code|Claude]] 3.5 Sonnet 是 [[Anthropic]] 推出的 [[Claude_Code|Claude]] 系列模型之一，在 [[SWE-bench]] Verified 上实现了当时 SOTA 成绩（49%），证明了[[单 Agent 架构]]配合优质工具集即可达到顶尖编码能力。

## 关键内容

1. **[[SWE-bench]] SOTA 成绩**：在 [[SWE-bench]] Verified 上达到 **49%** 解决率，为当时最高成绩，后续迭代达到更高。这一成绩标志着 [[Claude_Code|Claude]] 在编码 Agent 基准上取得领先地位。

2. **[[单 Agent 架构]]设计**：采用相对简单的[[单 Agent 架构]]——[[Claude_Code|Claude]] 3.5 Sonnet 作为核心推理引擎，配合精心设计的工具集（文件读写、命令执行、搜索等），无复杂的多 Agent 编排。体现了 [[Anthropic]] "简单优于复杂"的哲学。

3. **工具优化优先**：在 [[SWE-bench]] 任务中，工程师花在**工具优化**上的时间多于花在**整体 prompt** 上的时间。关键发现包括要求工具始终使用绝对路径，解决了模型在相对路径上的系统性错误。

4. **[[Think 工具]]集成**：集成了 [[Think 工具]] 专为代码调试场景定制，实验表明平均提升性能 **1.6%**（Welch t 检验，p < 0.001，效应量 d=1.47）。

5. **产品意义**：[[SWE-bench]] 成绩直接支撑了 [[Claude Code]] 产品的核心价值主张——[[Claude_Code|Claude]] 不仅是代码补全工具，而是能够独立解决真实软件工程问题的 Agent。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/07_swe_bench_sonnet.md]] — Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet

## 相关

- [[Anthropic]] — part_of（Claude 3.5 Sonnet 是 Anthropic 产品线的核心模型）
- [[SWE-bench]] — uses（在 SWE-bench Verified 上验证了 49% SOTA 成绩）
- [[Claude Code]] — extends（SWE-bench 成绩支撑了 Claude Code 产品价值主张）
- [[Agent 架构与设计原则]] — implements（单 Agent 架构 + 优质工具集 = SOTA）
