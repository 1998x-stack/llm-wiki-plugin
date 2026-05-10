---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [AI工程]
aliases: ["Cross-encoder", "Bi-encoder", "双编码器", "跨编码器", "重排器架构"]
relates_to:
  - target: "[[检索重排序]]"
    type: implements
    confidence: 0.95
  - target: "[[Embedding]]"
    type: compares_to
    confidence: 0.9
  - target: "[[近似最近邻检索]]"
    type: compares_to
    confidence: 0.85
  - target: "BM25"
    type: compares_to
    confidence: 0.8
supersedes: null
---

# Cross-encoder与Bi-encoder

## 概述

Bi-encoder（双编码器）和 Cross-encoder（跨编码器）是检索-重排两阶段架构的核心组件：Bi-encoder 独立编码查询和文档生成向量，速度快适合初检；Cross-encoder 联合编码，精度高适合[[检索重排序|精排]]。

## 关键内容

1. **本质区别**：
   - **Bi-encoder**：`score(q,d) = cos(E_q(q), E_d(d))`。文档向量**离线预[[计算]]并固定**，与查询无关。查询时只需[[计算]]查询向量再做 ANN 检索。本质是"在共享向量空间找几何最近点"。
   - **Cross-encoder**：`score(q,d) = f([q;d])`。将查询和文档拼接输入模型，**文档的表示随查询动态变化**。输出直接是相关性分数，无需向量空间。

2. **为什么 Bi-encoder 不如 Cross-encoder**：Bi-encoder 的文档向量在离线阶段固定，无法捕捉"同一文档在不同查询语境下的不同相关性"。Cross-encoder 的 full attention 可以捕捉 query 和 doc 之间的细粒度交互（指代消解、隐含约束、多跳语义关联）。

3. **大模型重排（LLM as reranker）优势**：BGE reranker（专用 cross-encoder）的能力边界集中在"相关性匹配"。大模型（GPT-4/[[Claude_Code|Claude]]/Qwen）预训练见过海量模式，能处理：
   - 同义改写、隐含约束
   - 世界知识和任务常识（"糖尿病患者能不能吃这个"）
   - 长上下文关键信息定位
   - 含糊需求的真实意图识别
   大模型更像"先理解问题，再判断是否相关"，专用 reranker 更像"高水平匹配器"。

4. **实践架构（两阶段）**：
   - 第一阶段：Bi-encoder（BGE/E5/text-embedding）+ ANN（[[Faiss|FAISS]]/Milvus）→ Top-100，延迟 < 20ms
   - 第二阶段：Cross-encoder（BGE-reranker/LLM）[[检索重排序|精排]] Top-100 → Top-10，延迟 < 100ms

5. **BGE reranker 特点**：BAAI 开源，基于 BERT 架构的 Cross-encoder，专门针对检索重排任务微调。在 MTEB benchmark 上性能优秀，但在需要世界知识和复杂推理的场景不如大模型。

## 来源

- `raw/articles/ai-engineering/search-retrieval/ChatGPT-BGE reranker 与 embedding区别.md`
- `raw/articles/ai-engineering/search-retrieval/ChatGPT-大模型重排优势分析.md`

## 相关

- [[检索重排序]] — implements（具体实现架构）
- [[Embedding]] — compares_to
- [[近似最近邻检索]] — compares_to（Bi-encoder 配合 ANN）
- BM25 — compares_to（稀疏 vs 稠密第一阶段召回）
