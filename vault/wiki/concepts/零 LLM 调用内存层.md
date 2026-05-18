---
type: concept
title: 零 LLM 调用内存层
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["AI", "记忆系统", "性能优化", "架构设计", "Agent系统"]
aliases: ["Zero LLM Call Memory", "无 LLM 内存层"]
relates_to:
  - target: "[[MemPalace]]"
    type: implements
  - target: "[[确定性内存设计]]"
    type: extends
  - target: "[[上下文窗口]]"
    type: extends
supersedes: null
---

# 零 LLM 调用内存层

## 概述
AI 记忆系统的架构设计原则：在内存的写入和读取过程中不调用任何 LLM，所有分类、检测、压缩操作通过确定性[[算法]]（正则表达式、关键词评分）完成。

## 关键内容
- **核心原则**：内存层应该是确定性的、免费的、离线的。不依赖 LLM 做[[内存管理]]决策
- **技术实现**：所有 Room 检测、内容分类、压缩全部用正则表达式和关键词评分完成，无需 LLM 参与
- **与传统方案对比**：Mem0/Zep 在写入和读取时频繁调用 LLM 做信息提取和摘要；[[MemPalace]] 内存层零 LLM 调用
- **优势**：
  - 成本为零（无 API 调用费用）
  - 速度极快（无网络延迟）
  - 确定性行为（相同输入产生相同输出）
  - 完全离线运行
  - 可预测的性能表现
- **依赖极简**：仅 [[ChromaDB]]（向量存储）+ PyYAML（[[Configuration|配置]]），无 [[LangChain]]、LlamaIndex、[[OpenAI]] SDK

## 来源
- [[raw/articles/ai-tools/mempalace/mempalace_01_overview.md]] — MemPalace 系列总览篇

## 相关
- [[MemPalace]] — implements
- [[确定性内存设计]] — extends
- [[上下文窗口]] — extends
