# 传统搜索引擎总体架构
> Traditional Search Engine Architecture — 深度解析系列 第 1 篇

---

## 1. 搜索引擎的本质定义

搜索引擎（Search Engine）是一个**信息检索系统（Information Retrieval System, IRS）**，其核心任务是：

> 给定用户的**查询（Query）**，从海量文档集合（Corpus）中，**快速、准确地找出最相关的文档**，并按相关性降序返回排名列表（Ranked List）。

这个定义包含三个核心维度：
- **快速（Efficiency）**：毫秒级响应，支撑亿级文档
- **准确（Effectiveness）**：返回结果与用户意图高度匹配
- **可扩展（Scalability）**：随文档量线性扩展

---

## 2. 全局数据流

```
原始文档（Web Pages / Documents）
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    离线索引管道（Offline Indexing Pipeline）         │
│                                                                 │
│  文档采集   →  文档解析   →  文本预处理   →  索引构建   →  索引存储  │
│ (Crawling)   (Parsing)   (Preprocessing)  (Indexing)  (Storage) │
└─────────────────────────────────────────────────────────────────┘
        │
        ▼  （构建完成的倒排索引）
┌─────────────────────────────────────────────────────────────────┐
│                    在线检索管道（Online Retrieval Pipeline）         │
│                                                                 │
│  用户查询   →  查询解析   →  查询执行   →  结果排序   →  结果展示  │
│  (Query)    (Parsing)   (Execution)    (Ranking)   (Display)   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. 核心组件全景图

```
┌─────────────────────────────────────────────────────────────────────┐
│                      传统搜索引擎核心组件                              │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                   离线组件（Offline Components）               │    │
│  │                                                             │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │    │
│  │  │ 网络爬虫  │  │ 文档解析  │  │ 文本分析  │  │ 索引构建  │   │    │
│  │  │ Crawler  │  │  Parser  │  │ Analyzer │  │ Indexer  │   │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │    │
│  │       │              │              │              │        │    │
│  │       ▼              ▼              ▼              ▼        │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │    │
│  │  │文档存储库 │  │ 元数据库  │  │ 词典库   │  │ 倒排索引  │   │    │
│  │  │Doc Store │  │Metadata  │  │ Lexicon  │  │Inv.Index │   │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                   在线组件（Online Components）               │    │
│  │                                                             │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │    │
│  │  │ 查询接收  │  │ 查询解析  │  │ 索引查找  │  │ 评分排序  │   │    │
│  │  │  Input   │  │  Parser  │  │  Lookup  │  │  Scorer  │   │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │    │
│  │                                                             │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │    │
│  │  │ 缓存系统  │  │ 结果聚合  │  │ 结果展示  │                 │    │
│  │  │  Cache   │  │Aggregator│  │  Render  │                 │    │
│  │  └──────────┘  └──────────┘  └──────────┘                 │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. 各组件职责详解

### 4.1 文档采集层（Crawling Layer）

| 子组件 | 职责 | 关键技术 |
|--------|------|---------|
| URL 调度器 | 管理待爬 URL 优先队列 | Priority Queue, PageRank 预估 |
| HTTP 下载器 | 并发下载网页内容 | 多线程/协程, HTTP/2 |
| 礼貌策略 | 遵守 robots.txt, 控制爬取速率 | Rate Limiting, Crawl-delay |
| 去重过滤器 | 发现并过滤重复页面 | SimHash, MD5 fingerprint |
| 链接提取器 | 从页面提取新链接 | HTML parser, XPath |

**爬虫工作流（Breadth-First 策略）：**
```
初始化种子 URL → 放入队列 → 取出URL → 下载页面 → 解析内容
      ↑                                              │
      └──────────── 提取新链接 ←────────────────────┘
                         │
                    去重过滤 → 合法新URL → 放入队列
```

---

### 4.2 文档解析层（Parsing Layer）

**输入：** 原始 HTML/PDF/Word/等各种格式文档  
**输出：** 结构化文本 + 元数据

```
原始HTML文档
    │
    ├─→ 字符编码检测 (UTF-8 / GBK / ...)
    ├─→ HTML结构解析 (DOM Tree)
    ├─→ 内容区域提取 (去除导航栏/广告/页脚)
    ├─→ 纯文本提取 (去除HTML标签)
    ├─→ 元数据提取:
    │       title, description, keywords
    │       author, date, language
    │       anchor texts, headings (H1-H6)
    └─→ 链接提取 (a href)
```

**字段权重概念（后续排序使用）：**
- `title` 字段权重 > `heading` > `body` > `meta`

---

### 4.3 文本分析层（Text Analysis Layer）

这是搜索质量的**核心前处理阶段**，详见第 2 篇。

```
原始文本
    │
    ├─→ 语言检测
    ├─→ 分词 (Tokenization)
    ├─→ 大小写归一化 (Normalization)
    ├─→ 停用词过滤 (Stop Words Removal)
    ├─→ 词干提取/词形还原 (Stemming/Lemmatization)
    └─→ 同义词扩展 (Synonym Expansion) [可选]
```

