# TF-IDF 深度解析
> Term Frequency–Inverse Document Frequency — 深度解析系列 第 4 篇

---

## 1. 核心思想与直觉

TF-IDF 是信息检索领域最经典的词条权重计算方法，由两个直觉组合而成：

### 直觉一：词频（TF，Term Frequency）

> "一个词在文档中出现越多次，它对该文档的主题越重要。"

```
文档: "机器学习 机器学习 机器学习 深度学习 神经网络"
"机器学习" 出现 3 次 → 比只出现 1 次更重要
```

### 直觉二：逆文档频率（IDF，Inverse Document Frequency）

> "一个词出现在越多文档中，它的区分能力越弱，权重应越低。"

```
"的" 出现在 100% 文档中 → 几乎无区分价值 → 权重极低
"量子纠缠" 出现在 0.01% 文档中 → 极强区分能力 → 权重极高
```

### TF-IDF 的本质

TF-IDF 是这两个直觉的**乘积**，寻找：
- 在**当前文档**中出现频率高（TF高）
- 但在**整个语料库**中出现频率低（IDF高）

的词条，这样的词条最能代表文档的独特主题。

---

## 2. TF 变体（Term Frequency Variants）

### 2.1 原始词频（Raw Count）

```
tf(t, d) = count(t, d)    # 词条 t 在文档 d 中的原始出现次数

示例:
  文档: "cat cat sat cat mat"
  tf("cat", d) = 3
  tf("sat", d) = 1
  tf("mat", d) = 1

问题: 对长文档不公平
  短文档(100词)  "cat" 出现 3次 → tf=3
  长文档(1000词) "cat" 出现 3次 → tf=3（同等对待，但比例差10倍）
```

### 2.2 布尔词频（Boolean）

```
tf(t, d) = 1 if count(t, d) > 0 else 0

# 只关心"有没有"，不关心"多少次"
# 退化为布尔检索，完全忽略词频信息
```

### 2.3 对数归一化词频（Log-Normalized TF）

**最常用的 TF 变体**，解决原始词频的线性增长问题：

```
tf(t, d) = log(1 + count(t, d))

含义: 边际效用递减
  1次 → log(2) ≈ 0.693
  2次 → log(3) ≈ 1.099   (+0.406)
  3次 → log(4) ≈ 1.386   (+0.287)
  10次 → log(11) ≈ 2.398 (+0.405 per additional 7 occurrences)

加1防止 count=0 时 log(0) = -∞
```

**对数归一化的动机：**
```
假设某篇文章中 "cat" 出现 100 次
直觉上它的相关性不应是出现 10 次的 10 倍，
而更接近 2-3 倍（边际效用递减）
```

### 2.4 增强词频（Augmented Normalized TF）

防止偏向长文档，将 TF 归一化到 [0.5, 1.0]：

```
tf(t, d) = 0.5 + 0.5 × (count(t, d) / max_count(d))
           ↑                         ↑
         基础权重              相对于文档内最高频词的比例

其中 max_count(d) = max_{t'} count(t', d)
     （文档中出现次数最多的词的次数）

特性:
  最高频词: tf = 0.5 + 0.5×1 = 1.0
  0次词:    tf = 0.5（不会变成0，给所有词保底权重）
  中等频次: tf ∈ (0.5, 1.0)
```

### 2.5 TF 变体对比表

| 变体 | 公式 | 值域 | 优点 | 缺点 |
|------|------|------|------|------|
| 原始计数 | `count(t,d)` | [0, ∞) | 简单直接 | 长文档偏置 |
| 布尔 | `1 if count>0 else 0` | {0, 1} | 最简单 | 丢失频次信息 |
| 对数 | `log(1+count)` | [0, ∞) | 边际效用递减 | 仍有长文档偏置 |
| 增强 | `0.5 + 0.5×count/max` | [0.5, 1] | 文档内归一化 | 需要两遍扫描 |
| BM25-TF | `(k+1)×count/(k×norm+count)` | (0,k+1) | 有上界，详见第5篇 | 参数需调 |

