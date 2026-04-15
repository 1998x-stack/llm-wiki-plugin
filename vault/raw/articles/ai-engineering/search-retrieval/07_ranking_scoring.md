# 排序与评分执行策略
> Scoring, DAAT/TAAT & WAND — 深度解析系列 第 7 篇

---

## 1. 评分执行的核心问题

**目标：** 对给定查询 q，高效计算所有相关文档的 BM25/TF-IDF 得分，返回 Top-K 结果。

**核心挑战：**
```
语料库规模: 100亿文档
查询词条数: 5个词
每个词条 posting list 平均长度: 1亿条

朴素策略: 对所有词条在所有文档打分
  5 × 1亿 = 5亿次运算 → 无法满足毫秒级响应

需要：智能跳过不重要的文档
```

---

## 2. 两种基础遍历策略

### 2.1 TAAT（Term-At-A-Time）

**一次处理一个词条**，累积所有文档的得分：

```
查询: q = {cat, dog, fish}

Step 1: 处理词条 "cat"
  cat: [(d1, tf=3), (d3, tf=1), (d7, tf=2)]
  accumulator: {d1: 0.8, d3: 0.3, d7: 0.6}   ← 加 IDF(cat) × BM25-TF

Step 2: 处理词条 "dog"
  dog: [(d1, tf=1), (d4, tf=2), (d7, tf=1)]
  accumulator: {d1: 0.8+0.5=1.3, d3: 0.3, d4: 0.9, d7: 0.6+0.5=1.1}

Step 3: 处理词条 "fish"
  fish: [(d3, tf=1), (d7, tf=4)]
  accumulator: {d1: 1.3, d3: 0.3+0.4=0.7, d4: 0.9, d7: 1.1+1.2=2.3}

排序: d7(2.3) > d1(1.3) > d4(0.9) > d3(0.7)
```

**TAAT 的问题：**
- 需要维护所有文档的累积得分（Accumulator）
- 内存消耗大（可能需要存储数百万文档的累积分）
- 无法提前终止

### 2.2 DAAT（Document-At-A-Time）

**一次处理一篇文档**，对每篇文档计算所有词条的得分：

```
查询: q = {cat, dog, fish}

各 posting list（已排序）:
  cat:  [d1, d3, d7, d9]
  dog:  [d1, d4, d7, d11]
  fish: [d3, d7, d15]

游标（cursor）: 每个 posting list 维护一个指针

Step 1: 所有游标的最小文档 = d1
  计算 d1 的得分: BM25(cat, d1) + BM25(dog, d1) = 0.8 + 0.5 = 1.3
  推进 cat 和 dog 的游标

Step 2: 最小文档 = d3
  计算 d3 的得分: BM25(cat, d3) + BM25(fish, d3) = 0.3 + 0.4 = 0.7
  推进 cat 和 fish 的游标

Step 3: 最小文档 = d4
  计算 d4 的得分: BM25(dog, d4) = 0.9
  推进 dog 的游标

Step 4: 最小文档 = d7
  计算 d7 的得分: BM25(cat,d7) + BM25(dog,d7) + BM25(fish,d7) = 0.6+0.5+1.2 = 2.3
  推进所有游标

...

Top-K 维护: 使用最小堆维护当前 Top-K
```

**DAAT vs TAAT 对比：**

| 维度 | TAAT | DAAT |
|------|------|------|
| 内存 | O(N)（需要累加器） | O(Q)（Q=查询词条数） |
| 缓存友好 | 顺序访问单个 posting list | 跨 posting list 跳转 |
| 早期终止 | 困难 | 天然支持（配合WAND） |
| 短语查询 | 不方便 | 方便（游标同步） |
| 适用场景 | OR 查询、大量词条 | AND 查询、Top-K 检索 |

---

## 3. WAND（Weak And）算法

WAND 是 **DAAT 的优化版本**，通过上界估计跳过无法进入 Top-K 的文档。

### 3.1 WAND 核心思想