---

### 4.4 索引构建层（Indexing Layer）

**核心产物：倒排索引（Inverted Index）**，详见第 3 篇。

```
预处理后的词条流
    │
    ├─→ 词典构建 (Term Dictionary)
    │       term → term_id (hash/trie)
    │
    ├─→ 词条频率统计 (Term Frequency)
    │       (doc_id, term_id, tf, positions)
    │
    ├─→ Posting List 构建
    │       term_id → [doc1, doc2, doc3, ...]
    │
    ├─→ 索引压缩 (Index Compression)
    │       差值编码 + 变长整数编码
    │
    └─→ 索引合并 (Index Merging)
            SPIMI / MapReduce 大规模构建
```

---

### 4.5 查询处理层（Query Processing Layer）

```
用户输入: "机器学习 推荐系统"
    │
    ├─→ 查询解析
    │       词条化: ["机器学习", "推荐系统"]
    │       意图识别: 信息型 / 导航型 / 事务型
    │
    ├─→ 查询重写
    │       拼写纠错: "macine learning" → "machine learning"
    │       同义词扩展: "机器学习" ≈ "ML" ≈ "machine learning"
    │       查询扩展: PRF (Pseudo Relevance Feedback)
    │
    ├─→ 索引查找
    │       term → posting list
    │       多词条交集/并集操作
    │
    └─→ 评分排序 (TF-IDF / BM25)
```

---

### 4.6 评分排序层（Scoring & Ranking Layer）

这是搜索引擎的**灵魂**，详见第 4、5、7 篇。

**经典相关性评分模型演进：**

```
布尔模型 (Boolean Model)
    │  简单 AND/OR/NOT，无评分
    ▼
向量空间模型 (Vector Space Model, VSM)
    │  TF-IDF 权重，余弦相似度
    ▼
概率模型 (Probabilistic Model)
    │  BM25，Robertson-Spärck Jones 权重
    ▼
语言模型 (Language Model)
    │  查询生成概率，Dirichlet 平滑
    ▼
学习排序 (Learning to Rank, LTR)
    │  RankSVM, LambdaMART
    ▼
神经排序 (Neural Ranking)
       BERT, DPR, ColBERT
```

---

## 5. 检索评估指标体系

### 5.1 效果指标（Effectiveness Metrics）

| 指标 | 公式 | 含义 |
|------|------|------|
| Precision@K | \|Relevant ∩ Retrieved_K\| / K | 前K结果中相关比例 |
| Recall@K | \|Relevant ∩ Retrieved_K\| / \|Relevant\| | 相关文档被召回比例 |
| F1 | 2·P·R / (P+R) | 精确率与召回率调和均值 |
| MAP | Mean Average Precision | 多查询平均精度 |
| MRR | Mean Reciprocal Rank | 第一个相关结果排名倒数均值 |
| NDCG@K | Σ(rel_i / log₂(i+1)) / IDCG | 归一化折扣累积增益 |

### 5.2 效率指标（Efficiency Metrics）

| 指标 | 典型值（工业级） | 含义 |
|------|----------------|------|
| 查询延迟 P50 | < 50ms | 中位响应时间 |
| 查询延迟 P99 | < 200ms | 长尾响应时间 |
| QPS | 10,000+ | 每秒查询量 |
| 索引更新延迟 | < 1s (近实时) | 新文档可检索延迟 |
| 索引大小比 | 原文档的 20-40% | 索引存储效率 |

---

## 6. 工业级搜索引擎对比

| 系统 | 类型 | 核心排序 | 适用场景 |
|------|------|---------|---------|
| **Lucene/Elasticsearch** | 开源全文检索 | BM25 (默认) | 企业搜索、日志 |
| **Solr** | 开源全文检索 | TF-IDF/BM25 | 电商搜索 |
| **Tantivy** | Rust 高性能 | BM25 | 嵌入式搜索 |
| **Whoosh** | Python 纯净 | TF-IDF | 小规模原型 |
| **Google Web Search** | 商业 | PageRank+ML | Web 全局搜索 |
| **Bing** | 商业 | LTR+Neural | Web 全局搜索 |

---

## 7. 系列文章导航

| 篇次 | 主题 | 核心内容 |
|------|------|---------|
| **第 1 篇** | 总体架构 | 数据流、组件职责、评估体系 |
| **第 2 篇** | 文本预处理 | 分词、归一化、停用词、词干提取 |
| **第 3 篇** | 倒排索引 | 结构、构建算法、压缩、DAAT |
| **第 4 篇** | TF-IDF | TF变体、IDF变体、VSM、余弦相似度 |
| **第 5 篇** | BM25 | Okapi BM25、BM25+、BM25F、参数调优 |
| **第 6 篇** | 查询处理 | 拼写纠错、查询扩展、布尔操作 |
| **第 7 篇** | 排序与评分 | DAAT/TAAT、WAND、早期终止 |
| **第 8 篇** | 索引压缩 | VByte、PForDelta、Elias-Gamma |

---

*© 传统搜索引擎深度解析系列 — 第 1 篇 / 8*
