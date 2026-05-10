---
type: concept
status: active
confidence: 0.5
created: 2026-04-19
updated: 2026-04-19
last_accessed: 2026-04-19
source_count: 1
tags: [技术, 方法论]
aliases: [KG-RAG, 知识图谱+RAG, GraphRAG]
relates_to:
  - 检索增强生成
  - 多跳推理
  - 知识图谱
supersedes: null
---

# 知识图谱增强RAG

## 概述
在RAG系统中引入知识图谱，从数据治理根源上建立知识点与知识点、文档块与文档块之间的连接关系，解决纯检索方案无法处理多跳推理的核心痛点。是RAG落地的第三阶段专项破局方案。

## 关键内容
1. **落地逻辑**：向量检索获取用户query对应的初始节点 → 基于知识图谱对初始节点做上下关系拓展获取完整关联信息层 → 节点过多时引入大模型做过滤 → 将筛选后的完整关联信息交给大模型生成答案。
2. **一层拓展策略**：工业界落地只做一层节点拓展就终止，核心原因是时间成本和Token成本。一层拓展在测试集上已能解决85%+多跳问题，单点问题回答准确率达95%+。
3. **三路检索融合**：最终形成向量+关键词+知识图谱的三路检索融合方案，在成本可控前提下实现效果最大化。
4. **与Agentic Search的对比**：Claude Code的自主检索让AI自己判断需要什么信息、检索多少次、何时信息足够，效果上限极高但商用场景无法接受其Token消耗和响应时长。

## 来源
- [[raw/articles/essays/thinking-series/011-算法面试]] — 智慧树RAG项目实战拆解

## 相关
- [[检索增强生成]] — extends
- [[多跳推理]] — implements
- [[知识图谱]] — uses
- [[Agentic Search]] — compares_to
