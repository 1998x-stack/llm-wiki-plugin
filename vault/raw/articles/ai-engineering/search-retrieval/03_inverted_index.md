# 倒排索引（Inverted Index）
> Inverted Index — 深度解析系列 第 3 篇

---

## 1. 核心概念与直觉

### 1.1 正排索引 vs 倒排索引

**正排索引（Forward Index）：** 文档 → 词条  
**倒排索引（Inverted Index）：** 词条 → 文档列表

```
文档集合:
  Doc1: "the cat sat on the mat"
  Doc2: "the cat in the hat"
  Doc3: "the rat sat on the mat"

正排索引（Forward Index）:
  Doc1 → {the:2, cat:1, sat:1, on:1, mat:1}
  Doc2 → {the:2, cat:1, in:1, hat:1}
  Doc3 → {the:2, rat:1, sat:1, on:1, mat:1}

  问题: 查询 "cat" → 需要扫描所有文档 → O(N) 全表扫描！

倒排索引（Inverted Index）:
  cat → [Doc1, Doc2]
  hat → [Doc2]
  in  → [Doc2]
  mat → [Doc1, Doc3]
  on  → [Doc1, Doc3]
  rat → [Doc3]
  sat → [Doc1, Doc3]
  the → [Doc1, Doc2, Doc3]

  优势: 查询 "cat" → 直接定位 [Doc1, Doc2] → O(1) 词典查找 + O(k) 遍历
```

### 1.2 为什么叫"倒排"

"正排"是从文档到词条，"倒排"是将这个映射**颠倒过来**，从词条到文档。  
英文 Inverted Index 的 Inverted 指的就是这种方向的反转。

---

## 2. 倒排索引完整数据结构

```
┌─────────────────────────────────────────────────────────────────┐
│                    倒排索引完整结构                               │
│                                                                 │
│  ┌──────────────────┐                                           │
│  │   词典（Lexicon）  │    ← 内存驻留，支持快速查找                  │
│  │  (Term Dictionary)│                                          │
│  │                  │                                           │
│  │  Term  │DF│Offset │                                          │
│  │ ────── │──│────── │                                          │
│  │  cat   │2 │ 0x100 │──────────────────────┐                  │
│  │  dog   │1 │ 0x200 │                      │                  │
│  │  fox   │3 │ 0x300 │                      │                  │
│  │  ...   │..│ ...   │                      │                  │
│  └──────────────────┘                       │                  │
│                                             ▼                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Postings Lists（倒排列表）                    │  │
│  │              存储在磁盘，按需加载到内存                       │  │
│  │                                                          │  │
│  │  cat: → [Doc1(tf=2,pos=[3,7]), Doc2(tf=1,pos=[1])]      │  │
│  │  dog: → [Doc5(tf=3,pos=[2,5,9])]                        │  │
│  │  fox: → [Doc1(tf=1,pos=[4]), Doc3(tf=2,pos=[1,6]),      │  │
│  │          Doc7(tf=1,pos=[2])]                             │  │
│  │  ...                                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────┐                                           │
│  │  文档元数据存储    │                                           │
│  │  (Doc Metadata)  │                                           │
│  │                  │                                           │
│  │  DocID │ Length │ │    ← 文档长度（BM25需要）                  │
│  │  ─────────────── │                                           │
│  │   Doc1 │   150  │ │                                           │
│  │   Doc2 │   320  │ │                                           │
│  │   ...  │   ...  │ │                                           │
│  └──────────────────┘                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Posting 数据结构详解

### 3.1 基础 Posting（最简形式）

只记录文档 ID，不存储词频和位置：

```
┌──────┬──────┬──────┬──────┐
│ Doc1 │ Doc4 │ Doc7 │ Doc9 │
└──────┴──────┴──────┴──────┘
```

**用途：** 布尔检索（有没有这个词）  
**存储：** 每个 DocID 占 4 字节（uint32）

### 3.2 带词频的 Posting（TF-IDF 需要）

```
┌──────────────┬──────────────┬──────────────┐
│  (Doc1, tf=3)│  (Doc4, tf=1)│  (Doc7, tf=5)│
└──────────────┴──────────────┴──────────────┘
```

**存储：** DocID (4B) + TF (2B) = 6 字节/条目

### 3.3 带位置的 Posting（短语检索需要）

```
┌────────────────────────────┬────────────────────────────┐
│  Doc1                      │  Doc4                      │
│  tf=3                      │  tf=1                      │
│  positions=[5, 23, 41]     │  positions=[12]            │
└────────────────────────────┴────────────────────────────┘
```

**存储：** DocID (4B) + TF (2B) + Positions (4B × TF) 字节/条目  
**用途：** 短语查询、近邻查询

### 3.4 短语查询如何使用位置信息

```
查询: "machine learning"（短语查询，要求相邻）