```
维护当前 Top-K 中的最低分（threshold θ）

对于每个候选文档 d：
  如果 d 的得分上界 ≤ θ：跳过（无法进入 Top-K）
  否则：精确计算得分

得分上界（Upper Bound）:
  UB(d, q) = Σ_{t∈q} max_score(t)
           = Σ_{t∈q} IDF(t) × (k₁ + 1)   ← BM25-TF 的最大值
```

### 3.2 WAND 算法详细步骤

```
初始化:
  - 各词条按当前文档 ID 排序（posting list 指针）
  - θ = 0（初始 Top-K 阈值）
  - 预计算每个词条的最大得分: max_score[t] = IDF(t) × (k₁+1)

主循环:
WHILE 任何 posting list 未到末尾:
  
  Step 1: 找 Pivot（关键步骤）
    将词条按当前指向的 doc_id 排序
    累加 max_score，找到第一个使累计值 > θ 的词条
    该词条的 doc_id = pivot_doc
    
    排序后词条: [fish(d3), cat(d7), dog(d11)]
    max_score:   [0.4,      0.8,     0.5]
    
    累计: 0.4 < θ? 继续
          0.4+0.8=1.2 > θ? 是 → pivot = cat, pivot_doc = d7
  
  Step 2: 检查 pivot_doc
    如果 pivot_doc 前面所有词条（max_score累计已>θ）的文档 ID = pivot_doc:
      → 这篇文档有可能进入 Top-K，精确计算得分
    否则:
      → 将所有文档ID < pivot_doc 的词条 advance 到 pivot_doc
  
  Step 3: 计算精确得分（当文档通过上界过滤）
    score = Σ_{t∈q, t包含pivot_doc} BM25(t, pivot_doc)
    
    如果 score > θ:
      加入 Top-K 堆
      θ = Top-K 堆中的最小分

Step 4: Advance 游标
  将参与计算的词条游标向前推进一位
```

### 3.3 WAND 跳过示例

```
查询: {machine, learning, python}
max_score: {machine:2.1, learning:1.8, python:1.4}
当前 θ = 2.5（已找到足够的 Top-K 文档）

Posting 游标当前指向:
  machine: d15 (max_score=2.1)
  learning: d15 (max_score=1.8)
  python: d42 (max_score=1.4)

按 doc_id 排序: [machine(d15), learning(d15), python(d42)]
累计 max_score: 2.1 < θ=2.5? 继续
                2.1+1.8=3.9 > θ=2.5? 是 → pivot = learning, pivot_doc = d15

检查: machine 和 learning 都指向 d15 ← 一致！
计算精确得分: score(d15) = BM25(machine,d15) + BM25(learning,d15)
              假设 = 1.5 + 1.2 = 2.7 > θ=2.5 → 加入 Top-K，θ 更新为 2.5（或新的最小值）

下一轮: python 仍指向 d42
  假设 max_score(python) = 1.4 < θ = 2.7 → python 对任何后续文档贡献最多 1.4
  如果其他词条 max_score 之和 + 1.4 < θ: 可以跳过大量文档！
```

### 3.4 WAND 性能

```
理论上：WAND 可以跳过高达 90%+ 的文档（取决于查询和语料）

实际上：
  普通 BM25 DAAT: 需要访问所有包含查询词的文档
  WAND: 只精确计算可能进入 Top-K 的文档
  
  加速比: 通常 5-20x（对于高 k₁ 或高 Top-K 阈值）
```

---

## 4. BMW（Block-Max WAND）

WAND 的进一步优化，利用**块级最大得分**实现更精确的上界：

### 4.1 Posting List 分块

```
将 posting list 按固定大小分块（如 128 个文档/块）:

机器学习 posting list:
  Block 1 [d1-d128]:   max_score_in_block = 3.2
  Block 2 [d129-d256]: max_score_in_block = 1.8
  Block 3 [d257-d384]: max_score_in_block = 2.1
  ...

当处理 Block 2 时:
  block_max = 1.8，如果 θ > 1.8 → 跳过整个块！
```

### 4.2 BMW vs WAND 对比

