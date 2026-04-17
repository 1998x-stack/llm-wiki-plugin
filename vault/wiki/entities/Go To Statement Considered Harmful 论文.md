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
- 技术
- 研究
- 历史
- 计算理论
aliases:
- Go To Statement Considered Harmful
- A Case against the GO TO Statement
- Dijkstra 1968 论文
- EWD 215
relates_to:
- target: "[[Edsger Dijkstra]]"
  type: caused_by
  confidence: 0.99
  note: 作者
- target: "[[结构化编程]]"
  type: caused
  confidence: 0.99
  note: 开创了结构化编程运动
- target: "[[意大利面条式代码]]"
  type: related_to
  confidence: 0.95
  note: 论文批判的编程风格
- target: "[[Bohm-Jacopini 定理]]"
  type: depends_on
  confidence: 0.9
  note: 为论文提供了理论基础
- target: "[[软件危机]]"
  type: related_to
  confidence: 0.85
  note: 论文发表的时代背景
- target: "[[John Backus]]"
  type: compares_to
  confidence: 0.8
  note: Backus 1977年演讲批评冯诺依曼范式，Dijkstra 1968年批评 goto
- target: "[[函数式编程]]"
  type: related_to
  confidence: 0.8
  note: 结构化编程的进一步延伸
- target: "[[LISP]]"
  type: compares_to
  confidence: 0.75
  note: LISP 天然支持结构化控制流，无需 goto
supersedes: null
---

# Go To Statement Considered Harmful 论文

## 概述

[[Edsger Dijkstra]] 于1968年发表的编辑来信《Go To Statement Considered Harmful》，是计算机科学史上影响最深远的短文之一，开创了[[结构化编程]]运动。

## 关键内容

### 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | Go To Statement Considered Harmful（原投稿标题：A Case against the GO TO Statement） |
| **标题更改者** | Niklaus Wirth（后来设计了 Pascal 语言） |
| **作者** | [[Edsger Dijkstra|Edsger Wybe Dijkstra]]（1930–2002） |
| **发表时间** | 1968年3月 |
| **刊物** | Communications of the ACM, Vol. 11, No. 3, pp. 147-148 |
| **发表形式** | Letters to the Editor（编辑来信） |
| **篇幅** | 不到两页 |
| **EWD 编号** | EWD 215 |

### 核心论点

[[Edsger Dijkstra|Dijkstra]] 论证了 `goto` 语句从根本上破坏了程序的逻辑结构可理解性，使程序员无法在静态的程序文本与动态的执行过程之间建立可靠的心智对应。主张程序应当仅使用**顺序**、**选择**和**循环**三种控制结构来组织。

### 坐标系论证

[[Edsger Dijkstra|Dijkstra]] 独创性地用"坐标系"类比来分析不同控制结构的复杂度：
- 纯顺序执行：只需一个数字（文本索引）
- 过程调用：需要一个栈
- 循环：文本索引 + 循环计数器
- goto：没有任何规则的坐标系可以简洁描述

### 历史影响

- 开创了[[结构化编程]]运动
- 直接影响了此后五十年间几乎所有编程语言的设计决策
- "X Considered Harmful" 成为技术界最广泛使用的批评文体
- [[Edsger Dijkstra|Dijkstra]] 于1972年获得[[阿兰·图灵|图灵]]奖

## 来源

- [[raw/books/计算机科学/06-dijkstra-goto-considered-harmful.md]]

## 相关

- [[Edsger Dijkstra]] — 作者
- [[结构化编程]] — 开创的运动
- [[意大利面条式代码]] — 批判的对象
- [[Bohm-Jacopini 定理]] — 理论基础
- [[软件危机]] — 时代背景