machine 的 postings:
  Doc1: positions=[3, 15, 27]
  Doc2: positions=[5]

learning 的 postings:
  Doc1: positions=[4, 16]      ← 4=3+1, 16=15+1 → 说明Doc1中有连续的"machine learning"
  Doc2: positions=[6]          ← 6=5+1 → Doc2也匹配

算法:
  对于共同包含两个词的文档（Doc1, Doc2）:
    检查 positions(learning) - positions(machine) == 1
    Doc1: [4-3=1 ✓, 16-15=1 ✓] → 匹配
    Doc2: [6-5=1 ✓]             → 匹配
```

---

## 4. 差值编码（Delta Encoding / Gap Encoding）

倒排列表中的 DocID 是**有序的**（升序），利用这个性质进行差值压缩：

```
原始 DocID 列表（升序）:
  [2, 5, 11, 19, 34, 41, 67, 89]

差值编码（Gap Encoding）:
  [2, 3, 6, 8, 15, 7, 26, 22]
   ↑  ↑─┘  ↑──┘  ↑──┘  ↑──┘
   │  差值  差值  差值  差值
   首个值

重建：2, 2+3=5, 5+6=11, 11+8=19, ...
```

**为什么有效：**
- 原始值范围：1 ~ N（N 可达数十亿）→ 需要 4 字节
- 差值范围：通常远小于 N → 可用更少字节表示

---

## 5. 索引构建算法

### 5.1 原地构建（BIIP - Basic In-memory Indexed Information Processing）

适用于**小规模语料**（可完全装入内存）：

```python
def build_inverted_index_basic(documents: dict) -> dict:
    """
    基础倒排索引构建
    documents: {doc_id: [term1, term2, ...]}
    返回: {term: [(doc_id, tf), ...]}
    """
    # Phase 1: 统计词频
    term_doc_freq = {}  # {term: {doc_id: tf}}
    
    for doc_id, terms in documents.items():
        for term in terms:
            if term not in term_doc_freq:
                term_doc_freq[term] = {}
            term_doc_freq[term][doc_id] = \
                term_doc_freq[term].get(doc_id, 0) + 1
    
    # Phase 2: 构建倒排列表（按 doc_id 排序）
    inverted_index = {}
    for term, doc_freq in term_doc_freq.items():
        postings = sorted(doc_freq.items(), key=lambda x: x[0])
        inverted_index[term] = postings
    
    return inverted_index

# 示例
docs = {
    1: ["cat", "sat", "mat"],
    2: ["cat", "hat"],
    3: ["rat", "sat", "mat"],
}
idx = build_inverted_index_basic(docs)
# → {
#     "cat": [(1,1), (2,1)],
#     "sat": [(1,1), (3,1)],
#     "mat": [(1,1), (3,1)],
#     "hat": [(2,1)],
#     "rat": [(3,1)],
#   }
```

### 5.2 SPIMI（Single-Pass In-Memory Indexing）

适用于**大规模语料**，分批处理，避免排序整个词条-文档对：

```
SPIMI 算法流程:

初始化: 空字典 (term → posting list)

for each 词条-文档对 (term, doc_id) in token stream:
    if 内存已满:
        将当前字典排序后写入临时文件块
        清空内存字典
        continue
    
    if term 不在字典中:
        字典[term] = 新建空 posting list
    
    将 doc_id 追加到 字典[term] 末尾
    （无需排序！SPIMI的核心优势）

