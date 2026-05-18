---
type: tool
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [缓存数据库, 内存数据库, NoSQL, AI工程]
aliases: ["Redis", "Remote Dictionary Server"]
relates_to:
  - target: "[[API模块规范]]"
    type: used_by
  - target: "[[缓存策略]]"
    type: implements
  - target: "[[NoSQL数据库]]"
    type: part_of
supersedes: null
---

# Redis

## 概述
Redis是一个开源的内存数据结构存储系统，可用作数据库、缓存和消息代理。它支持多种数据结构，如字符串、哈希、列表、集合等。

## 关键内容

1. **核心技术特点**：
   - 内存存储：数据主要存储在内存中，提供高速读写性能
   - 多种数据结构：支持字符串、哈希、列表、集合、有序集合等多种数据结构
   - 持久化选项：支持RDB和AOF两种持久化方式
   - 主从复制：支持数据的高可用性和扩展性

2. **应用场景**：
   - 会话缓存：如API规范中提到的用作会话缓存
   - 数据库缓存层：加速对后端数据库的访问
   - 消息队列：使用列表和发布订阅功能
   - 排行榜/计数器：利用有序集合实现实时排行榜

3. **缓存策略**：
   - 支持多种过期策略，如TTL(Time To Live)
   - 支持LRU(Least Recently Used)等淘汰[[算法]]
   - 提供原子操作确保缓存一致性

4. **性能优势**：
   - 单线程模型减少上下文切换开销
   - 非阻塞I/O多路复用技术
   - 丰富的内置数据结构减少序列化开销

## 来源
- [[directory-api-CLAUDE]] — 在API模块规范中提到使用Redis做会话缓存

## 相关
- [[API模块规范]] — used_by
- [[缓存策略]] — implements
- [[NoSQL数据库]] — part_of