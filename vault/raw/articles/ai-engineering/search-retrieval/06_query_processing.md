# 查询处理（Query Processing）
> Query Parsing, Expansion & Execution — 深度解析系列 第 6 篇

---

## 1. 查询处理全流水线

```
用户原始输入: "机器学系推荐系统 python"
        │
        ▼
┌──────────────────────────────────────────────────────┐
│                 查询分析层                             │
│                                                      │
│  意图识别  →  拼写纠错  →  词条化  →  停用词过滤        │
│   (Intent)    (Spelling)  (Tokenize) (Stop Words)   │
└──────────────────────────────────────────────────────┘
        │
        ▼ "机器学习 推荐系统 python"（纠错后）
┌──────────────────────────────────────────────────────┐
│                 查询重写层                             │
│                                                      │
│  同义词扩展  →  查询扩展  →  查询松弛                  │
│  (Synonyms)   (Expansion) (Relaxation)              │
└──────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────┐
│                 查询执行层                             │
│                                                      │
│  索引查找  →  Posting 合并  →  早期终止               │
│  (Lookup)     (Merging)    (Early Termination)      │
└──────────────────────────────────────────────────────┘
        │
        ▼
排名结果列表
```

---

## 2. 查询意图识别（Query Intent Classification）

### 2.1 三类基本意图（Broder 2002）

```
信息型（Informational）：
  目标：获取关于某主题的信息
  示例："什么是机器学习" / "BM25 原理"
  期望：解释性文档、百科页面

导航型（Navigational）：
  目标：找到特定网站或页面
  示例："GitHub TensorFlow" / "Elasticsearch 官方文档"
  期望：目标网站的首页/官方页面

事务型（Transactional）：
  目标：完成某个操作（购买、下载等）
  示例："下载 Python 3.11" / "购买机械键盘"
  期望：可直接交互的页面
```

### 2.2 意图识别对处理策略的影响

| 意图类型 | 拼写纠错 | 同义词扩展 | 结果类型 |
|---------|---------|---------|---------|
| 信息型 | 强力纠错 | 积极扩展 | 多样化文档 |
| 导航型 | 保守（品牌名不改） | 几乎不扩展 | 精确匹配 |
| 事务型 | 适度纠错 | 适度扩展 | 功能性页面 |

---

## 3. 拼写纠错（Spelling Correction）

### 3.1 编辑距离（Edit Distance / Levenshtein Distance）

编辑距离 = 将字符串 A 转换为字符串 B 所需的**最少操作数**（插入/删除/替换）：

```
操作:
  插入（Insert）:  "cat" → "cart"  (插入 r)
  删除（Delete）:  "cart" → "cat"  (删除 r)
  替换（Replace）: "cat" → "bat"   (c→b)

计算 edit_distance("machin", "machine"):
        m  a  c  h  i  n  e
     ┌──┬──┬──┬──┬──┬──┬──┬──┐
     │0 │1 │2 │3 │4 │5 │6 │7 │
   m │1 │0 │1 │2 │3 │4 │5 │6 │
   a │2 │1 │0 │1 │2 │3 │4 │5 │
   c │3 │2 │1 │0 │1 │2 │3 │4 │
   h │4 │3 │2 │1 │0 │1 │2 │3 │
   i │5 │4 │3 │2 │1 │0 │1 │2 │
   n │6 │5 │4 │3 │2 │1 │0 │1 │
     └──┴──┴──┴──┴──┴──┴──┴──┘
     
edit_distance = 1（只差一个字符 e）
```

**动态规划实现：**

```python
def edit_distance(s1: str, s2: str) -> int:
    """Levenshtein 编辑距离，O(mn) 时间复杂度"""
    m, n = len(s1), len(s2)
    
    # dp[i][j] = s1[:i] 和 s2[:j] 的编辑距离
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 初始化
    for i in range(m + 1):
        dp[i][0] = i  # 删除 i 个字符
    for j in range(n + 1):
        dp[0][j] = j  # 插入 j 个字符
    
    # 状态转移
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # 字符相同，无需操作
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # 删除 s1[i-1]
                    dp[i][j-1],    # 插入 s2[j-1]
                    dp[i-1][j-1],  # 替换
                )
    
    return dp[m][n]

# 示例
print(edit_distance("machin", "machine"))  # → 1
print(edit_distance("receieve", "receive")) # → 1
print(edit_distance("pytohn", "python"))   # → 2
```

