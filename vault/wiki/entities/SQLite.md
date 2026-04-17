---
type: entity
title: "SQLite"
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 2
tags: [工具, 数据库, 技术, 工具与框架]
aliases: ["sqlite", "SQLite3"]
relates_to:
  - target: "[[Claude-Mem]]"
    type: related_to
    confidence: 0.95
  - target: "[[Bun-Runtime|Bun Runtime]]"
    type: related_to
    confidence: 0.9
  - target: "FTS5"
    type: related_to
    confidence: 0.95
  - target: "[[关系模型]]"
    type: implements
    confidence: 0.9
  - target: "[[SQL]]"
    type: implements
    confidence: 0.9
  - target: "[[E.F. Codd]]"
    type: extends
    confidence: 0.8
  supersedes: null
---

# SQLite

## 概述
SQLite 是一个轻量级、无服务器、嵌入式的关系型数据库引擎，由 D. Richard Hipp 于2000年创建。它将整个数据库存储为单个磁盘文件，无需独立服务器进程，是世界上部署量最大的数据库引擎（手机、浏览器、桌面应用、嵌入式系统内置）。在 [[Claude-Mem]] 中，SQLite 作为本地记忆存储后端，通过 `bun:sqlite` 接口高效读写观察记录。

## 关键内容
- **核心特点**：零配置、无服务器、单文件存储（.db 文件）、跨平台、ACID 事务
- **WAL 模式**：Write-Ahead Logging，允许读写并发，提升高频写入场景（如 [[Claude-Mem]]）的吞吐量
- **FTS5**：内置[[FTS5|全文搜索]]引擎模块，支持快速文本索引和检索
- **使用场景**：移动应用（iOS/Android 内置）、桌面软件、测试数据库、嵌入式系统、本地 AI 工具
- **局限性**：不适合高并发写密集的多服务器场景；无内置网络访问控制

## 来源
- 综合自内部引用：[[Claude-Mem]]、[[Bun-Runtime]] 等
- [[raw/books/计算机科学/07-codd-relational-model.md]] — 关系模型背景

## 相关
- [[Claude-Mem]]
- [[Bun-Runtime|Bun Runtime]]
- FTS5
- [[ChromaDB]]
- [[关系模型]] — 实现的理论基础
- [[SQL]] — 使用的查询语言
- [[E.F. Codd]] — 关系模型奠基者