最终: 归并所有临时文件块 → 完整倒排索引
```

**SPIMI vs BSBI 对比：**

| 特性 | BSBI（基于排序） | SPIMI |
|------|--------------|-------|
| 内存使用 | 需要完整排序缓冲 | 按块写出 |
| 时间复杂度 | O(T log T) | O(T) |
| 实现复杂度 | 简单 | 中等 |
| 适用规模 | 中等 | 大规模 |

### 5.3 MapReduce 构建（超大规模，分布式）

```
Map 阶段:
  输入: (doc_id, document_text)
  
  对每个词条 term in tokenize(document_text):
      emit (term, (doc_id, tf))

Reduce 阶段:
  输入: (term, [(doc_id1, tf1), (doc_id2, tf2), ...])
  
  将所有 posting 按 doc_id 排序
  计算 df = len(postings)
  emit (term, df, sorted_postings)
```

**分布式索引构建架构：**

```
文档分片                Map Worker               Reduce Worker
Doc1-Doc1000  →  Worker1 emits (term, (doc,tf))  →  Reducer-A: 词条a~g
Doc1001-Doc2000 → Worker2 emits (term, (doc,tf))  →  Reducer-B: 词条h~n
Doc2001-Doc3000 → Worker3 emits (term, (doc,tf))  →  Reducer-C: 词条o~z
...

Shuffle 阶段: 按 term 的哈希值路由到对应 Reducer
每个 Reducer 输出一个完整的词典分区
最终合并 → 全局倒排索引
```

---

## 6. 词典（Term Dictionary）实现

词典需要支持**精确查找**和**前缀查找**（通配符/前缀查询）。

### 6.1 哈希表实现（精确查找最快）

```python
class HashTermDictionary:
    def __init__(self):
        self.dict = {}  # term_string → (term_id, df, postings_offset)
    
    def add(self, term: str, term_id: int, df: int, offset: int):
        self.dict[term] = (term_id, df, offset)
    
    def lookup(self, term: str):
        return self.dict.get(term)  # O(1) 查找
    
    # 缺点: 无法支持前缀查找/范围查找
    # 缺点: 无法支持通配符 "cat*"
```

### 6.2 B+ 树实现（支持范围查找）

```
B+ 树词典结构:

内部节点（路由）:
           [mat, sat]
          /    |    \
         /     |     \
  [cat,hat]  [on]  [rat,the]
      |         |       |
      ▼         ▼       ▼
   叶子节点  叶子节点  叶子节点

叶子节点:
  cat → (df=2, offset=0x100)
  hat → (df=1, offset=0x150)
    ↓ (链表指针) →
  mat → (df=2, offset=0x200)
  on  → (df=2, offset=0x250)
    ↓ →
  rat → (df=1, offset=0x300)
  sat → (df=2, offset=0x350)

优势: O(log N) 查找 + 支持范围查询（前缀、范围）
```

### 6.3 Trie（前缀树）实现（最佳前缀支持）

```
Trie 结构（前缀 "ca" 的路径）:

root
 ├── c
 │   ├── a
 │   │   └── t ← "cat" [df=2, offset=0x100]
 │   │   └── r ← "car" [df=3, offset=0x120]
 │   └── o
 │       └── d ← "cod" [df=1, offset=0x130]
 └── d
     └── o
         └── g ← "dog" [df=5, offset=0x140]

前缀查询 "ca*": 
  找到前缀节点 "ca" → 遍历子树 → [cat, car]

通配符查询 "c?t":
  c → 遍历所有子节点 → 选 ?=a → at ← cat ✓
                    → 选 ?=u → ut ← cut ✓
```

### 6.4 有限状态自动机（FST / FSA）

现代搜索引擎（Lucene）使用 FST（Finite State Transducer）：

```
优势：
  空间效率: 比 Trie 节省 2-3 倍空间（共享前缀 + 共享后缀）
  查找速度: O(len(key)) 精确匹配
  遍历: 支持按字典序遍历所有词条

