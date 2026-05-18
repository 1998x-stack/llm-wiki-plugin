---
type: concept
status: active
confidence: 0.8
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [mathematics, computer-science, algorithm-theory, 工具与框架]
aliases: ["Bohm-Jacopini Theorem", "博姆-贾可皮尼定理"]
relates_to:
  - target: "[[Go To Statement Considered Harmful]]"
    type: provides_theoretical_basis_for
    confidence: 0.9
  - target: "[[结构化编程]]"
    type: supports
    confidence: 0.85
  - target: "[[Corrado Boehm]]"
    type: developed_by
    confidence: 0.8
  - target: "[[Giuseppe Jacopini]]"
    type: developed_by
    confidence: 0.8
  - target: "[[图灵完备]]"
    type: relates_to
    confidence: 0.8
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# Bohm-Jacopini定理

## 概述
Bohm-Jacopini定理是1966年由意大利数学家Corrado Boehm和Giuseppe Jacopini提出的理论结果，证明了任何使用[[goto语句]]的程序都可以用仅包含顺序执行、条件选择(if-then-else)和循环(while-do)三种结构的等价程序来替换。

## 关键内容
1. **定理内容**：该定理从数学上证明了goto在表达能力上是冗余的，任何可[[计算]]问题都可以通过顺序、选择和循环三种基本结构来解决。

2. **理论意义**：为[[结构化编程]]提供了坚实的理论基础，证明了无需goto也能实现所有程序逻辑，从而支持了[[Edsger Dijkstra|Dijkstra]]等学者限制或消除goto的主张。

3. **影响**：该定理成为[[结构化编程]]运动的重要理论支撑，影响了此后几十年编程语言的设计和发展方向。

4. **应用**：为编程语言设计者提供了指导，表明可以在不损失表达能力的前提下简化控制结构。

## 来源
- [[计算理论基础]] — 相关资料
- [[原始论文分析]] — raw/books/计算机科学/06-dijkstra-goto-considered-harmful.md（提及理论基础）

## 相关
- [[Go To Statement Considered Harmful]] — provides_theoretical_basis_for
- [[结构化编程]] — supports
- [[Corrado Boehm]] — developed_by
- [[Giuseppe Jacopini]] — developed_by