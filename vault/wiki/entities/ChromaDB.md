---
type: entity
title: "ChromaDB"
status: active
confidence: 0.85
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [工具, 数据库, AI, 向量搜索]
aliases: ["Chroma", "chroma-db"]
relates_to:
  - target: "[[Claude-Mem]]"
    type: related_to
    confidence: 0.9
  - target: "[[SQLite]]"
    type: related_to
    confidence: 0.7
supersedes: null
---

# ChromaDB

## 概述
ChromaDB 是一个开源的向量数据库（Vector Database），专为 AI/LLM 应用设计，用于存储和检索向量嵌入（Embeddings）。它支持语义搜索——将文本转换为高维向量后，按语义相似度检索，而非关键词匹配。在 [[Claude-Mem]] 中，ChromaDB 作为可选的向量存储后端，为记忆检索提供语义搜索能力，补充 [[SQLite]] 的 [[FTS5]] 关键词搜索。

## 关键内容
- **核心功能**：存储文档及其向量嵌入；支持近似最近邻（ANN）相似度搜索；支持元数据过滤
- **部署模式**：本地内存模式（测试）、持久化磁盘模式（生产）、HTTP 客户端/服务端模式
- **与传统数据库对比**：[[SQLite]]/[[FTS5]] 适合精确关键词匹配；ChromaDB 适合语义相似度检索（"找意思相近的记忆"）
- **生态**：与 LangChain、LlamaIndex 等 RAG 框架深度集成

## 来源
- 综合自 wiki 内部引用（Claude-Mem 等页面）

## 相关
- [[Claude-Mem]]
- [[SQLite]]
- [[FTS5]]
