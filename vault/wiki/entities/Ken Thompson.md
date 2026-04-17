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
- Kenneth Lane Thompson
- 肯·汤普森
relates_to:
- target: "[[Dennis Ritchie]]"
  type: related_to
  confidence: 0.99
  note: UNIX 的共同创造者
- target: "[[UNIX 论文]]"
  type: caused
  confidence: 0.99
  note: 1974年共同发表
- target: "[[UNIX]]"
  type: caused
  confidence: 0.99
  note: 共同创造者
- target: "[[Multics]]"
  type: related_to
  confidence: 0.8
  note: 曾参与 Multics 项目，后退出
- target: "[[C 语言]]"
  type: extends
  confidence: 0.8
  note: 最初使用 B 语言，后与 Ritchie 一起发展出 C 语言
- target: "[[操作系统]]"
  type: caused
  confidence: 0.9
  note: 定义了现代操作系统的基因
supersedes: null
---

# Ken Thompson

## 概述

美国计算机科学家（1943–），UNIX 操作系统的共同创造者，最初在 PDP-7 上写出了 UNIX 的第一个原型。1983年与 Dennis Ritchie 共同获得 ACM 图灵奖。

## 关键内容

### UNIX 的诞生

- 1969年，在 Bell Labs 实验室角落里一台被冷落的 PDP-7 小型机上，利用妻子带孩子回娘家的三个星期，写出了 UNIX 的第一个原型
- 包括文件系统、进程子系统、命令解释器和若干实用工具
- 最初的名字是 UNICS（Uniplexed Information and Computing Service），是对 Multics 的戏谑

### Space Travel 游戏

- Thompson 最初是想在 PDP-7 上玩一个他写的"太空旅行"（Space Travel）游戏
- 这促使他和 Ritchie 意识到需要一个高效的编程环境
- UNIX 是程序员为程序员设计的系统，这一基因决定了它后来的一切特征

### fork 的偶然优雅

- `fork` 最初并不是精心设计的产物，而是 PDP-7 上的一个实现捷径——在那台机器上，复制一个进程的内存恰好很容易做到
- 这个"偶然"的设计后来证明了其深刻的优雅性

### 图灵奖演讲（1984）

- 题为"Reflections on Trusting Trust"
- 展示了如何在编译器中植入不可检测的后门
- 后来成为计算机安全领域的经典文献

### 后续贡献

- 参与开发了 Go 编程语言
- 是正则表达式和 QED 编辑器的早期开发者
- 与 Ritchie、McIlroy、Ossanna、Kernighan 等人组成了 Bell Labs 最具影响力的 UNIX 团队

## 来源

- [[raw/books/计算机科学/09-ritchie-thompson-unix.md]]

## 相关

- [[Dennis Ritchie]] — 共同创造者
- [[UNIX 论文]] — 1974年共同发表
- [[UNIX]] — 共同创造
- [[Multics]] — 曾参与的项目
- [[C 语言]] — 从 B 语言发展而来
- [[操作系统]] — 定义的领域