示例（共享前后缀）：
Trie中存储: {cat, cats, car, care, care}
FST中: 
  c → a → t → (output: "cat" posting offset)
                → s → (output: "cats" posting offset)
          → r → (output: "car" posting offset)
                → e → (output: "care" posting offset)

共享 "ca" 前缀 + 共享末尾结构 → 极大压缩
```

---

## 7. 多字段索引（Multi-field Index）

实际文档有多个字段（title, body, anchor, url 等），需要分别或联合索引：

### 7.1 字段索引方案比较

**方案 A：独立索引（Separate Indexes）**
```
title_index:    {term → [(doc_id, tf_title), ...]}
body_index:     {term → [(doc_id, tf_body), ...]}
anchor_index:   {term → [(doc_id, tf_anchor), ...]}

查询时分别查找，用字段权重加权合并:
score = w_title × score_title + w_body × score_body + w_anchor × score_anchor
```

**方案 B：字段感知单一索引**
```
index: {
    term → [(doc_id, fields_info), ...]
}

fields_info = {
    "title": tf_title,
    "body": tf_body,
    "anchor": tf_anchor,
}

优势: 一次索引查找获得所有字段信息
缺点: Posting 结构更复杂
```

---

## 8. 索引的更新策略

### 8.1 全量重建（Full Rebuild）

```
优点: 实现简单，索引最优化
缺点: 重建期间旧索引提供服务，延迟高
适用: 离线批量场景，文档更新频率低
```

### 8.2 增量索引（Incremental Index）

```
主索引（大，磁盘）: 旧文档
辅助索引（小，内存）: 新增/更新文档

查询时:
  1. 查询辅助索引（内存，快）
  2. 查询主索引（磁盘，慢）
  3. 合并结果（处理删除标记）

定期合并: 辅助索引 → 主索引（防止辅助索引过大）
```

**删除处理（Tombstone）：**
```
文档删除不立即从索引中移除（代价高）
而是维护一个删除标记集合（Deletion Bitmap）:
  deleted_docs = BitSet({doc5, doc23, doc89})

返回结果时过滤已删除文档:
  final_results = [d for d in candidates if d not in deleted_docs]

合并时才真正清理删除文档
```

### 8.3 实时索引（Near Real-time, NRT）

Elasticsearch / Lucene 的 NRT 方案：

```
时间线:

t=0s: 新文档写入内存缓冲区（In-memory Buffer）
      此时不可搜索

t=1s: 定期刷新（Refresh，默认1秒）
      内存缓冲区 → 内存 Segment（已持久化但未 fsync）
      新文档变为可搜索！

t=30min: 定期提交（Commit / Flush）
      内存 Segment → 磁盘 Segment（fsync，持久化保证）

后台: Segment 合并（Merge）
      多个小 Segment → 一个大 Segment
      清除已删除文档
```

---

## 9. Posting List 合并算法

多个词条的查询需要对 posting list 进行集合操作：

### 9.1 AND 合并（交集）

```python
def intersect(p1: List[int], p2: List[int]) -> List[int]:
    """
    双指针合并两个有序 posting list 的交集
    时间复杂度: O(|p1| + |p2|)
    """
    result = []
    i, j = 0, 0
    
    while i < len(p1) and j < len(p2):
        if p1[i] == p2[j]:
            result.append(p1[i])
            i += 1
            j += 1
        elif p1[i] < p2[j]:
            i += 1
        else:
            j += 1
    
    return result

# 示例
p_cat = [2, 5, 11, 23, 34]
p_dog = [3, 5, 11, 19, 34, 45]
print(intersect(p_cat, p_dog))  # → [5, 11, 34]
```

### 9.2 OR 合并（并集）

```python
def union(p1: List[int], p2: List[int]) -> List[int]:
    """
    双指针合并两个有序 posting list 的并集
    """
    result = []
    i, j = 0, 0
    
    while i < len(p1) and j < len(p2):
        if p1[i] == p2[j]:
            result.append(p1[i])
            i += 1; j += 1
        elif p1[i] < p2[j]:
            result.append(p1[i]); i += 1
        else:
            result.append(p2[j]); j += 1
    
    result.extend(p1[i:])
    result.extend(p2[j:])
    return result
