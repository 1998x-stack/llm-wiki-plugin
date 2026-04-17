---
type: entity
entity_type: paper
status: active
confidence: 0.98
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 计算理论
- 数学
- 历史
- 基础理论
aliases:
- On Computable Numbers, with an Application to the Entscheidungsproblem
- Turing 1936
- 论可计算数及其在判定问题上的应用
relates_to:
- target: "[[阿兰·图灵]]"
  type: caused_by
  confidence: 0.99
  note: 作者，24岁时完成
- target: "[[图灵机]]"
  type: caused
  confidence: 0.99
  note: 论文中首次定义
- target: "[[停机问题]]"
  type: caused
  confidence: 0.99
  note: 论文中首次证明不可判定性
- target: "[[可计算数]]"
  type: caused
  confidence: 0.99
  note: 论文中首次定义
- target: "[[判定问题 (Entscheidungsproblem)]]"
  type: caused
  confidence: 0.95
  note: 论文给出否定回答
- target: "[[Church-Turing 论题]]"
  type: caused
  confidence: 0.9
  note: 论文附录证明了与 λ 演算的等价性
- target: "[[阿隆佐·邱奇]]"
  type: compares_to
  confidence: 0.85
  note: Church 同年用 λ 演算独立解决同一问题
- target: "[[库尔特·哥德尔]]"
  type: related_to
  confidence: 0.8
  note: Godel 不完备定理（1931）为该论文铺平道路
- target: "[[大卫·希尔伯特]]"
  type: related_to
  confidence: 0.85
  note: 论文回答了 Hilbert 1928年提出的判定问题
- target: "[[约翰·冯·诺依曼]]"
  type: related_to
  confidence: 0.75
  note: 通用图灵机概念影响了 von Neumann 存储程序架构
supersedes: null
---

# On Computable Numbers 论文

## 概述

[[阿兰·图灵]]于1936年发表的划时代论文，首次精确定义了"计算"的数学概念（[[图灵机]]），证明了[[停机问题]]不可判定，否定回答了[[判定问题 (Entscheidungsproblem)]]，并构造了[[图灵机|通用图灵机]]预言了可编程计算机。被公认为计算机科学的"创世文档"。

## 关键内容

### 论文信息

| 字段 | 内容 |
|------|------|
| **标题** | On Computable Numbers, with an Application to the Entscheidungsproblem |
| **作者** | Alan Mathison Turing (1912–1954) |
| **提交时间** | 1936年5月28日 |
| **正式出版** | 1937年，附勘误与附录 |
| **发表期刊** | Proceedings of the London Mathematical Society, Series 2, Volume 42, pp. 230–265 |
| **作者当时身份** | 剑桥大学国王学院研究员，年仅24岁 |

### 四大核心贡献

1. **[[图灵机]]定义**：通过对人类计算员行为的忠实抽象（有限符号、有限状态、每步一格），给出了有史以来第一个数学上完全精确的"计算"定义。Godel 本人评价为"哲学上不可能设置得更令人满意"。

2. **[[图灵机|通用图灵机]]**：证明存在一台能模拟任意[[图灵机]]的机器——在概念层面预言了可编程计算机的出现，比 ENIAC（1946年）早10年，比 von Neumann 存储程序架构（1945年）早9年。

3. **[[停机问题]]不可判定**：通过反证法和对角化论证，证明不存在算法能判定任意程序是否停机。这是第一个被严格证明不可判定的具体问题，开创了不可判定性理论的整个领域。

4. **[[判定问题 (Entscheidungsproblem)]]的否定回答**：由停机问题的不可判定性推导出 Hilbert 判定问题不可解，与 Godel 不完备定理一起彻底终结了 Hilbert 形式化纲领。

### 附录：与 Church λ 演算的等价性

Turing 在附录中证明了图灵可计算性与 λ 可定义性的完全等价，这一结果连同与 Godel 递归函数、Post 产生式系统、Markov 算法等的等价性，共同构成了[[Church-Turing 论题]]的经验基础。

### 历史意义

很少有学术论文能够同时：
- 解决了一个著名的悬而未决的数学问题（判定问题）
- 创立了一个全新的学科（计算理论）
- 发明了一个至今仍在使用的核心概念（[[图灵机]]）
- 预言了一种尚未出现的技术（可编程计算机）

Turing 的这篇论文做到了以上所有。在人类思想史上，很难找到第二篇单独的论文具有如此多维度的深远影响。

## 来源

- [[raw/books/计算机科学/01-turing-on-computable-numbers.md]]

## 相关

- [[阿兰·图灵]] — 作者
- [[图灵机]] — 论文中定义的核心概念
- [[停机问题]] — 论文中证明不可判定
- [[可计算数]] — 论文中定义的概念
- [[判定问题 (Entscheidungsproblem)]] — 论文回答的问题
- [[图灵机|通用图灵机]] — 论文中最具预见性的构造
- [[Church-Turing 论题]] — 论文附录提供了关键支撑
