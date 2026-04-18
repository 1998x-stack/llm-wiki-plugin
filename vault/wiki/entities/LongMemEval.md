---
type: entity
title: "LongMemEval"
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: [基准测试, 评估, AI记忆, 论文]
aliases: []
relates_to:
  - target: "[[MemPalace]]"
    type: used_by
  - target: "[[Mem0]]"
    type: used_by
  - target: "[[Zep]]"
    type: used_by
supersedes: null
---

# LongMemEval

## 概述
AI 长期记忆系统评估基准，用于衡量[[记忆工具]]的检索召回率。[[MemPalace]] 在此基准上达到 96.6% 的 [[候选生成|Recall]]@5 成绩。

## 关键内容
- **评估指标**：[[候选生成|Recall]]@5（R@5），即前 5 个检索结果中包含正确答案的比例
- **数据集特点**：包含多轮、跨会话的长对话记录，问题需要跨多个历史会话才能回答
- **[[MemPalace]] 成绩**：96.6%（原文模式）
- **对比成绩**：Mem0 和 Zep 均约 85%，[[MemPalace]] 领先约 11 个百分点
- **意义**：96.6% 的成绩验证了"[[原文逐字存储]] + 结构化检索"策略相比"AI 提取关键信息"策略的优越性

### MemPalace 架构迭代记录

LongMemEval 记录了 [[MemPalace]] 完整的架构进化过程：

| 架构版本 | 方法 | R@5 | 说明 |
|---------|------|-----|------|
| 基线 | 扁平向量搜索（[[ChromaDB]]） | 60.9% | 朴素 RAG 天花板 |
| v1 | [[LLM 路由]]（Haiku 双端） | 34.2% | 灾难性失败，词汇不匹配 |
| v2 | 关键词路由（去查询期 LLM） | 75.6% | +15pp vs 基线 |
| v3 | 宫殿结构 + [[混合搜索]] | — | [[LoCoMo]] R@10 = 88.9% |
| v4-v5 | 精准 Bug Fix | — | 引号提取、人名权重、怀旧模式 |
| Hybrid v5 | 完整方案 | 96.6% | 最终结果 |

**34% 提升分解**：约 34.1pp 来自宫殿结构（路由精准化），约 1.8pp 来自[[混合搜索]] + 三项 Fix。

### 社区质疑与官方回应

- **质疑 1**：AAAK 节省 token 的声明有误（用 `len(text)//3` 估算而非真实分词）。官方修正：[[OpenAI]] 分词器真实统计显示 AAAK 在小规模场景不省 token
- **质疑 2**：96.6% 是在哪种模式下测的。官方澄清：来自[[原文逐字存储]]模式，AAAK 和 Rooms 模式分数更低
- **质疑 3**：Benchmark 可复现性。官方回应：`benchmarks/` 目录下有完整运行器脚本

## 来源
- [[raw/articles/ai-tools/mempalace/mempalace_01_overview.md]] — MemPalace 深度解析系列总览篇
- [[raw/articles/ai-tools/mempalace/mempalace_07_benchmarks.md]] — MemPalace 深度解析第七篇：Benchmark 深度解析

## 相关
- [[MemPalace]] — used_by
- [[Mem0]] — used_by
- [[Zep]] — used_by
- [[Recall@K]] — uses
- [[LoCoMo]] — compares_to
- [[混合搜索]] — used_by
- [[LLM 路由]] — used_by
- [[精确短语引号提取]] — used_by
- [[人名权重增强]] — used_by
- [[记忆/怀旧模式识别]] — used_by
