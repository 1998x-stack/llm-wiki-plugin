---
type: tool
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [RAG, 评估, 工具, AI工程]
aliases: ["RAG Assessment", "RAG评估工具"]
relates_to:
  - target: "[[LlamaIndex]]"
    type: related
    confidence: 0.75
  - target: "[[LangChain]]"
    type: related
    confidence: 0.7
  - target: "[[Context-Engineering]]"
    type: supports
    confidence: 0.8
  - target: "[[Quality Assurance]]"
    type: implements
    confidence: 0.85
supersedes: null
---

# RAGAs

## 概述
RAGAs是专门用于RAG（检索增强生成）系统评估的工具，提供专项的RAG评估指标和框架。

## 关键内容

1. **评估维度**：
   - 检索质量：评估检索组件返回的相关性
   - 生成质量：评估最终生成答案的准确性
   - 整体效果：综合评估RAG系统的表现

2. **核心指标**：
   - Faithfulness：生成内容与检索信息的一致性
   - Answer Relevancy：答案与问题的相关性
   - Context Precision：检索上下文的精确度

3. **应用价值**：
   - 量化RAG系统性能
   - 识别系统瓶颈和改进方向
   - 自动化质量保障流程

## 来源
- [[Context-Engineering]] — 评估工具介绍
- [[LLM-工程三阶段]] — 质量保障方式

## 相关
- [[LlamaIndex]] — relates_to
- [[LangChain]] — relates_to
- [[Context-Engineering]] — relates_to
- [[Quality Assurance]] — relates_to