---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: [AI Engineering, Retrieval Augmentation, LLM, context-engineering]
aliases: ["检索增强生成", "检索增强生成技术", "Retrieval-Augmented Generation", "RAG"]
relates_to:
  - {target: Context Engineering, type: part_of, confidence: 0.8}
  - {target: LLM, type: enhances, confidence: 0.9}
  - {target: Vector Database, type: uses, confidence: 0.9}
  - {target: Embedding, type: uses, confidence: 0.9}
  - {target: Semantic Search, type: uses, confidence: 0.8}
  - {target: Context Design, type: applies_to, confidence: 0.7}
supersedes: null
---

# RAG

## 概述
[[检索增强生成]]（Retrieval-Augmented Generation, RAG），一种结合信息检索和文本生成的技术[[规范化理论|范式]]，通过从外部知识库中检索相关信息来增强大[[Language-Model|语言模型]]的生成能力，解决模型知识更新、幻觉和私有数据访问等问题。在Context Design中，RAG被作为[[混合搜索|混合检索]]的重要组成部分。

## 关键内容

1. **核心架构**：
   - 检索器（Retriever）：负责从知识库中查找与查询相关的信息
   - [[生成器]]（[[生成器|Generator]]）：基于原始查询和检索到的信息生成最终响应
   - 知识库：存储待检索的文档集合，可以是文档、网页或结构化数据

2. **关键技术**：
   - 向量化：将文档和查询转换为高维向量表示
   - [[向量空间模型|向量检索]]：[[计算]]向量相似度以找到最相关的信息
   - 上下文拼接：将检索到的信息与原始查询拼接作为生成模型的输入

3. **主要优势**：
   - 解决模型知识时效性问题，无需重新训练即可接入最新信息
   - 减少模型幻觉，响应基于检索到的实际证据
   - 支持私有或领域特定知识的接入
   - 提供可追溯的信息来源，增强响应的可解释性

4. **变体技术**：
   - HyDE：先让LLM生成假设文档，再用假设文档检索
   - RAG-Fusion：多查询生成和倒排[[检索重排序|重排序]]
   - GraphRAG：结合知识图谱和[[向量空间模型|向量检索]]
   - RAPTOR：递归摘要树，解决超长文档检索

5. **在Context Design中的应用**：
   - 采用"按需检索 + [[混合搜索|混合检索]] + 重排 + 去重 + 反证位"的策略
   - 流程包括：query understanding → need_retrieval? → hybrid retrieve → contextualize → rerank → diversify → compress → assemble
   - 强制避免单一来源垄断，[[Settings|设置]]反证槽位防止早期锚定偏见

## 来源
- AI-Agent--02_context_engineering — Context Engineering核心技术体系中提及
- [[raw/articles/ai-engineering/prompt-context/context-design.md]] — 在Context Design中的应用
- [[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks]] — 原始论文

## 相关
- [[Context Engineering]] — part_of
- [[Context Design]] — applies_to
- [[LLM]] — enhances
- [[Vector Database]] — uses
- [[Embedding]] — uses
- [[Semantic Search]] — uses
- [[Self-RAG]] — relates_to
- [[RAPTOR]] — relates_to