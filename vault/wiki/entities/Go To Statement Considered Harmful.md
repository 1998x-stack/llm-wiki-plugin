---
type: entity
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [programming, software-engineering, computer-science, paper, 机器人学]
aliases: ["Go To Statement Considered Harmful", "GOTO有害论", "goto harmful"]
relates_to:
  - target: "[[Edsger W. Dijkstra]]"
    type: authored
    confidence: 0.9
  - target: "[[结构化编程]]"
    type: influenced
    confidence: 0.9
  - target: "[[Bohm-Jacopini定理]]"
    type: built_upon
    confidence: 0.8
  - target: "[[意大利面条式代码]]"
    type: addressed_problem
    confidence: 0.9
  - target: "[[Communications of the ACM]]"
    type: published_in
    confidence: 0.9
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# Go To Statement Considered Harmful

## 概述
[[Edsger Dijkstra|Dijkstra]]在1968年发表的著名论文，论证了[[goto语句]]从根本上破坏了程序的逻辑结构可理解性，主张仅使用顺序、选择和循环三种控制结构来组织程序，为[[结构化编程]]运动奠定思想基石。

## 关键内容
1. **核心论点**：论文论证了[[goto语句]]从根本上破坏了程序的逻辑结构可理解性，使程序员无法在静态的程序文本与动态的执行过程之间建立可靠的心智对应。[[Edsger Dijkstra|Dijkstra]]提出程序应当仅使用顺序（sequence）、选择（selection）和循环（iteration）三种控制结构来组织。

2. **背景问题**：1968年正值[[软件危机]]时期，当时主流编程语言都大量依赖[[goto语句]]，产生了"[[意大利面条式代码]]"。[[Edsger Dijkstra|Dijkstra]]认为[[goto语句]]是程序正确性论证的最大障碍。

3. **理论基础**：论文建立在[[Bohm-Jacopini定理]]之上，该定理证明任何使用[[goto语句]]的程序都可以用仅包含顺序、条件选择和循环三种结构的等价程序替换。因此goto在表达能力上是冗余的。

4. **历史影响**：这篇不到两页的编辑来信引发了[[结构化编程]]革命，直接影响了此后五十年间几乎所有编程语言的设计决策，包括Pascal、Java、[[Python]]等现代语言都限制或禁止了goto的使用。

## 来源
- [[原始论文分析]] — raw/books/计算机科学/06-dijkstra-goto-considered-harmful.md
- [[Communications of the ACM]] — 1968年3月刊

## 相关
- [[Edsger W. Dijkstra]] — authored
- [[结构化编程]] — influenced
- [[意大利面条式代码]] — addressed_problem