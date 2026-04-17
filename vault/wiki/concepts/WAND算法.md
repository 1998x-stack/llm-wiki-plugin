---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [AI工程]
aliases: ["WAND", "Weak And", "BMW", "Block-Max WAND", "DAAT", "TAAT"]
relates_to:
  - target: "BM25"
    type: uses
    confidence: 0.95
  - target: "[[倒排索引]]"
    type: uses
    confidence: 0.9
  - target: "[[搜索引擎架构]]"
    type: part_of
    confidence: 0.85
  - target: "[[查询处理]]"
    type: implements
    confidence: 0.9
supersedes: null
---

# WAND算法

## 概述

WAND（Weak And）是 DAAT（Document-At-A-Time）遍历策略的优化版本，通过维护 Top-K 当前最低分作为阈值 θ，利用词条得分上界快速跳过不可能进入 Top-K 的文档，通常可跳过 70-95% 的文档。

## 关键内容

1. **两种基础遍历策略对比**：
   - **TAAT（Term-At-A-Time）**：一次处理一个词条，累积所有文档得分到 Accumulator。内存 O(N)，无法提前终止，适合 OR 查询。
   - **DAAT（Document-At-A-Time）**：每个词条维护游标，每轮处理所有游标最小文档，计算该文档完整得分。内存 O(Q)，配合 WAND 可提前终止，适合 AND/Top-K 检索。

2. **WAND 核心步骤**：
   - 预计算每词条最大得分：`max_score(t) = IDF(t) × (k₁+1)`（BM25-TF 上界）
   - 维护当前 Top-K 最低分阈值 θ
   - 每轮：将词条按当前指向 doc_id 排序 → 累加 max_score 找到第一个使累计 > θ 的词条（Pivot）→ 若 Pivot doc_id 之前词条也指向同一文档则精确计算；否则将前面词条游标跳进到 Pivot doc_id → 更新 θ

3. **BMW（Block-Max WAND）**：将 Posting List 分成固定大小块（128 doc/块），存储每块的局部最大得分。上界更紧（块级而非全局），跳过精度更高。Lucene 8+ 默认使用，加速比 10-50x vs 普通 WAND 5-20x。

4. **Top-K 最小堆维护**：用最小堆维护当前 Top-K，堆顶是最低分文档。新文档得分 > 堆顶才能替换入堆，同时更新 θ。

5. **性能**：理论上跳过 70-95%+ 文档；Lucene/Elasticsearch 生产验证，对高 Top-K 阈值和高 k₁ 场景效果最显著。

6. **两阶段检索架构（工业实践）**：
   - 第一阶段：BM25+WAND → Top-1000，目标高召回，延迟 < 20ms
   - 第二阶段：精确重排（点击率/PageRank/个性化/BERT reranker），延迟 < 100ms，返回 Top-10

## 来源

- `raw/articles/ai-engineering/search-retrieval/07_ranking_scoring.md` — 传统搜索引擎深度解析系列 第7篇

## 相关

- BM25 — uses
- [[倒排索引]] — uses
- [[查询处理]] — implements
- [[学习排序]] — compares_to
