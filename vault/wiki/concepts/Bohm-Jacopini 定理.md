---
type: concept
status: active
confidence: 0.9
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 研究
- 数学
- 计算理论
aliases:
- Bohm-Jacopini Theorem
- 伯姆-雅科皮尼定理
relates_to:
- target: "[[结构化编程]]"
  type: caused
  confidence: 0.95
  note: 为结构化编程提供了理论基础
- target: "[[Go To Statement Considered Harmful 论文]]"
  type: related_to
  confidence: 0.9
  note: 为 Dijkstra 的论证提供了坚实的理论基础
- target: "[[Edsger Dijkstra]]"
  type: related_to
  confidence: 0.85
  note: Dijkstra 的论证依赖此定理
- target: "[[图灵机]]"
  type: related_to
  confidence: 0.7
  note: 定理证明了三种结构在表达能力上是图灵完备的
supersedes: null
---

# Bohm-Jacopini 定理

## 概述

Bohm-Jacopini 定理（1966年）由意大利数学家 Corrado Bohm 和 Giuseppe Jacopini 发表，证明了任何使用 goto 语句的程序都可以用仅包含顺序执行、条件选择和循环三种结构的等价程序来替换。

## 关键内容

### 定理陈述

> 任何包含 goto 语句的程序，都可以被转换为一个仅使用**顺序执行**（sequence）、**条件选择**（if-then-else）和**循环**（while-do）三种控制结构的等价程序。

### 意义

这一定理从数学上证明了 goto 在表达能力上是**冗余的**——你不需要它就能写出任何程序。这为 [[Edsger Dijkstra|Dijkstra]] 1968年《[[Go To Statement Considered Harmful 论文|Go To Statement Considered Harmful]]》的论证提供了坚实的理论基础：既然 goto 不是必需的，而且它还带来了严重的可理解性问题，那么我们就有充分的理由将它从编程实践中移除。

### 与图灵完备的关系

三种基本控制结构（加上过程调用这种组织手段）在表达能力上是**[[阿兰·图灵|图灵]]完备**的——任何可[[计算]]的问题都可以用它们来解决。

### 实践影响

虽然定理在数学上证明了 goto 的可替代性，但转换后的程序有时需要引入额外的布尔标志变量，可能导致代码更加复杂。Donald Knuth 在1974年的论文中对此进行了全面分析，承认在少数场景下 goto 仍然是更好的选择。

## 来源

- [[raw/books/计算机科学/06-dijkstra-goto-considered-harmful.md]]

## 相关

- [[结构化编程]] — 定理为其提供理论基础
- [[Go To Statement Considered Harmful 论文]] — 依赖此定理
- [[Edsger Dijkstra]] — 论证依赖此定理
- [[图灵机]] — 三种结构是图灵完备的