---

## 3. IDF 变体（Inverse Document Frequency Variants）

### 3.1 原始 IDF（Sparck Jones, 1972）

```
idf(t, D) = log(N / df(t))

其中:
  N     = 语料库文档总数
  df(t) = 包含词条 t 的文档数（Document Frequency）

示例（N = 1,000,000 篇文档）:
  "the":  df=999,000 → idf = log(1M/999K) ≈ 0.001  （极低）
  "cat":  df=10,000  → idf = log(1M/10K)  ≈ 4.605
  "quark":df=100     → idf = log(1M/100)  ≈ 9.210  （极高）
  "xyzzy":df=1       → idf = log(1M/1)    ≈ 13.816 （最高）

问题: 当 df(t) = N 时，idf = log(1) = 0
      即出现在所有文档中的词权重为 0（正常行为，但某些场景不理想）
```

### 3.2 平滑 IDF（带平滑的 IDF）

```
idf_smooth(t, D) = log((N + 1) / (df(t) + 1)) + 1
                           ↑              ↑      ↑
                        分子+1         分母+1   +1保证>0

优点:
  当 df(t) = N 时: idf = log(1) + 1 = 1（不再为0）
  当 df(t) = 0 时: 不会出现除零错误（但实际不会有df=0的词进索引）

这是 scikit-learn TfidfVectorizer 的默认设置（smooth_idf=True）
```

### 3.3 最大 IDF（防止罕见词权重爆炸）

```
idf_max(t, D) = log(max_df(D) / df(t))

其中 max_df(D) = max_{t'} df(t')（最高文档频率）

特性: idf 值域被限制在 [0, log(max_df / min_df)]
```

### 3.4 概率 IDF（Sparck Jones 1977）

```
idf_prob(t, D) = log((N - df(t)) / df(t))

直觉: 相关文档数 vs 不相关文档数的对数比
当 df(t) = N/2 时: idf = log(1) = 0
当 df(t) → 0 时:   idf → log(N/1) = log(N) → 最大
当 df(t) → N 时:   idf → log(0) → -∞（出现问题！）

通常加平滑: idf_prob(t, D) = max(0, log((N - df(t) + 0.5) / (df(t) + 0.5)))
```

### 3.5 IDF 变体完整对比

| 变体 | 公式 | 出处 | 特点 |
|------|------|------|------|
| 标准 IDF | `log(N/df)` | Sparck Jones 1972 | 经典，df=N时为0 |
| 平滑 IDF | `log((N+1)/(df+1))+1` | sklearn默认 | 防零，值>0 |
| 最大 IDF | `log(max_df/df)` | 变体 | 相对归一化 |
| 概率 IDF | `log((N-df)/df)` | Sparck Jones 1977 | BM25中使用 |
| BM25 IDF | `log((N-df+0.5)/(df+0.5)+1)` | Robertson 1994 | 最稳健 |

---

## 4. TF-IDF 完整公式与向量空间模型

### 4.1 基础 TF-IDF 权重

```
tfidf(t, d, D) = tf(t, d) × idf(t, D)

展开:
tfidf(t, d, D) = log(1 + count(t, d)) × log(N / df(t))
```

### 4.2 向量空间模型（VSM）

VSM 将每篇文档表示为词条权重向量：

```
词典（Vocabulary）: V = {t₁, t₂, ..., tₙ}  （n个唯一词条）

文档 d 的 TF-IDF 向量:
d⃗ = [tfidf(t₁,d,D), tfidf(t₂,d,D), ..., tfidf(tₙ,d,D)]

查询 q 的 TF-IDF 向量:
q⃗ = [tfidf(t₁,q,D), tfidf(t₂,q,D), ..., tfidf(tₙ,q,D)]

示例（词典: {cat, dog, fish, bird}）:
文档1: "cat cat dog"     → d₁ = [0.8, 0.4, 0.0, 0.0]
文档2: "fish bird fish"  → d₂ = [0.0, 0.0, 0.9, 0.5]
查询:  "cat fish"        → q  = [0.6, 0.0, 0.7, 0.0]
```