| 特性 | WAND | BMW |
|------|------|------|
| 上界粒度 | 词条级（全局最大） | 块级（局部最大） |
| 跳过精度 | 低（上界过于保守） | 高（更紧的上界） |
| 内存开销 | 低 | 较高（需存储块最大值） |
| 实现复杂度 | 中等 | 较高 |
| 加速效果 | 5-20x | 10-50x |
| 工业应用 | Lucene 历史版本 | Lucene 8+ 默认 |

---

## 5. Top-K 维护：最小堆

```python
import heapq
from typing import List, Tuple

class TopKHeap:
    """
    维护 Top-K 最高分文档的最小堆
    堆顶 = 当前 Top-K 中分数最低的文档
    """
    
    def __init__(self, k: int):
        self.k = k
        self.heap: List[Tuple[float, int]] = []  # (score, doc_id)
    
    @property
    def threshold(self) -> float:
        """当前 Top-K 阈值（最小分数）"""
        return self.heap[0][0] if len(self.heap) >= self.k else -float('inf')
    
    def push(self, score: float, doc_id: int) -> bool:
        """
        尝试将文档加入 Top-K
        返回: 是否成功加入
        """
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, (score, doc_id))
            return True
        elif score > self.heap[0][0]:
            heapq.heapreplace(self.heap, (score, doc_id))
            return True
        return False
    
    def get_results(self) -> List[Tuple[int, float]]:
        """获取 Top-K 结果（按分数降序）"""
        return [(doc_id, score) 
                for score, doc_id in sorted(self.heap, reverse=True)]


# 在 DAAT 中使用
def daat_bm25_topk(
    query_terms: List[str],
    index,          # InvertedIndex
    bm25: "BM25",
    k: int = 10
) -> List[Tuple[int, float]]:
    """
    DAAT BM25 Top-K 检索
    """
    # 获取所有查询词的 posting lists
    posting_lists = {}
    cursors = {}
    
    for term in query_terms:
        postings = index.get_postings(term)
        if postings:
            posting_lists[term] = postings
            cursors[term] = 0
    
    if not posting_lists:
        return []
    
    top_k = TopKHeap(k)
    
    while True:
        # 找所有游标的最小 doc_id
        active_terms = [
            t for t, idx in cursors.items()
            if idx < len(posting_lists[t])
        ]
        
        if not active_terms:
            break
        
        # 当前最小文档
        min_doc_id = min(
            posting_lists[t][cursors[t]].doc_id
            for t in active_terms
        )
        
        # 计算该文档的 BM25 得分
        score = 0.0
        terms_with_doc = []
        
        for term in active_terms:
            idx = cursors[term]
            posting = posting_lists[term][idx]
            
            if posting.doc_id == min_doc_id:
                # 这个词条在当前文档中
                idf = bm25._idf(term)
                tf_weight = bm25._tf_weight(
                    posting.term_freq,
                    index.doc_lengths[min_doc_id]
                )
                score += idf * tf_weight
                terms_with_doc.append(term)
                cursors[term] += 1  # 推进游标
        
        # 尝试加入 Top-K
        top_k.push(score, min_doc_id)
    
    return top_k.get_results()
```

---

## 6. 完整 WAND 实现

