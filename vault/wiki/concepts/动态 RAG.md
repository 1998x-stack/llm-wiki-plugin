---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [检索增强生成, 多Agent系统, 信息检索, AI工程]
aliases: ["Dynamic RAG", "动态检索增强生成"]
relates_to:
  - name: RAG 系统
    relation: extends
  - name: 多 Agent 系统
    relation: part_of
  - name: 上下文工程
    relation: relates_to
supersedes: null
---

# 动态 RAG

## 概述
动态 RAG 是一种[[检索增强生成]]模式，系统在多步搜索中动态发现相关信息，并根据新发现实时适应搜索策略，而非预先检索后静态注入上下文。

## 关键内容

1. **与传统 RAG 的区别**：传统 RAG 采用"预先检索 → 静态注入上下文 → 一次生成"的线性流程；动态 RAG 则支持迭代式多步搜索，每步搜索结果都会影响后续搜索策略。

2. **核心特征**：
   - **动态发现**：信息不是预先确定的，而是在搜索过程中逐步发现
   - **策略适应**：根据新发现的信息调整后续搜索方向和方法
   - **迭代分析**：多轮检索与分析交替进行，逐步生成高质量答案

3. **在研究系统中的应用**：[[Anthropic]] 的 Research 功能采用动态 RAG 模式，[[多 Agent 系统]]通过[[子 Agent & 多 Agent 系统|子 Agent]] 并行探索不同方向，每个[[子 Agent & 多 Agent 系统|子 Agent]] 独立进行动态检索，再将压缩后的信息传递给主 Agent 综合。

4. **[[信息论]]优势**：动态 RAG 的本质是信息压缩——从海量语料中提炼洞见，[[子 Agent & 多 Agent 系统|子 Agent]] 在独立[[上下文窗口]]中并行探索，压缩信息后再传递给主 Agent，减少路径依赖，避免陷入局部最优。

## 来源
- [[05_multi_agent_research]] — 第二节：架构设计（动态 RAG vs 静态 RAG）

## 相关
- [[RAG 系统]] — extends
- [[多 Agent 系统]] — part_of
- [[上下文工程]] — relates_to
- [[先广后深搜索策略]] — relates_to
