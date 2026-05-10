---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [LLM, 工具调用, 大规模工具, 工具检索]
aliases: ["ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs"]
relates_to: []
supersedes: null
---

# ToolBench

## 概述
ToolBench是由Qin等人提出的大型工具调用基准和框架，涵盖RapidAPI上的49类、16,464个真实API，构建了268,000条工具使用指令和多工具协作场景。ToolLLM是基于ToolBench微调的模型。

## 关键内容

1. **数据集规模**：
   - 覆盖49类、16,464个真实API
   - 268,000条工具使用指令
   - 包含多工具协作场景（需要3-5个API组合完成）

2. **核心技术：DFSDT**：
   - DFSDT（深度优先搜索[[决策树]]）：将工具调用建模为[[决策树]]搜索
   - 遇到工具调用失败时，不是无脑重试，而是系统性探索替代路径
   - 与传统[[ReAct]]线性方式不同，支持回溯和路径探索

3. **评估指标ToolEval**：
   - 通过率（Pass Rate）：任务是否成功完成
   - 偏好胜率（Win Rate）：人类偏好哪个解决方案（相对于[[ChatGPT]]-[[ReAct]]）

4. **实验结果**：
   - Tool[[LLaMA]]在Win Rate上达到[[ChatGPT]]的83%
   - 证明了大规模工具调用的可行性

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Paper]] — "ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs", ICLR 2024

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Large-Scale-Tools]] — relates_to
- [[Tool-Retrieval]] — relates_to
- [[Tool-Evaluation]] — relates_to