### 3.2 K-gram 索引加速拼写候选搜索

**问题：** 遍历整个词典计算编辑距离太慢（O(词典大小 × query_len)）

**解决：** K-gram 索引快速过滤候选

```
词: "cat"
3-gram 集合（边界字符 $）: {$ca, cat, at$}

词典建立 3-gram 倒排索引:
  $ca → [cat, can, car, cap, ...]
  cat → [cat, scatter, concatenate, ...]
  at$ → [cat, bat, hat, mat, rat, ...]

查询 "cta"（可能的拼写错误）:
  3-gram: {$ct, cta, ta$}
  
  $ct → []
  cta → [dictate, ...]
  ta$ → [data, delta, meta, beta, ...]
  
  候选 = union({$ct ∩ cta ∩ ta$}) 或 overlap 超过阈值的词

Jaccard 相似度过滤:
  J("cta", "cat") = |gram("cta") ∩ gram("cat")| / |gram("cta") ∪ gram("cat")|
                  = |{ta$}| / |{$ct, cta, ta$, $ca, cat, at$}|
                  = 1/6 ≈ 0.167  ← 太低，可能不是候选

  J("cta", "eta") = 高  ← 更好的候选
```

### 3.3 语言模型拼写纠错

现代方案：Noisy Channel Model（噪声信道模型）

```
P(intended | observed) ∝ P(observed | intended) × P(intended)
                         └───────────────────────┘  └─────────┘
                              信道模型（混淆概率）     语言模型先验

最优纠错: intended* = argmax_w [P(observed|w) × P(w)]

P(observed|w): 键盘混淆矩阵（哪些键容易被误敲）
P(w): 词的先验概率（词频）

示例:
  observed = "recieve"
  候选: {receive, relieve, retrieve, ...}
  
  P("recieve" | "receive") = 高（ie/ei 是常见混淆）
  P("receive") = 高（常用词）
  → "receive" 最可能的纠错
```

### 3.4 工业级拼写纠错系统

```
Stage 1: 快速过滤
  - 检查词典（存在则跳过）
  - K-gram Jaccard 过滤候选集

Stage 2: 候选评分
  - 编辑距离（≤2）
  - 语音相似度（Soundex/Metaphone）
  - 键盘相邻度（a和s相邻，容易误敲）

Stage 3: 上下文感知排序
  - n-gram 语言模型
  - 查询日志中的共现

Stage 4: 上下文决策
  - "Did you mean: ...?"（软纠错，展示建议）
  - 自动替换（硬纠错，置信度高时）
```

---

## 4. 查询扩展（Query Expansion）

### 4.1 基于关联规则的扩展

```
词条关联规则（从点击日志挖掘）:
  用户搜索 "机器学习" → 点击含 "ML" 的文档 → 建立关联
  用户搜索 "深度学习" → 与 "神经网络" 频繁共现

扩展规则:
  IF query ∋ "机器学习" THEN add "ML", "machine learning"
  IF query ∋ "深度学习"  THEN add "deep learning", "神经网络"
```

### 4.2 伪相关反馈（PRF，Pseudo Relevance Feedback）

**假设：** 检索结果的前 k 篇文档（Top-k）是相关的（"伪相关"）

```
Step 1: 用原始查询检索，获取 Top-k 文档 (D_rel)

Step 2: 从 D_rel 中提取高权重词条作为扩展词
  方法A - Rocchio 算法:
    q_new = α×q_old + β×(Σ d∈D_rel d/|D_rel|) - γ×(Σ d∈D_nonrel d/|D_nonrel|)
    
  方法B - RM3（Relevance Model 3）:
    P(w|q) = (1-λ)×P(w|q_orig) + λ×P(w|θ_rel)
    
    其中 P(w|θ_rel) = Σ_{d∈D_rel} P(d|q) × P(w|d)

Step 3: 将扩展词加入查询，重新检索

示例:
  原始查询: "python 机器学习"
  Top-5文档关键词: sklearn, numpy, pandas, 分类, 回归, 特征工程
  扩展查询: "python 机器学习 sklearn numpy 分类"
```

