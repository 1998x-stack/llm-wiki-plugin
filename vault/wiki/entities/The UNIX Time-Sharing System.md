---
type: entity
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [操作系统, 计算机科学, 论文]
aliases: [The UNIX Time-Sharing System, UNIX分时系统论文]
entity_type: paper
relates_to:
  - target: "[[Dennis Ritchie]]"
    type: authored_by
    confidence: 0.99
  - target: "[[Ken Thompson]]"
    type: authored_by
    confidence: 0.99
  - target: "[[UNIX]]"
    type: documents
    confidence: 0.99
  - target: "[[贝尔实验室]]"
    type: published_from
    confidence: 0.9
  - target: "[[ACM通讯]]"
    type: published_in
    confidence: 0.9
  - target: "[[操作系统理论]]"
    type: contributes_to
    confidence: 0.95
  - target: "[[现代操作系统]]"
    type: defines_principles_for
    confidence: 0.99
supersedes: null
---

# The UNIX Time-Sharing System

## 概述
《The UNIX Time-Sharing System》是由Dennis Ritchie和Ken Thompson于1974年发表在《ACM通讯》上的经典论文，向全世界正式介绍了UNIX操作系统的设计理念和实现，是计算机科学史上被引最多的论文之一。

## 关键内容
1. **历史意义**：论文详细描述了一个以简洁性、模块化和"一切皆文件"为核心设计哲学的分时操作系统，这个系统后来成为现代操作系统设计的基因模板。

2. **核心技术概念**：论文涵盖了UNIX的文件系统、进程模型、Shell、I/O系统等核心组件，展示了极简主义设计哲学在操作系统领域的成功应用。

3. **设计哲学体现**：论文虽只有11页，但清晰地传达了"做一件事，做好它"的设计理念，成为后来操作系统课程的必读文献。

4. **深远影响**：截至2020年代，这篇论文在Google Scholar上的引用超过11,000次，对整个计算机科学领域产生了深远影响。

## 来源
- [[09-ritchie-thompson-unix]] — 论文分析
- [[ACM通讯]] — 发表刊物

## 相关
- [[Dennis Ritchie]] — authored_by
- [[Ken Thompson]] — authored_by
- [[UNIX]] — documents
- [[操作系统理论]] — contributes_to
- [[现代操作系统]] — defines_principles_for