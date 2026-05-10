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
- The UNIX Time-Sharing System
- UNIX 论文
- Ritchie Thompson 1974 论文
relates_to:
- target: "[[Dennis Ritchie]]"
  type: caused_by
  confidence: 0.99
  note: 第一作者
- target: "[[Ken Thompson]]"
  type: caused_by
  confidence: 0.99
  note: 第二作者
- target: "[[UNIX]]"
  type: caused
  confidence: 0.99
  note: 首次向世界正式介绍 UNIX
- target: "[[C 语言]]"
  type: related_to
  confidence: 0.9
  note: 论文描述了用 C 语言重写 UNIX 内核
- target: "[[Multics]]"
  type: compares_to
  confidence: 0.85
  note: UNIX 是对 Multics 复杂性的反叛
- target: "[[操作系统]]"
  type: caused
  confidence: 0.95
  note: 定义了现代操作系统的基因
- target: "[[计算复杂度理论]]"
  type: compares_to
  confidence: 0.6
  note: 两者都是 1970 年代初期计算机科学的奠基性工作
supersedes: null
---

# UNIX 论文

## 概述

[[Dennis Ritchie]] 和 [[Ken Thompson]] 于1974年发表的《The UNIX Time-Sharing System》，是[[操作系统]]史上被引最多的文献之一（11,000+次），首次向世界正式介绍了 [[UNIX|UNIX 操作系统]]的设计哲学和实现细节。

## 关键内容

### 论文信息

| 条目 | 内容 |
|------|------|
| **标题** | The UNIX Time-Sharing System |
| **作者** | Dennis M. Ritchie, [[Ken Thompson]] |
| **发表时间** | 1974年7月（正式版）；1973年10月在第四届 ACM SOSP 会议上宣读前一版本 |
| **刊物** | Communications of the ACM, Vol. 17, No. 7, pp. 365-375 |
| **篇幅** | 11页 |

### 核心设计

- **一切皆文件**：将所有 I/O 资源统一为文件抽象
- **i-node 结构**：文件元数据与文件名分离
- **fork/exec 进程模型**：创建进程和加载程序分离
- **Shell 作为普通用户程序**：命令解释器可从内核替换
- **管道（Pipeline）**：程序组合的[[操作系统]]级实现

### 历史背景

- 从 [[Multics]] 项目的废墟中汲取灵感
- Thompson 在 PDP-7 上利用三个星期写出第一个原型
- 1973年用 [[C 语言]]重写整个内核——人类历史上第一次用高级语言编写[[操作系统]]内核

### 影响

- 定义了现代[[操作系统]]的基因
- 其后代（Linux、macOS、Android）统治了几乎所有[[计算]]平台
- 开源运动的先驱
- 1983年 Thompson 和 Ritchie 因此获得[[阿兰·图灵|图灵]]奖

## 来源

- [[raw/books/计算机科学/09-ritchie-thompson-unix.md]]

## 相关

- [[Dennis Ritchie]] — 第一作者
- [[Ken Thompson]] — 第二作者
- [[UNIX]] — 论文描述的操作系统
- [[C 语言]] — 重写 UNIX 的语言
- [[Multics]] — UNIX 反叛的对象
- [[操作系统]] — 定义的领域
