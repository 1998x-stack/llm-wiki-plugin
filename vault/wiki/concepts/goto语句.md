---
type: concept
status: active
confidence: 0.8
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [programming, control-flow, computer-science, 工具与框架]
aliases: ["Goto Statement", "无条件跳转", "跳转语句"]
relates_to:
  - target: "[[Go To Statement Considered Harmful]]"
    type: addressed_by
    confidence: 0.95
  - target: "[[意大利面条式代码]]"
    type: causes
    confidence: 0.9
  - target: "[[结构化编程]]"
    type: opposed_by
    confidence: 0.9
  - target: "[[汇编语言]]"
    type: originates_from
    confidence: 0.8
  - target: "[[控制流]]"
    type: relates_to
    confidence: 0.9
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# goto语句

## 概述
goto语句是一种无条件跳转语句，允许程序控制流转移到指定标签或行号处继续执行。在1960年代是编程语言的基本构造，但在[[Edsger Dijkstra|Dijkstra]]的"[[Go To Statement Considered Harmful]]"论文后受到广泛批评。

## 关键内容
1. **功能**：goto语句允许程序无条件跳转到代码中标记的位置，打破了传统的顺序执行流程。

2. **历史背景**：早期编程语言（[[FORTRAN]]、COBOL、ALGOL、汇编语言）都大量依赖goto语句实现控制流，是当时编程的主要手段。

3. **问题**：过度使用goto语句导致程序控制流混乱，产生"[[意大利面条式代码]]"，严重影响代码的可读性、[[可维护性]]和正确性验证。

4. **现代观点**：大部分现代编程语言限制或禁止使用goto语句，仅在极少数特殊场景（如[[错误处理]]、跳出多层循环）保留有限的跳转功能。

## 来源
- [[原始论文分析]] — raw/books/计算机科学/06-dijkstra-goto-considered-harmful.md
- [[编程语言设计]] — 相关资料

## 相关
- [[Go To Statement Considered Harmful]] — addressed_by
- [[意大利面条式代码]] — causes
- [[结构化编程]] — opposed_by
- [[汇编语言]] — originates_from