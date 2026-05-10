---
type: entity
status: active
confidence: 0.95
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, 信息过滤, 协同过滤, Xerox PARC]
aliases: ["Tapestry", "Using Collaborative Filtering to Weave an Information Tapestry"]
relates_to:
  - target: "[[协同过滤]]"
    type: implements
  - target: "[[Xerox PARC]]"
    type: part_of
  - target: "[[GroupLens]]"
    type: extends
  - target: "[[TQL]]"
    type: uses
  - target: "[[标注存储]]"
    type: uses
  - target: "[[标注]]"
    type: uses
  - target: "[[David Goldberg]]"
    type: developed_by
  - target: "[[David Nichols]]"
    type: developed_by
  - target: "[[Brian M. Oki]]"
    type: developed_by
  - target: "[[Douglas Terry]]"
    type: developed_by
  - target: "[[编译信息]]"
    type: explained_by
supersedes: null
---ce: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [推荐系统, 信息过滤, [[协同过滤]]]
aliases: ["Tapestry", "[[Tapestry 论文|Using Collaborative Filtering to Weave an Information Tapestry]]"]
relates_to:
  - target: "[[协同过滤]]"
    type: caused
  - target: "[[Xerox PARC]]"
    type: part_of
  - target: "[[GroupLens]]"
    type: extends
  - target: "TQL"
    type: uses
supersedes: null
---

# Tapestry 系统

## 概述
Tapestry 是 [[Xerox PARC]] 于 1992 年开发的信息过滤系统，首次提出"[[协同过滤]]"（[[协同过滤|Collaborative Filtering]]）术语和概念，通过让用户协作分享对文档的主观评价来帮助彼此从海量信息中筛选有价值内容。

## 关键内容

1. **论文信息**：[[David Goldberg|Goldberg]], D., [[David Nichols|Nichols]], D., Oki, B.M., & [[Douglas Terry|Terry]], D. (1992). "Using [[协同过滤|Collaborative Filtering]] to Weave an Information Tapestry." *Communications of the ACM*, 35(12), 61-70。DOI: 10.1145/138859.138867。引用量约 2,841 次（ACM DL）。

2. **系统架构**：由多个协作组件构成：
   - **Indexer（索引器）**：提取文档可索引字段（发件人、主题、日期、关键词）
   - **Document Store（文档存储）**：只追加数据库，文档不可修改/删除
   - **Annotation Store（[[标注存储]]）**：保存用户对文档的反应和评价，与文档分离存储且公开
   - **Filterer（过滤器）**：反复运行用户定义的 TQL 查询，投递匹配文档到用户邮箱
   - **Little Box（用户邮箱）**：每个用户的专属队列
   - **Appraiser（评估器）**：对过滤结果分类和优先级排序
   - **Reader/Browser（阅读器/浏览器）**：提供"Like It!"和"Hate It!"按钮

3. **TQL（[[TQL|Tapestry Query Language]]）**：量身定制的查询语言，在 SQL 基础上改进，支持可扩展字段、集合值字段、[[标注]]引用。用户可在同一查询中混合基于内容的条件和基于[[标注]]的条件。

4. **手动[[协同过滤]]的特征**：
   - 用户需要知道并选择信任特定的人
   - 用户自行编写 TQL 查询规则
   - 适用于小型熟人社区（如 PARC 内部几百人）
   - 无任何"自动发现相似用户"机制

5. **局限性**：
   - 绝大多数文档未被[[标注]]（[[标注]]稀疏性）
   - 激励不对称：[[标注]]成本由[[标注]]者承担，收益由他人享受
   - 依赖商业数据库授权，无法自由分发
   - [[冷启动问题]]：新用户不知道该引用谁的[[标注]]
   - 只追加存储导致存储需求持续增长

6. **历史地位**：推荐系统发展史的起点。1992 Tapestry → 1994 [[GroupLens]]（自动化 CF）→ 1995 [[Ringo]]/[[Firefly Networks|Firefly]]（音乐推荐）→ 1997 "推荐系统"术语确立 → 1998 [[Amazon]]（Item-based CF）→ 2006 [[Netflix Prize]] → 2010s 深度学习时代 → 2020s LLM 时代。

## 来源
- [[raw/books/推荐系统/01-tapestry-collaborative-filtering.md]] — 全文解读
- [[raw/books/推荐系统/02-grouplens-collaborative-filtering.md]] — GroupLens 对 Tapestry 的继承与超越

## 相关
- [[协同过滤]] — Tapestry 首次提出并定义的核心概念
- [[Xerox PARC]] — Tapestry 的开发机构
- [[GroupLens]] — 受 Tapestry 启发，实现自动化协同过滤
- [[TQL]] — Tapestry 的查询语言
- [[基于内容的过滤]] — Tapestry 将内容过滤与协同过滤有机结合
- [[标注存储]] — Tapestry 系统的重要组成部分
- [[标注]] — Tapestry 协同过滤的核心机制