```

### 9.3 Skip Pointers（跳表加速）

当两个 posting list 大小差异悬殊时，跳表可以大幅加速：

```
普通 AND 合并: O(|p1| + |p2|)

带跳表的 AND 合并: 当 p1[i] >> p2[j] 时，
                   可以跳过 p2 中的大段，直接跳到接近 p1[i] 的位置

跳表结构（每隔 sqrt(len) 个元素设一个跳指针）:
posting list: [2, 5, 11, 23, 34, 56, 78, 90, ...]
跳表指针:      ↑(2)            ↑(34)         ↑(90)
               每 sqrt(n) 个元素一个跳指针

当 p1[i] = 67 时:
  p2 当前 = 11
  查看跳表: 下一个跳点 = 34 < 67 → 跳
  查看跳表: 下一个跳点 = 90 > 67 → 不跳
  线性扫描 34 → 56 → 78... → 找到或超过 67
  
节省了从 11 到 34 的线性扫描
```

---

## 10. 完整索引实现

```python
import struct
import array
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class Posting:
    doc_id: int
    term_freq: int
    positions: List[int] = field(default_factory=list)

class InvertedIndex:
    """
    完整倒排索引实现，支持：
    - 精确词条查找
    - 位置信息
    - 文档频率统计
    - Skip Pointer 加速
    """
    
    def __init__(self):
        # 词典: term → (term_id, df)
        self.term_dict: Dict[str, Tuple[int, int]] = {}
        # 倒排列表: term_id → List[Posting]
        self.postings: Dict[int, List[Posting]] = defaultdict(list)
        # 文档长度: doc_id → num_tokens
        self.doc_lengths: Dict[int, int] = {}
        # 词条ID计数器
        self._next_term_id = 0
        # 总文档数
        self.num_docs = 0
        # 文档总词条数（计算平均长度）
        self._total_tokens = 0
    
    def _get_or_create_term_id(self, term: str) -> int:
        if term not in self.term_dict:
            self.term_dict[term] = (self._next_term_id, 0)
            self._next_term_id += 1
        return self.term_dict[term][0]
    
    def add_document(self, doc_id: int, terms: List[str]):
        """添加一篇文档到索引"""
        self.num_docs += 1
        self.doc_lengths[doc_id] = len(terms)
        self._total_tokens += len(terms)
        
        # 统计词频和位置
        term_info: Dict[str, Tuple[int, List[int]]] = {}
        for pos, term in enumerate(terms):
            if term not in term_info:
                term_info[term] = (0, [])
            tf, positions = term_info[term]
            term_info[term] = (tf + 1, positions + [pos])
        
        # 写入倒排列表
        for term, (tf, positions) in term_info.items():
            term_id = self._get_or_create_term_id(term)
            
            # 更新文档频率
            old_id, old_df = self.term_dict[term]
            self.term_dict[term] = (old_id, old_df + 1)
            
            # 添加 Posting
            posting = Posting(doc_id=doc_id, term_freq=tf, positions=positions)
            self.postings[term_id].append(posting)
    
    @property
    def avg_doc_length(self) -> float:
        """平均文档长度（BM25 需要）"""
        return self._total_tokens / max(self.num_docs, 1)
    
    def get_postings(self, term: str) -> List[Posting]:
        """获取词条的倒排列表"""
        if term not in self.term_dict:
            return []
        term_id, _ = self.term_dict[term]
        return self.postings[term_id]
    
    def get_df(self, term: str) -> int:
        """获取文档频率（Document Frequency）"""
        if term not in self.term_dict:
            return 0
        _, df = self.term_dict[term]
        return df
    
    def boolean_and(self, terms: List[str]) -> List[int]:
        """
        布尔 AND 查询：返回所有词条都出现过的文档
        优化：先按 df 升序排序，从最稀有词条开始
        """
        if not terms:
            return []
        
        # 按文档频率升序排序（DF 最小的先处理）
        sorted_terms = sorted(
            [t for t in terms if t in self.term_dict],
            key=lambda t: self.get_df(t)
        )
        
        if not sorted_terms:
            return []
        
        # 从最稀有词条的 posting list 开始
        result = [p.doc_id for p in self.get_postings(sorted_terms[0])]
        
        for term in sorted_terms[1:]:
            postings_ids = [p.doc_id for p in self.get_postings(term)]
            result = self._intersect(result, postings_ids)
            if not result:  # 提前终止
                return []
        
        return result
    
    def _intersect(self, p1: List[int], p2: List[int]) -> List[int]:
        """双指针交集合并"""
        result = []
        i = j = 0
        while i < len(p1) and j < len(p2):
            if p1[i] == p2[j]:
                result.append(p1[i])
                i += 1; j += 1
            elif p1[i] < p2[j]:
                i += 1
            else:
                j += 1
        return result
    
    def phrase_search(self, terms: List[str]) -> List[int]:
        """
        短语查询：要求词条按顺序且相邻出现
        例如: "machine learning" 要求 machine 后紧跟 learning
        """
        if len(terms) < 2:
            return self.boolean_and(terms)
        
        # 先找候选文档（AND 查询）
        candidate_docs = self.boolean_and(terms)
        
        matching_docs = []
        for doc_id in candidate_docs:
            # 获取每个词条在该文档中的位置列表
            term_positions = []
            valid = True
            for term in terms:
                postings = self.get_postings(term)
                doc_posting = next((p for p in postings if p.doc_id == doc_id), None)
                if doc_posting is None:
                    valid = False
                    break
                term_positions.append(set(doc_posting.positions))
            
            if not valid:
                continue
            
            # 检查是否存在连续位置序列
            # 第一个词的每个位置，检查后续词是否在 +1, +2, ... 位置
            first_positions = term_positions[0]
            for start_pos in first_positions:
                if all(
                    (start_pos + offset) in term_positions[offset]
                    for offset in range(1, len(terms))
                ):
                    matching_docs.append(doc_id)
                    break
        
        return matching_docs
    
    def stats(self) -> dict:
        """索引统计信息"""
        total_postings = sum(len(pl) for pl in self.postings.values())
        return {
            "num_docs": self.num_docs,
            "vocab_size": len(self.term_dict),
            "total_postings": total_postings,
            "avg_doc_length": self.avg_doc_length,
            "avg_postings_per_term": total_postings / max(len(self.term_dict), 1),
        }