```python
import heapq
from typing import List, Tuple, Dict

class WANDBm25Retrieval:
    """
    WAND（Weak And）算法实现
    基于 BM25 评分的 Top-K 高效检索
    """
    
    def __init__(self, index, bm25):
        self.index = index
        self.bm25 = bm25
        
        # 预计算每个词条的最大可能得分
        # max_score(t) = IDF(t) × (k₁ + 1)
        self.term_max_scores: Dict[str, float] = {}
    
    def _get_term_max_score(self, term: str) -> float:
        """词条的最大可能 BM25 得分"""
        if term not in self.term_max_scores:
            idf = self.bm25._idf(term)
            # BM25-TF 的最大值是 k₁+1（当tf→∞, b=0）
            max_tf_score = self.bm25.k1 + 1
            self.term_max_scores[term] = idf * max_tf_score
        return self.term_max_scores[term]
    
    def search(self, query_terms: List[str], k: int = 10) -> List[Tuple[int, float]]:
        """
        WAND Top-K 检索
        """
        # 初始化各词条的游标
        postings = {}
        cursors = {}  # term → current index in posting list
        
        for term in set(query_terms):
            pl = self.index.get_postings(term)
            if pl:
                postings[term] = pl
                cursors[term] = 0
        
        if not postings:
            return []
        
        top_k = TopKHeap(k)
        docs_scored = 0  # 统计实际打分的文档数（评估效率用）
        docs_skipped = 0
        
        while True:
            # Step 1: 获取所有未结束的词条，按当前 doc_id 排序
            active = {
                t: postings[t][cursors[t]].doc_id
                for t in cursors
                if cursors[t] < len(postings[t])
            }
            
            if not active:
                break
            
            # 按 doc_id 排序
            sorted_terms = sorted(active.items(), key=lambda x: x[1])
            
            # Step 2: 找 Pivot
            threshold = top_k.threshold
            cumulative_max = 0.0
            pivot_idx = -1
            
            for i, (term, doc_id) in enumerate(sorted_terms):
                cumulative_max += self._get_term_max_score(term)
                if cumulative_max > threshold:
                    pivot_idx = i
                    break
            
            if pivot_idx == -1:
                # 所有词条的最大得分之和 ≤ 阈值 → 终止
                break
            
            pivot_term, pivot_doc_id = sorted_terms[pivot_idx]
            
            # Step 3: 检查 pivot_doc 之前的词条
            all_at_pivot = all(
                doc_id >= pivot_doc_id 
                for _, doc_id in sorted_terms[:pivot_idx]
            )
            
            if all_at_pivot:
                # pivot_doc 可能进入 Top-K，精确计算
                score = self._compute_exact_score(pivot_doc_id, postings, cursors)
                docs_scored += 1
                top_k.push(score, pivot_doc_id)
                
                # 推进所有指向 pivot_doc 的游标
                for term in list(cursors.keys()):
                    if (cursors[term] < len(postings[term]) and 
                            postings[term][cursors[term]].doc_id == pivot_doc_id):
                        cursors[term] += 1
            else:
                # 将前面的词条游标推进到 pivot_doc_id
                docs_skipped += 1
                for term, doc_id in sorted_terms[:pivot_idx]:
                    if doc_id < pivot_doc_id:
                        # 跳跃到 ≥ pivot_doc_id 的位置
                        cursors[term] = self._advance_to(
                            postings[term], cursors[term], pivot_doc_id
                        )
        
        # 打印效率统计
        total = docs_scored + docs_skipped
        if total > 0:
            skip_rate = docs_skipped / total * 100
            print(f"WAND 统计: 打分={docs_scored}, 跳过={docs_skipped}, "
                  f"跳过率={skip_rate:.1f}%")
        
        return top_k.get_results()
    
    def _compute_exact_score(self, doc_id: int, postings: Dict, cursors: Dict) -> float:
        """精确计算文档得分"""
        score = 0.0
        doc_length = self.index.doc_lengths.get(doc_id, self.index.avgdl)
        
        for term, pl in postings.items():
            idx = cursors[term]
            if idx < len(pl) and pl[idx].doc_id == doc_id:
                tf = pl[idx].term_freq
                idf = self.bm25._idf(term)
                tf_w = self.bm25._tf_weight(tf, doc_length)
                score += idf * tf_w
        
        return score
    
    def _advance_to(self, posting_list: List, start: int, target_doc_id: int) -> int:
        """
        二分查找：将游标推进到第一个 doc_id ≥ target_doc_id 的位置
        O(log n) 复杂度（比线性扫描快）
        """
        lo, hi = start, len(posting_list)
        while lo < hi:
            mid = (lo + hi) // 2
            if posting_list[mid].doc_id < target_doc_id:
                lo = mid + 1
            else:
                hi = mid
        return lo
```

---

## 7. 评分系统的架构设计

### 7.1 两阶段检索（Recall + Rank）