**PRF 的风险：**
```
查询: "apple"（用户想找苹果公司）
Top-5 文档: 关于苹果水果的文章
提取扩展词: "fruit, tree, juice, orchard"
扩展后查询: "apple fruit tree juice"
→ 完全跑偏！主题漂移（Query Drift）

防止策略:
  1. 限制扩展词数量（通常5-10个）
  2. 控制扩展权重（β < 1）
  3. 只使用高置信度扩展词
```

### 4.3 词嵌入扩展（Word Embedding Expansion）

```python
# 使用 Word2Vec 找最相似词条
import gensim

model = gensim.models.Word2Vec.load("word2vec_model")

def expand_with_embeddings(query_terms, top_n=3, min_similarity=0.7):
    expanded = list(query_terms)  # 原始查询词
    
    for term in query_terms:
        try:
            similar_words = model.wv.most_similar(term, topn=top_n)
            for word, similarity in similar_words:
                if similarity >= min_similarity:
                    expanded.append(word)
        except KeyError:
            pass  # 词不在词汇表中
    
    return list(set(expanded))

# 示例
query = ["car", "accident"]
expanded = expand_with_embeddings(query)
# → ["car", "accident", "vehicle", "crash", "automobile", "collision"]
```

---

## 5. 布尔查询解析

### 5.1 布尔查询语法

```
基础操作:
  AND（与）: "machine learning" AND "python"
  OR（或）:  "machine learning" OR "deep learning"
  NOT（非）: "python" NOT "snake"

短语查询:
  "machine learning"  （带引号，要求词条相邻）

通配符:
  pyth*               （前缀匹配）
  p?thon              （单字符通配）

范围查询:
  date:[2024-01-01 TO 2024-12-31]
  price:[100 TO 500]

字段查询:
  title:python        （只在标题中匹配）
  body:"machine learning"
```

### 5.2 查询解析为 AST（抽象语法树）

```
查询: (machine OR deep) AND learning NOT snake

AST:
           AND
          /   \
        OR    NOT
       /  \     \
  machine deep  snake
              \
           learning

执行顺序（从下到上）:
1. machine 的 posting list: [d1, d2, d3, d5]
2. deep 的 posting list:    [d2, d4, d5, d6]
3. OR(machine, deep):       [d1, d2, d3, d4, d5, d6]
4. learning 的 posting list:[d1, d2, d4, d5]
5. AND(step3, learning):    [d1, d2, d4, d5]
6. snake 的 posting list:   [d4, d7]
7. NOT(step5, snake):       [d1, d2, d5]
```

### 5.3 布尔查询优化

**策略：AND 操作先处理 DF 最小的词条**

```python
def optimized_boolean_and(query_terms: List[str], index: InvertedIndex) -> List[int]:
    """
    优化的 AND 查询
    从最小 posting list 开始，利用提前终止
    """
    # 按 DF 升序排序
    sorted_terms = sorted(
        query_terms,
        key=lambda t: index.get_df(t)
    )
    
    # 从最稀有词开始
    result = set(p.doc_id for p in index.get_postings(sorted_terms[0]))
    
    for term in sorted_terms[1:]:
        term_docs = set(p.doc_id for p in index.get_postings(term))
        result = result & term_docs  # 取交集
        
        if not result:  # 提前终止！
            return []
    
    return sorted(result)
```

---

## 6. 近邻查询（Proximity Queries）

允许词条在一定距离内出现（不要求严格相邻）：