# 使用示例
if __name__ == "__main__":
    from text_analyzer import TextAnalyzer, TextAnalyzerConfig
    
    # 构建索引
    index = InvertedIndex()
    
    documents = {
        1: ["machine", "learning", "is", "great"],
        2: ["deep", "learning", "for", "machine", "translation"],
        3: ["machine", "learning", "algorithms"],
        4: ["natural", "language", "processing"],
        5: ["deep", "neural", "networks"],
    }
    
    for doc_id, terms in documents.items():
        index.add_document(doc_id, terms)
    
    # 查询
    print("AND查询 'machine learning':", index.boolean_and(["machine", "learning"]))
    # → [1, 2, 3]
    
    print("短语查询 'machine learning':", index.phrase_search(["machine", "learning"]))
    # → [1, 3]（Doc2中 machine 在位置4，learning在位置2，不相邻）
    
    print("索引统计:", index.stats())
```

---

## 11. 索引压缩总览（详见第 8 篇）

| 压缩技术 | 压缩对象 | 压缩率 | 解压速度 |
|---------|---------|-------|---------|
| VByte（变长字节） | DocID差值 | 中等 | ★★★★★ |
| Gamma Coding | DocID差值 | 高 | ★★★ |
| PForDelta | DocID差值（批量） | 高 | ★★★★ |
| Simple-9 | DocID差值（批量） | 中高 | ★★★★ |
| 词典压缩（Front Coding）| 词典字符串 | 高 | ★★★★ |

---

*© 传统搜索引擎深度解析系列 — 第 3 篇 / 8*