**高维空间可视化（降维到2D）：**
```
bird^
  |      d₂●
  |
  |
  |                  q● (cat, fish)
  |
  |      d₁●
  |
  └─────────────────────→ cat
```

### 4.3 余弦相似度（Cosine Similarity）

**为什么用余弦而不用欧氏距离？**

```
欧氏距离的问题:
  文档A: "cat cat cat cat" → 向量: [4, 0, 0, ...]
  文档B: "cat"             → 向量: [1, 0, 0, ...]
  查询:  "cat"             → 向量: [1, 0, 0, ...]

  欧氏距离: dist(A, q) = 3, dist(B, q) = 0
  → 结果: B 比 A 更相关？（直觉上 A 更相关）

余弦相似度消除文档长度影响:
  cos(A, q) = (4×1) / (4×1) = 1.0    ← 完全相关
  cos(B, q) = (1×1) / (1×1) = 1.0    ← 完全相关
  → 两者同等相关（合理，因为主题相同）
```

**余弦相似度公式：**

```
        q⃗ · d⃗
cos(q, d) = ─────────────────
            ‖q⃗‖ × ‖d⃗‖

        Σᵢ qᵢ × dᵢ
      = ─────────────────────────
        √(Σᵢ qᵢ²) × √(Σᵢ dᵢ²)

实践中对文档向量预先L2归一化:
  d̂ = d⃗ / ‖d⃗‖

则查询时: cos(q, d) = q⃗ · d̂  (只需点积，无需除法)
```

### 4.4 完整计算示例

**语料库设置：**
```
N = 3 篇文档:
  d₁: "the cat sat on the mat"     → 预处理后: [cat, sat, mat]
  d₂: "the cat in the hat"         → 预处理后: [cat, hat]
  d₃: "the rat sat on the mat"     → 预处理后: [rat, sat, mat]

词典: {cat, hat, mat, rat, sat}
```

**Step 1: 统计 df**
```
df(cat) = 2  (出现在 d₁, d₂)
df(hat) = 1  (出现在 d₂)
df(mat) = 2  (出现在 d₁, d₃)
df(rat) = 1  (出现在 d₃)
df(sat) = 2  (出现在 d₁, d₃)
```

**Step 2: 计算 IDF**
```
idf(cat) = log(3/2) ≈ 0.405
idf(hat) = log(3/1) ≈ 1.099
idf(mat) = log(3/2) ≈ 0.405
idf(rat) = log(3/1) ≈ 1.099
idf(sat) = log(3/2) ≈ 0.405
```

**Step 3: 计算各文档的 TF-IDF 向量**

（使用对数 TF = log(1 + count)）

```
词条:        cat    hat    mat    rat    sat

d₁ TF:      1      0      1      0      1
d₁ log-TF: 0.693   0    0.693    0    0.693

d₁ TF-IDF:  0.693×0.405  0  0.693×0.405  0  0.693×0.405
           = [0.281,   0.000, 0.281,   0.000, 0.281]

d₂ TF-IDF: [0.281,   1.099, 0.000,   0.000, 0.000]

d₃ TF-IDF: [0.000,   0.000, 0.281,   1.099, 0.281]
```

**Step 4: 处理查询 "cat mat"**

```
查询词条: [cat, mat]
查询 TF:  cat=1, mat=1
查询 TF-IDF 向量:
  q = [0.281, 0.000, 0.281, 0.000, 0.000]
```

**Step 5: 计算余弦相似度**

```
cos(q, d₁) = (0.281×0.281 + 0.000×0.000 + 0.281×0.281 + ...) / (‖q‖ × ‖d₁‖)
           = (0.0790 + 0.0790) / (0.397 × 0.486)
           = 0.1580 / 0.193
           ≈ 0.819

cos(q, d₂) = (0.281×0.281 + 0 + 0 + 0 + 0) / (0.397 × 1.140)
           = 0.0790 / 0.453
           ≈ 0.174

cos(q, d₃) = (0 + 0 + 0.281×0.281 + 0 + 0) / (0.397 × 1.157)
           = 0.0790 / 0.459
           ≈ 0.172

排名: d₁(0.819) > d₂(0.174) > d₃(0.172)
最相关文档: d₁ "the cat sat on the mat" ✓ 合理！
```