```
NEAR 查询语法 (Elasticsearch):
  "machine learning"~2   # machine 和 learning 之间最多2个词

位置感知评分:
  词条越近，相关性越高

算法：
  给定词条 t₁ 和 t₂，及文档中的位置列表
  t₁ positions: [5, 23, 67]
  t₂ positions: [7, 25, 90]
  
  找最近的词条对:
    |7-5|=2, |25-23|=2, |90-67|=23
    最小距离 = 2
  
  近邻得分: score_prox = 1 / (1 + min_distance)
           = 1 / (1 + 2) = 0.333
```

---

## 7. 查询松弛（Query Relaxation）

当严格查询返回结果太少时，自动放宽约束：

```
原始查询（AND，返回0结果）:
  "python" AND "机器学习" AND "推荐系统" AND "协同过滤"
  → 0 results

松弛策略（逐步放宽）:
  Step 1: 移除最后一个词
    "python" AND "机器学习" AND "推荐系统"
    → 5 results ← 足够了，停止

  Step 2: AND → OR
    "python" OR "机器学习" OR "推荐系统" OR "协同过滤"
    → 过多，需要排序

  Step 3: 部分匹配（至少包含 n/m 个词）
    至少包含 3/4 个查询词 → 适中
```

---

## 8. 近实时查询处理代码

```python
import re
from dataclasses import dataclass
from typing import List, Dict, Tuple, Union, Set
from enum import Enum

class QueryType(Enum):
    TERM = "term"
    PHRASE = "phrase"
    BOOLEAN_AND = "and"
    BOOLEAN_OR = "or"
    BOOLEAN_NOT = "not"
    WILDCARD = "wildcard"
    RANGE = "range"

@dataclass
class QueryNode:
    """查询 AST 节点"""
    type: QueryType
    value: Union[str, None] = None
    children: List["QueryNode"] = None
    field: str = None
    boost: float = 1.0
    
    def __post_init__(self):
        if self.children is None:
            self.children = []

class QueryParser:
    """
    简单查询解析器
    支持：词条、短语、AND/OR/NOT
    """
    
    def parse(self, query_string: str) -> QueryNode:
        """解析查询字符串为 AST"""
        query_string = query_string.strip()
        
        # 检查是否为布尔查询
        if " AND " in query_string.upper():
            parts = re.split(r'\s+AND\s+', query_string, flags=re.IGNORECASE)
            node = QueryNode(QueryType.BOOLEAN_AND)
            node.children = [self.parse(p) for p in parts]
            return node
        
        if " OR " in query_string.upper():
            parts = re.split(r'\s+OR\s+', query_string, flags=re.IGNORECASE)
            node = QueryNode(QueryType.BOOLEAN_OR)
            node.children = [self.parse(p) for p in parts]
            return node
        
        if query_string.upper().startswith("NOT "):
            node = QueryNode(QueryType.BOOLEAN_NOT)
            node.children = [self.parse(query_string[4:])]
            return node
        
        # 检查是否为短语查询（带引号）
        if query_string.startswith('"') and query_string.endswith('"'):
            phrase = query_string[1:-1]
            node = QueryNode(QueryType.PHRASE, value=phrase)
            return node
        
        # 检查是否有字段指定 (field:term)
        if ":" in query_string:
            field, term = query_string.split(":", 1)
            node = self.parse(term)
            node.field = field
            return node
        
        # 普通词条
        # 处理通配符
        if "*" in query_string or "?" in query_string:
            return QueryNode(QueryType.WILDCARD, value=query_string)
        
        return QueryNode(QueryType.TERM, value=query_string)
    
    def to_string(self, node: QueryNode, indent: int = 0) -> str:
        """将 AST 转为可读字符串（调试用）"""
        prefix = "  " * indent
        if node.type in (QueryType.TERM, QueryType.PHRASE, QueryType.WILDCARD):
            field_str = f"{node.field}:" if node.field else ""
            return f"{prefix}{node.type.value}({field_str}{node.value})"
        else:
            result = f"{prefix}{node.type.value}:\n"
            for child in node.children:
                result += self.to_string(child, indent + 1) + "\n"
            return result.rstrip()


class QueryExecutor:
    """
    查询执行引擎
    将 AST 转换为检索结果
    """
    
    def __init__(self, index):  # index: InvertedIndex
        self.index = index
        self.parser = QueryParser()
    
    def execute(self, query_string: str, analyzer=None) -> List[int]:
        """
        执行查询，返回匹配文档 ID 列表
        analyzer: 文本分析器（与索引时相同）
        """
        ast = self.parser.parse(query_string)
        return self._execute_node(ast, analyzer)
    
    def _execute_node(self, node: QueryNode, analyzer) -> List[int]:
        """递归执行 AST 节点"""
        if node.type == QueryType.TERM:
            term = analyzer.analyze(node.value)[0] if analyzer else node.value.lower()
            return [p.doc_id for p in self.index.get_postings(term)]
        
        elif node.type == QueryType.PHRASE:
            terms = analyzer.analyze(node.value) if analyzer else node.value.lower().split()
            return self.index.phrase_search(terms)
        
        elif node.type == QueryType.BOOLEAN_AND:
            results = [self._execute_node(c, analyzer) for c in node.children]
            return self._intersect_all(results)
        
        elif node.type == QueryType.BOOLEAN_OR:
            results = [self._execute_node(c, analyzer) for c in node.children]
            return self._union_all(results)
        
        elif node.type == QueryType.BOOLEAN_NOT:
            all_docs = set(range(self.index.num_docs))
            excluded = set(self._execute_node(node.children[0], analyzer))
            return sorted(all_docs - excluded)
        
        return []
    
    def _intersect_all(self, posting_lists: List[List[int]]) -> List[int]:
        """多个倒排列表的交集"""
        if not posting_lists:
            return []
        # 按长度排序，从最短的开始
        posting_lists.sort(key=len)
        result = set(posting_lists[0])
        for pl in posting_lists[1:]:
            result &= set(pl)
            if not result:
                return []
        return sorted(result)
    
    def _union_all(self, posting_lists: List[List[int]]) -> List[int]:
        """多个倒排列表的并集"""
        result = set()
        for pl in posting_lists:
            result |= set(pl)
        return sorted(result)


# 演示
if __name__ == "__main__":
    parser = QueryParser()
    
    queries = [
        'machine AND learning',
        '"machine learning"',
        'python OR java',
        'python AND NOT snake',
        'title:machine AND body:"learning algorithm"',
    ]
    
    for q in queries:
        ast = parser.parse(q)
        print(f"查询: {q}")
        print(parser.to_string(ast))
        print()
```