```
第一阶段（First-Stage Retrieval）: 高效召回
  BM25 / WAND → Top-1000 候选文档
  目标: 不漏掉相关文档（高召回）
  延迟要求: < 20ms

第二阶段（Re-ranking）: 精确排序
  对 Top-1000 进行精确评分
  使用更昂贵的特征:
    - 点击率、停留时间、新鲜度
    - PageRank、链接权威性
    - 个性化信号（用户历史）
    - 语义相关度（BERT re-ranker）
  延迟要求: < 100ms

最终展示: Top-10
```

### 7.2 特征工程（传统 LTR）

```
查询-文档特征（Query-Document Features）:
  tf_idf_score           TF-IDF 得分
  bm25_score             BM25 得分
  query_term_coverage    查询词覆盖率
  min_span               查询词最小距离
  field_specific_bm25    各字段 BM25

文档特征（Document Features）:
  pagerank               PageRank 分数
  inlink_count           入链数量
  doc_length             文档长度
  url_depth              URL 深度
  content_freshness      内容新鲜度

查询特征（Query Features）:
  query_length           查询长度
  query_frequency        查询频率（热门查询）
  is_navigational        是否导航型查询

交互特征（Interaction Features）:
  click_rate             点击率
  dwell_time             停留时间
  bounce_rate            跳出率

LTR 模型: LambdaMART（梯度提升树）
```

---

## 8. 评估指标实现

```python
from typing import List, Dict
import math

def ndcg_at_k(ranked_docs: List[int], relevance: Dict[int, int], k: int) -> float:
    """
    NDCG@K (Normalized Discounted Cumulative Gain)
    
    Args:
        ranked_docs: 按排名顺序的文档ID列表
        relevance: {doc_id: relevance_score} (0-3, 越高越相关)
        k: 截断位置
    
    Returns: NDCG@K 值（0-1）
    """
    def dcg(docs: List[int], rel: Dict[int, int], k: int) -> float:
        return sum(
            rel.get(doc_id, 0) / math.log2(i + 2)  # i+2 因为 i 从0开始
            for i, doc_id in enumerate(docs[:k])
        )
    
    actual_dcg = dcg(ranked_docs, relevance, k)
    
    # 理想排名（按相关性降序）
    ideal_docs = sorted(relevance.keys(), key=lambda d: relevance[d], reverse=True)
    ideal_dcg = dcg(ideal_docs, relevance, k)
    
    if ideal_dcg == 0:
        return 0.0
    
    return actual_dcg / ideal_dcg


def map_score(
    results_per_query: List[List[int]],  # 每个查询的排名结果
    relevant_per_query: List[set],        # 每个查询的相关文档集合
) -> float:
    """MAP (Mean Average Precision)"""
    
    def average_precision(ranked: List[int], relevant: set) -> float:
        if not relevant:
            return 0.0
        precisions = []
        hits = 0
        for i, doc_id in enumerate(ranked):
            if doc_id in relevant:
                hits += 1
                precisions.append(hits / (i + 1))
        return sum(precisions) / len(relevant)
    
    ap_scores = [
        average_precision(results, relevant)
        for results, relevant in zip(results_per_query, relevant_per_query)
    ]
    
    return sum(ap_scores) / len(ap_scores)


def mrr(results_per_query: List[List[int]], relevant_per_query: List[set]) -> float:
    """MRR (Mean Reciprocal Rank)"""
    
    def reciprocal_rank(ranked: List[int], relevant: set) -> float:
        for i, doc_id in enumerate(ranked):
            if doc_id in relevant:
                return 1.0 / (i + 1)
        return 0.0
    
    rr_scores = [
        reciprocal_rank(results, relevant)
        for results, relevant in zip(results_per_query, relevant_per_query)
    ]
    
    return sum(rr_scores) / len(rr_scores)


# 示例
ranked = [3, 1, 4, 2, 5, 6, 7, 8, 9, 10]
relevance = {1: 3, 2: 2, 3: 1, 5: 3}  # 相关文档及其相关性分数

print(f"NDCG@5: {ndcg_at_k(ranked, relevance, 5):.4f}")
print(f"MAP: {map_score([ranked], [set(relevance.keys())]):.4f}")
print(f"MRR: {mrr([ranked], [set(relevance.keys())]):.4f}")
```

---

*© 传统搜索引擎深度解析系列 — 第 7 篇 / 8*
