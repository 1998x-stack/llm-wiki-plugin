---
type: concept
status: active
confidence: 0.95
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
- Unix
- UNIX 操作系统
relates_to:
- target: "[[Dennis Ritchie]]"
  type: caused_by
  confidence: 0.99
  note: 共同创造者
- target: "[[Ken Thompson]]"
  type: caused_by
  confidence: 0.99
  note: 共同创造者
- target: "[[UNIX 论文]]"
  type: caused_by
  confidence: 0.99
  note: 首次向世界正式介绍
- target: "[[C 语言]]"
  type: depends_on
  confidence: 0.95
  note: 1973年用 C 语言重写内核
- target: "[[Multics]]"
  type: supersedes
  confidence: 0.85
  note: 对 Multics 复杂性的反叛
- target: "[[操作系统]]"
  type: implements
  confidence: 0.99
  note: 定义了现代操作系统的基因
- target: "[[Brian Kernighan]]"
  type: related_to
  confidence: 0.75
  note: Bell Labs UNIX 团队成员
- target: "[[Doug McIlroy]]"
  type: related_to
  confidence: 0.8
  note: 管道思想的提出者
supersedes: null
---

# UNIX

## 概述

UNIX 是由 Ken Thompson 和 Dennis Ritchie 在 Bell Labs 开发的分时操作系统，以简洁性、模块化和"一切皆文件"为核心设计哲学，其后代（Linux、macOS、Android）统治了几乎所有计算平台。

## 关键内容

### 诞生

- 1969年：Thompson 在 PDP-7 上写出第一个原型（三个星期）
- 1971年：迁移到 PDP-11/20
- 1973年：用 C 语言重写整个内核——人类历史上第一次用高级语言编写操作系统内核
- 1974年：发表 UNIX 论文

### 核心设计

**一切皆文件**：将所有 I/O 资源（磁盘文件、终端设备、打印机、管道）统一为文件抽象，通过 `open`、`read`、`write`、`close` 操作。

**i-node 结构**：文件元数据与文件名分离，支持硬链接和元数据独立于命名。

**fork/exec 进程模型**：`fork` 创建进程副本，`exec` 加载新程序，`wait` 等待子进程终止。

**Shell 作为普通用户程序**：命令解释器可从内核替换，支持变量、条件、循环。

**管道（Pipeline）**：`command1 | command2 | command3`，程序组合的操作系统级实现。

### 设计哲学

- 做一件事，做好它（Do one thing, and do it well）
- 程序是过滤器——从标准输入读，向标准输出写
- 文本是通用接口
- 尽早失败，沉默是金

### 后代

| 系统 | 与 UNIX 的关系 | 市场地位 |
|------|---------------|---------|
| Linux | 从零重写的 UNIX 兼容系统 | 服务器、超级计算机、Android |
| macOS / iOS | 基于 FreeBSD/Mach 的 Darwin | Apple 全平台 |
| Android | 基于 Linux 内核 | 全球最大移动操作系统 |
| FreeBSD | BSD UNIX 的直系后代 | 服务器、网络设备 |

### 历史影响

- 1983年 Thompson 和 Ritchie 获得图灵奖
- 开源运动的先驱
- 管道思想影响了函数式编程、微服务架构、数据工程等

## 来源

- [[raw/books/计算机科学/09-ritchie-thompson-unix.md]]

## 相关

- [[Dennis Ritchie]] — 共同创造者
- [[Ken Thompson]] — 共同创造者
- [[UNIX 论文]] — 首次正式介绍
- [[C 语言]] — 重写语言
- [[Multics]] — 反叛的对象
- [[操作系统]] — 定义的领域
- [[Brian Kernighan]] — Bell Labs 团队成员
- [[Doug McIlroy]] — 管道思想提出者
