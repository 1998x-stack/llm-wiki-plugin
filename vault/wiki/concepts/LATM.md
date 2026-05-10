---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [LLM, 工具生成, 双LLM架构]
aliases: ["Large Language Models as Tool Makers"]
relates_to: []
supersedes: null
---

# LATM

## 概述
LATM（[[Language-Model|Large Language Model]]s as Tool Makers）是由Cai等人提出的概念，提出双LLM架构来实现工具制造和工具使用的分离。该方法利用强推理能力的模型制造工具，用较小模型使用工具，从而在保证质量的同时降低成本。

## 关键内容

1. **双LLM架构**：
   - Tool Maker（如GPT-4）：负责接受任务描述并生成[[Python]]工具函数
   - [[Tool-Use|Tool Use]]r（如[[GPT-3]].5）：接受任务和工具函数，调用工具完成任务
   - 工具库（Tool Cache）：存储可复用的工具函数

2. **核心创新**：
   - 工具制造需要强推理能力（用GPT-4）
   - 工具使用可用更小的模型（用[[GPT-3]].5），降低推理成本
   - 同类任务只需制造一次工具，后续批量复用

3. **工具制造过程**：
   - 输入：若干同类型任务的示例
   - GPT-4生成可复用工具函数
   - 后续同类任务直接调用此工具，无需GPT-4参与

4. **实验结果**：
   - 在Big-Bench Hard（BBH）任务集上，LATM优于纯GPT-4 CoT
   - 成本约为纯GPT-4的1/7

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Paper]] — "Large Language Models as Tool Makers", ICLR 2024

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Tool-Making]] — relates_to
- [[Dual-LLM-Architecture]] — relates_to
- [[Tool-Reuse]] — relates_to