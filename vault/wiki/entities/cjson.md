---
type: entity
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["JSON", "Lua库", "编解码", "高性能"]
aliases: [cjson库, lua-cjson, JSON编解码]
relates_to: [UrhoX引擎, Lua数据驱动设计]
supersedes: null
---

# cjson

## 概述
cjson 是一个高性能的 Lua JSON 编解码库，基于 C 实现，比纯 Lua 实现快数倍。[[UrhoX引擎|UrhoX]] 推荐使用 cjson 进行 JSON 操作。

## 关键内容
1. **在 UrhoX 中的推荐**：JSON 编解码推荐使用 cjson，相关文档见 `engine-docs/recipes/json.md`。
2. **性能优势**：cjson 是 C 扩展库，编解码速度远快于纯 Lua 实现，适合游戏配置加载、存档读写等场景。
3. **使用方式**：`local cjson = require "cjson"`，然后使用 `cjson.encode()` 和 `cjson.decode()` 进行编解码。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，快速查找章节

## 相关
- [[UrhoX引擎]] — relates_to（宿主引擎）
- [[Lua数据驱动设计]] — relates_to（JSON 是数据驱动的重要载体）
