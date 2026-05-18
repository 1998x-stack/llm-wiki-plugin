---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: [ai-engineering, evaluation, benchmark, browsing, AI工程]
aliases: [BrowseComp, Browse Competition]
relates_to:
  - target: "[[评测驱动开发]]"
    type: part_of
  - target: "[[Anthropic]]"
    type: part_of
  - target: "[[SWE-bench]]"
    type: compares_to
supersedes: null
---

# BrowseComp

## 概述
BrowseComp 是 [[Anthropic]] 提出的浏览器操作能力评测基准，用于评估 AI Agent 在真实网页环境中的导航、信息提取和任务完成能力。

## 关键内容

1. **Eval 感知分析**：2026 年 3 月提出的测试行为分析，揭示模型在 BrowseComp 上的评测行为模式，推动评测透明披露机制的建立。

2. **Token 使用量与性能关系**：研究发现 Token 使用量可解释 80% BrowseComp 方差，证明[[Context Management|上下文管理]]效率是浏览器操作能力的关键决定因素。

3. **与 [[SWE-bench]] 的对比**：
   - [[SWE-bench]] 评估代码修复能力（静态）
   - BrowseComp 评估浏览器操作能力（动态交互）
   - 两者共同构成 AI Agent 能力的多维度评估体系

4. **抗 AI 评估挑战**：随着模型能力提升，传统评测方法面临失效风险，BrowseComp 代表了对动态交互能力评估的新方向。

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/00_INDEX.md]] — 评测与质量保障章节
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/16_eval_awareness_browsecomp.md]] — Eval 感知分析：Claude Opus 4.6 在 BrowseComp 上的测试行为

## 相关
- [[评测驱动开发]] — part_of
- [[Anthropic]] — part_of
- [[SWE-bench]] — compares_to
- [[上下文工程]] — relates_to
- [[Token 资源管理]] — relates_to
- [[评测感知]] — relates_to（BrowseComp 是评测感知现象的发现场景）
- [[格式敏感性]] — relates_to（BrowseComp 格式激活了模型特定搜索策略）
- [[训练数据污染]] — relates_to（BrowseComp 可能受训练数据污染影响的基准）
