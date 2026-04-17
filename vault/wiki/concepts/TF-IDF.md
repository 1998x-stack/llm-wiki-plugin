---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [AI工程]
aliases: ["Term Frequency-Inverse Document Frequency", "词条频率-逆文档频率", "TFIDF"]
relates_to:
  - target: "BM25"
    type: extends
    confidence: 0.95
  - target: "[[向量空间模型]]"
    type: implements
    confidence: 0.9
  - target: "[[倒排索引]]"
    type: uses
    confidence: 0.9
  - target: "[[搜索引擎架构]]"
    type: part_of
    confidence: 0.85
supersedes: null
---

# TF-IDF

## 概述

TF-IDF（Term Frequency–Inverse Document Frequency）是信息检索最经典的词条权重方法：TF 衡量词条在**当前文档**的重要性，IDF 衡量词条在**整个语料库**的区分能力，两者相乘得到最终权重。

## 关键内容

1. **核心直觉**：
   - **TF（词频）**："词在文档中出现越多，对该文档主题越重要"
   - **IDF（逆文档频率）**："词出现在越多文档中，区分能力越弱，权重越低"
   - **TF-IDF**：寻找在当前文档高频但在语料库低频的词，最能代表文档独特主题。

2. **TF 变体**：
   - 原始计数：`count(t, d)`，长文档偏置
   - 对数归一化：`log(1 + count)`（最常用），边际效用递减
   - 增强：`0.5 + 0.5 × count/max_count(d)`，归一化到 [0.5, 1]
   - 布尔：仅 0/1，完全忽略频次

3. **IDF 变体**：
   - 标准：`log(N/df)` — Karen Spärck Jones 1972
   - 平滑：`log((N+1)/(df+1)) + 1` — sklearn 默认，避免零值
   - 概率：`log((N-df)/df)` — BM25 中使用
   - BM25 IDF：`log((N-df+0.5)/(df+0.5)+1)` — 最稳健

4. **[[向量空间模型]]（VSM）**：每篇文档表示为 TF-IDF 权重向量，用**余弦相似度**（而非欧氏距离）计算查询-文档相关性。余弦相似度消除文档长度影响：`cos(q, d) = q⃗·d⃗ / (‖q‖‖d‖)`。实践中对文档向量预先 L2 归一化，查询时只需点积。

5. **SMART 表示法**：三字母编码 TF变体][IDF变体][归一化]，如 `lnc-ltc`（文档用 log-TF 无IDF 余弦归一化，查询用 log-TF 标准IDF 余弦归一化）。

6. **局限**：词袋模型（忽略词序）；语义盲区（car ≠ automobile）；长文档偏置（L2 归一化只部分缓解）。BM25 显式引入 TF 饱和函数和长度归一化参数解决后两个问题。

7. **Zipf 定律关联**：自然语言词频满足 Zipf 分布（频率 × 排名 ≈ 常数），IDF 自然补偿了这种偏斜——高频词 IDF 低，低频词 IDF 高。

## 来源

- `raw/articles/ai-engineering/search-retrieval/04_tfidf.md` — 传统搜索引擎深度解析系列 第4篇

## 相关

- BM25 — extends（BM25 是 TF-IDF 的概率框架升级）
- [[向量空间模型]] — implements
- [[倒排索引]] — uses
- [[搜索引擎架构]] — part_of
