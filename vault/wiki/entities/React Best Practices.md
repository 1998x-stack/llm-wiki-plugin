---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [React, Performance, Optimization, Vercel]
aliases: ["react-best-practices", "React Performance Best Practices"]
relates_to: []
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相關頁面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# React Best Practices

## 概述
[[Vercel]] 提供的 [[React]] 性能優化規則集，包含 70+ 條工業級最佳實踐。

## 關鍵內容

1. **八大分類**：
   - Async 模式（CRITICAL 級別）：請求並行化、條件優化
   - Bundle 優化（CRITICAL 級別）：動態導入、按需加載
   - RSC 邊界（HIGH 級別）：序列化最小化
   - Client 端性能（HIGH 級別）：回調穩定化、key 管理
   - 數據獲取緩存（HIGH 級別）：LRU 緩存
   - Security、State、Advanced 等其他分類

2. **核心規則**：
   - `async-parallel`：並行化獨立請求
   - `minimize-serialization-at-rsc-boundaries`：最小化 RSC 邊界序列化
   - `cross-request-lru-caching`：跨請求 LRU 緩存

## 來源
- [[raw/articles/ai-tools/claude-skills/05_vercel_agent_skills_react.md]] — 深度解析

## 相關
- [[Vercel Agent Skills]] — 所屬集合
- [[React]] — 技術棧
- [[Next.js]] — 相關框架