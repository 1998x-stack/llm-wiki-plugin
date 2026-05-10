---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [LLM, 工具调用, 代码复用, 检索增强]
aliases: ["Customized LLM Agents Through Retrieval and Reuse of Code"]
relates_to: []
supersedes: null
---

# CRAFT

## 概述
CRAFT（Customized L[[LM Agent]]s Through Retrieval and Reuse of Code）是由Yuan等人提出的系统，通过检索和重用代码片段来定制LLM代理。其核心思想是维护一个代码片段库，在新任务时检索相关代码并进行组合。

## 关键内容

1. **核心问题**：
   - 每次遇到相似任务都让LLM从头生成代码是巨大浪费
   - 需要维护可复用的代码片段库，以提高效率和一致性

2. **系统流程**：
   - 语义检索代码库获取相关的Top-K代码片段
   - LLM（如GPT-4）组合和适配代码片段
   - 执行验证，成功则存入代码库供未来检索，失败则反馈重新生成

3. **代码库条目格式**：
   - 任务描述（用于语义检索）
   - 代码片段
   - 验证状态
   - 使用次数统计

4. **关键技术贡献**：
   - 实现了代码片段的动态积累和检索
   - 代码复用率随任务数增加而提升
   - 在TabMWP和MATH数据集上比PoT基线提升4-7%

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Paper]] — "CRAFT: Customized LLM Agents Through Retrieval and Reuse of Code", 2023

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Code-Reuse]] — relates_to
- [[Retrieval-Based-Generation]] — relates_to
- [[Code-Library]] — relates_to