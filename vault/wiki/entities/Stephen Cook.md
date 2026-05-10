---
type: entity
entity_type: person
status: active
confidence: 0.95
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 历史
- 研究
aliases:
- Stephen Arthur Cook
- Stephen Cook
- 斯蒂芬·库克
relates_to:
- target: "[[Cook NP 完全性论文]]"
  type: caused
  confidence: 0.99
  note: 1971年发表
- target: "[[NP 完全性]]"
  type: caused
  confidence: 0.99
  note: 定义者
- target: "[[Cook-Levin 定理]]"
  type: caused
  confidence: 0.99
  note: 证明者（与 Levin 独立发现）
- target: "[[P vs NP]]"
  type: caused
  confidence: 0.95
  note: 为该问题奠定基础
- target: "[[Leonid Levin]]"
  type: compares_to
  confidence: 0.9
  note: 独立发现相同结果
- target: "[[Richard Karp]]"
  type: extends
  confidence: 0.85
  note: Karp 证明了21个 NP 完全问题
supersedes: null
---

# Stephen Cook

## 概述

美国-加拿大[[计算]]机科学家（1939–2023），1971年发表论文《[[Cook NP 完全性论文|The Complexity of Theorem-Proving Procedures]]》，定义了 [[NP 完全性]]概念并证明了 SAT 是第一个 [[NP 完全性|NP 完全问题]]。1982年因[[计算复杂度理论]]的开创性贡献获得 ACM [[阿兰·图灵|图灵]]奖。

## 关键内容

### Cook 1971年论文

- 在 STOC 会议上发表了仅八页的论文
- 定义了 [[NP 完全性]]概念
- 证明了[[SAT 问题|布尔可满足性问题]]（SAT）是 [[NP 完全性|NP 完全]]的
- 证明了即使 CNF 形式的 SAT（CNF-SAT）也是 [[NP 完全性|NP 完全]]的

### 证明的核心洞察

将非确定性[[图灵机]]的[[计算]]过程编码为布尔公式：
- 用[[计算]]表（computation tableau）描述[[图灵机]]的运行
- 为表格的每个单元格引入布尔变量
- 将初始条件、合法性约束、转移规则和接受条件表达为 CNF 子句
- 证明了 M 接受 x 当且仅当所构造的公式可满足

### 图灵奖（1982）

授奖理由是"在[[计算复杂度理论]]方面的开创性贡献"。

### 后续影响

- 启发了 Karp（1972）证明21个经典组合问题的 [[NP 完全性]]
- 为 [[P vs NP|P vs NP 问题]]（千禧年数学问题，悬赏100万美元）奠定基础
- 改变了[[算法]]研究的方法论：从"盲目寻找高效[[算法]]"到"先证明复杂度再选择策略"

## 来源

- [[raw/books/计算机科学/08-cook-np-completeness.md]]

## 相关

- [[Cook NP 完全性论文]] — 1971年发表
- [[NP 完全性]] — 定义
- [[Cook-Levin 定理]] — 证明
- [[P vs NP]] — 奠定的问题
- [[Leonid Levin]] — 独立发现者
- [[Richard Karp]] — 拓展者
