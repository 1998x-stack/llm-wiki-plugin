---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [LLM, 工具调用, 层次化检索, 自反思, AI工程]
aliases: ["AnyTool: Self-Reflective, Large-Scale API Usage without Exhaustive Testing"]
relates_to: []
supersedes: null
---

# AnyTool

## 概述
AnyTool是由Du等人提出的自反思大规模API使用框架，无需穷举测试即可处理数千个API。其核心创新是层次化工具检索和自反思机制，解决了大规模工具库中的检索噪声问题。

## 关键内容

1. **层次化检索机制**：
   - L1：API类别检索（49类 → Top-5类）
   - L2：类别内工具检索（每类 → Top-10工具）
   - L3：工具参数匹配（精确对齐）

2. **自反思机制**：
   - 若初次检索结果无法完成任务，启动Self-Reflection
   - 分析失败原因（工具不存在？参数错误？类别判断偏差？）
   - 在相邻类别中扩大检索范围

3. **技术优势**：
   - 无需任务特定微调，在[[ToolBench]]测试集上通过率超过Tool[[LLaMA]] 12%
   - 检索效率高：平均只需遍历全量工具的3%
   - 通过自反思机制提升工具调用成功率

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Paper]] — "AnyTool: Self-Reflective, Large-Scale API Usage without Exhaustive Testing", 2024

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Large-Scale-Tools]] — relates_to
- [[Hierarchical-Retrieval]] — relates_to
- [[Self-Reflection]] — relates_to
- [[Tool-Retrieval]] — relates_to