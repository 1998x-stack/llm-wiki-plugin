---
type: entity
status: active
confidence: 0.95
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [操作系统, 计算机科学, 系统软件]
aliases: [UNIX 操作系统, Unix, Unix操作系统]
entity_type: project
relates_to:
  - target: "[[Dennis Ritchie]]"
    type: created_by
    confidence: 0.99
  - target: "[[Ken Thompson]]"
    type: created_by
    confidence: 0.99
  - target: "[[贝尔实验室]]"
    type: developed_at
    confidence: 0.9
  - target: "[[C语言]]"
    type: implemented_in
    confidence: 0.95
  - target: "[[The UNIX Time-Sharing System]]"
    type: documented_in
    confidence: 0.9
  - target: "[[Linux]]"
    type: influences
    confidence: 0.99
  - target: "[[BSD]]"
    type: precedes
    confidence: 0.9
  - target: "[[分时系统]]"
    type: exemplifies
    confidence: 0.95
supersedes: null
---

# UNIX

## 概述
UNIX 是由 Dennis Ritchie 和 Ken Thompson 在贝尔实验室开发的经典操作系统，以其简洁性、模块化和"一切皆文件"的设计哲学著称，成为现代操作系统设计的基因模板。

## 关键内容
1. **极简主义设计哲学**：通过找到少量正确的抽象（统一的文件接口、fork/exec 进程模型、管道），用最少的机制实现了最大的功能组合空间，证明了"少即是多"不仅是美学偏好，更是工程策略。

2. **一切皆文件抽象**：将所有 I/O 资源统一为文件，普通磁盘文件、终端设备、打印机、甚至进程间通信通道（管道），都可以通过同一组操作来访问：`open`、`read`、`write`、`close`。

3. **管道和重定向**：发明了管道机制，使得不同程序可以通过管道连接，实现程序间的无缝协作，催生了"做一件事，做好它"的设计哲学。

4. **C语言实现**：1973年用C语言重写整个内核，打破了"操作系统必须用汇编语言编写"的偏见，实现了操作系统的可移植性。

5. **进程模型**：`fork` 和 `exec` 系统调用的分离设计，使得进程创建和程序加载成为独立操作，为I/O重定向和管道的实现提供了基础。

## 来源
- [[09-ritchie-thompson-unix]] — 论文分析
- [[贝尔实验室]] — 开发背景

## 相关
- [[Dennis Ritchie]] — created_by
- [[Ken Thompson]] — created_by
- [[C语言]] — implemented_in
- [[The UNIX Time-Sharing System]] — documented_in
- [[Linux]] — influences
- [[BSD]] — precedes
- [[分时系统]] — exemplifies