---

## 5. TF-IDF 的变种与扩展

### 5.1 BM25 视角下的 TF-IDF

TF-IDF 可以看作 BM25 的特殊情况（详见第 5 篇）：
```
当 BM25 参数 k₁→∞, b=0 时: BM25 → 原始TF × IDF
当 BM25 参数 k₁=1, b=0.75 时: BM25（标准）
```

### 5.2 字段加权 TF-IDF（Field-Weighted TF-IDF）

```
score(q, d) = Σ_t Σ_f w_f × tfidf_f(t, d)

其中:
  f ∈ {title, body, anchor, url}  字段
  w_f: 字段权重（title > anchor > body > url）

典型权重配置:
  w_title = 3.0
  w_anchor = 2.0
  w_body = 1.0
  w_url = 0.5
```

### 5.3 TF-IDF 权重系统命名约定（SMART）

SMART 表示法（Salton 等提出）使用三字母编码描述 TF-IDF 变体：

```
格式: [TF变体][IDF变体][归一化]

TF变体:
  n = None（原始计数）
  l = log(1 + tf)
  a = 0.5 + 0.5×tf/max_tf（增强）
  b = 布尔 {0, 1}

IDF变体:
  n = None（无IDF）
  t = log(N/df)（标准IDF）
  p = log((N-df)/df)（概率IDF）

归一化:
  n = None
  c = 余弦归一化（L2归一化）
  u = 单位归一化

常见组合:
  lnc (文档): log-TF, 无IDF, 余弦归一化
  ltc (文档): log-TF, 标准IDF, 余弦归一化
  lnc-ltc:    文档用 lnc，查询用 ltc
  atc-lnc:    文档用 lnc，查询用 atc
```

---

## 6. TF-IDF 的问题与局限

### 6.1 词袋模型（Bag of Words）局限

```
文档A: "dog bites man"
文档B: "man bites dog"

TF-IDF(A) = TF-IDF(B)  ← 相同的词条集合，忽略词序！
```

### 6.2 语义盲区（Semantic Blindness）

```
查询: "car"
文档: "I drive an automobile to work every day"

TF-IDF 得分: 0（"car" 未出现）
但文档语义高度相关！

解决方案:
  1. 同义词词典扩展（WordNet）
  2. LSA（潜在语义分析）
  3. Word2Vec / GloVe 词嵌入
  4. Dense Retrieval (DPR, ColBERT)
```

### 6.3 文档长度偏置

```
长文档天然包含更多词，TF 值更高
→ 即使内容匹配质量相同，长文档得分更高

解决方案:
  1. TF-IDF + 余弦归一化（L2归一化）
  2. BM25 的 b 参数（显式长度归一化，见第5篇）
```

### 6.4 频率-相关性非线性

```
词出现 10 次的文档相关性 ≠ 10 × 出现 1 次的文档相关性
边际效用递减：前几次出现最重要

解决方案: BM25 的饱和函数
  BM25-TF = (k₁+1)×tf / (k₁×(1-b+b×dl/avgdl) + tf)
  当 tf → ∞ 时: BM25-TF → k₁+1（有上界！）
```

---

## 7. Python 完整实现