---

## 9. 查询性能优化

### 9.1 查询缓存

```python
from functools import lru_cache
import hashlib

class QueryCache:
    """LRU 缓存搜索结果"""
    
    def __init__(self, max_size: int = 10000):
        self.cache: Dict[str, List[int]] = {}
        self.max_size = max_size
        self.access_count: Dict[str, int] = {}
    
    def _hash_query(self, query: str) -> str:
        """查询字符串的哈希键"""
        return hashlib.md5(query.lower().strip().encode()).hexdigest()
    
    def get(self, query: str) -> List[int]:
        key = self._hash_query(query)
        if key in self.cache:
            self.access_count[key] += 1
            return self.cache[key]
        return None
    
    def set(self, query: str, results: List[int]):
        key = self._hash_query(query)
        if len(self.cache) >= self.max_size:
            # LRU: 淘汰最少访问的
            lru_key = min(self.access_count, key=self.access_count.get)
            del self.cache[lru_key]
            del self.access_count[lru_key]
        self.cache[key] = results
        self.access_count[key] = 1
```

### 9.2 常见查询统计（Top-K 热词优化）

```
统计热门查询（工业实践）:
  1. 实时统计: 用 Redis 的 ZADD/ZREVRANGE 维护热词排行
  2. 预计算: 对热门查询提前计算并缓存结果
  3. 差值更新: 文档更新时只失效受影响的缓存条目

典型热门查询比例:
  Top 1% 查询 → 覆盖 50%+ 的流量（Zipf 定律）
  缓存命中率可达 80%+（对于主流搜索引擎）
```

---

*© 传统搜索引擎深度解析系列 — 第 6 篇 / 8*