```python
import math
import numpy as np
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Optional

class TFIDF:
    """
    完整 TF-IDF 实现
    支持多种 TF/IDF 变体和向量空间模型查询
    """
    
    def __init__(
        self,
        tf_method: str = "log",       # raw, log, augmented, boolean
        idf_method: str = "standard", # standard, smooth, prob, max
        norm: Optional[str] = "l2",   # None, "l1", "l2"
        sublinear_tf: bool = False,   # 是否使用 log(1+log(tf)) 的次线性 TF
    ):
        self.tf_method = tf_method
        self.idf_method = idf_method
        self.norm = norm
        self.sublinear_tf = sublinear_tf
        
        self.vocabulary: Dict[str, int] = {}  # term → index
        self.idf_values: np.ndarray = None
        self.doc_vectors: np.ndarray = None   # (n_docs, n_terms)
        self.n_docs = 0
    
    def _compute_tf(self, term_counts: Dict[str, int]) -> Dict[str, float]:
        """计算 TF 值（支持多种变体）"""
        total = sum(term_counts.values())
        max_count = max(term_counts.values()) if term_counts else 1
        
        tf_values = {}
        for term, count in term_counts.items():
            if self.tf_method == "raw":
                tf = count
            elif self.tf_method == "log":
                tf = math.log(1 + count)
            elif self.tf_method == "augmented":
                tf = 0.5 + 0.5 * (count / max_count)
            elif self.tf_method == "boolean":
                tf = 1.0 if count > 0 else 0.0
            else:
                raise ValueError(f"Unknown TF method: {self.tf_method}")
            
            if self.sublinear_tf and tf > 0:
                tf = math.log(1 + tf)
            
            tf_values[term] = tf
        
        return tf_values
    
    def _compute_idf(self, df_counts: Dict[str, int], n_docs: int) -> Dict[str, float]:
        """计算 IDF 值（支持多种变体）"""
        idf_values = {}
        max_df = max(df_counts.values()) if df_counts else 1
        
        for term, df in df_counts.items():
            if self.idf_method == "standard":
                idf = math.log(n_docs / df)
            elif self.idf_method == "smooth":
                idf = math.log((n_docs + 1) / (df + 1)) + 1
            elif self.idf_method == "prob":
                idf = max(0, math.log((n_docs - df + 0.5) / (df + 0.5)))
            elif self.idf_method == "max":
                idf = math.log(max_df / df)
            elif self.idf_method == "none":
                idf = 1.0
            else:
                raise ValueError(f"Unknown IDF method: {self.idf_method}")
            
            idf_values[term] = idf
        
        return idf_values
    
    def fit(self, documents: List[List[str]]) -> "TFIDF":
        """
        从文档集合构建词典和 IDF 值
        documents: 已分词的文档列表
        """
        self.n_docs = len(documents)
        
        # 构建词典
        all_terms = set()
        for doc in documents:
            all_terms.update(doc)
        self.vocabulary = {term: idx for idx, term in enumerate(sorted(all_terms))}
        vocab_size = len(self.vocabulary)
        
        # 统计 DF
        df_counts = defaultdict(int)
        for doc in documents:
            for term in set(doc):  # set去重，每篇文档只算一次
                if term in self.vocabulary:
                    df_counts[term] += 1
        
        # 计算 IDF
        idf_dict = self._compute_idf(dict(df_counts), self.n_docs)
        self.idf_values = np.zeros(vocab_size)
        for term, idf in idf_dict.items():
            self.idf_values[self.vocabulary[term]] = idf
        
        return self
    
    def transform(self, documents: List[List[str]]) -> np.ndarray:
        """
        将文档列表转换为 TF-IDF 矩阵
        返回: (n_docs, n_terms) 的矩阵
        """
        vocab_size = len(self.vocabulary)
        result = np.zeros((len(documents), vocab_size))
        
        for doc_idx, doc in enumerate(documents):
            term_counts = Counter(doc)
            tf_values = self._compute_tf(dict(term_counts))
            
            for term, tf in tf_values.items():
                if term in self.vocabulary:
                    term_idx = self.vocabulary[term]
                    result[doc_idx, term_idx] = tf * self.idf_values[term_idx]
        
        # 向量归一化
        if self.norm == "l2":
            norms = np.linalg.norm(result, axis=1, keepdims=True)
            norms[norms == 0] = 1  # 防止除零
            result = result / norms
        elif self.norm == "l1":
            norms = np.sum(np.abs(result), axis=1, keepdims=True)
            norms[norms == 0] = 1
            result = result / norms
        
        return result
    
    def fit_transform(self, documents: List[List[str]]) -> np.ndarray:
        """fit 和 transform 的组合"""
        self.fit(documents)
        matrix = self.transform(documents)
        self.doc_vectors = matrix
        return matrix
    
    def transform_query(self, query: List[str]) -> np.ndarray:
        """将查询词条转换为 TF-IDF 向量"""
        return self.transform([query])[0]
    
    def cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """计算两个向量的余弦相似度"""
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return np.dot(v1, v2) / (norm1 * norm2)
    
    def search(
        self, 
        query: List[str], 
        top_k: int = 10
    ) -> List[Tuple[int, float]]:
        """
        TF-IDF 向量空间检索
        返回: [(doc_idx, score), ...] 按分数降序排列
        """
        if self.doc_vectors is None:
            raise RuntimeError("请先调用 fit_transform()")
        
        query_vec = self.transform_query(query)
        
        # 计算查询与所有文档的余弦相似度
        # 如果文档向量已L2归一化，则只需点积
        if self.norm == "l2":
            scores = self.doc_vectors @ query_vec
        else:
            scores = np.array([
                self.cosine_similarity(query_vec, doc_vec)
                for doc_vec in self.doc_vectors
            ])
        
        # 按分数降序排列
        ranked_indices = np.argsort(scores)[::-1]
        
        return [
            (int(idx), float(scores[idx]))
            for idx in ranked_indices[:top_k]
            if scores[idx] > 0
        ]
    
    def top_terms(self, doc_vector: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        """获取文档的最高权重词条"""
        reverse_vocab = {v: k for k, v in self.vocabulary.items()}
        top_indices = np.argsort(doc_vector)[::-1][:top_k]
        return [(reverse_vocab[i], doc_vector[i]) for i in top_indices if doc_vector[i] > 0]


# ─── 演示 ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # 已分词的文档集
    documents = [
        ["machine", "learning", "algorithms", "python"],
        ["deep", "learning", "neural", "networks", "machine"],
        ["python", "programming", "software", "development"],
        ["natural", "language", "processing", "machine", "learning"],
        ["neural", "networks", "deep", "reinforcement", "learning"],
    ]
    
    # 初始化 TF-IDF（对数TF + 平滑IDF + L2归一化）
    tfidf = TFIDF(tf_method="log", idf_method="smooth", norm="l2")
    doc_matrix = tfidf.fit_transform(documents)
    
    print(f"词典大小: {len(tfidf.vocabulary)}")
    print(f"文档矩阵维度: {doc_matrix.shape}")
    
    # 搜索
    query = ["machine", "learning"]
    results = tfidf.search(query, top_k=3)
    
    print(f"\n查询: {query}")
    print("排名结果:")
    for rank, (doc_id, score) in enumerate(results, 1):
        print(f"  [{rank}] Doc{doc_id}: {documents[doc_id]} | 相关度={score:.4f}")
    
    # 查看文档0的关键词
    print(f"\nDoc0 关键词:")
    for term, weight in tfidf.top_terms(doc_matrix[0]):
        print(f"  {term}: {weight:.4f}")
```

---

## 8. IDF 的统计特性

### 8.1 Zipf 定律与 IDF

Zipf 定律描述自然语言中词频的分布：

```
词频 × 词频排名 ≈ 常数

最高频词: "the" (英语, 约7%的词token)
第2名词频 ≈ 1/2 × "the" 的词频
第k名词频 ≈ 1/k × "the" 的词频

Zipf + IDF 的含义:
  高频词（低排名）→ 高 DF → 低 IDF → 低权重
  低频词（高排名）→ 低 DF → 高 IDF → 高权重
  
  IDF 自然补偿了 Zipf 分布的偏斜！
```

### 8.2 词频 vs IDF 的动态平衡

```
信息量最大的词条（最佳检索词）:
  不应过于常见（IDF 太低）
  不应过于罕见（TF 太低）
  
  "甜蜜点": 中等 DF + 较高 TF
```

---

*© 传统搜索引擎深度解析系列 — 第 4 篇 / 8*
