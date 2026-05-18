---
type: entity
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, react, performance, skills, AI工程]
aliases: ["react-best-practices", "React Best Practices", "React/Next.js Performance Rules"]
relates_to:
  - target: "[[Vercel Agent Skills]]"
    type: part_of
    confidence: 0.9
  - target: "[[React]]"
    type: implements
    confidence: 0.8
  - target: "[[Next.js]]"
    type: implements
    confidence: 0.8
supersedes: null
---

# React Best Practices Skill

## 概述
[[Vercel Agent Skills]] 中最重要的[[Skills|技能]]之一，包含 70+ 条 [[React]]/[[Next.js]] 性能优化规则，基于 [[Vercel]] 工程师 10+ 年生产代码经验。

## 关键内容

1. **八大分类**：涵盖 Async 模式、Bundle 优化、RSC 边界、Client 端性能、数据获取缓存、安全、状态管理和高级特性

2. **核心规则**：
   - `async-parallel`：并行化独立请求以减少延迟
   - `async-cheap-condition-before-await`：先检查廉价条件再进行昂贵的异步调用
   - Bundle 优化：动态导入、按需导入、避免模块副作用
   - RSC 边界：最小化序列化数据、并行数据获取

3. **优先级体系**：按 CRITICAL → HIGH → MEDIUM → LOW 四级优先级排列规则

## 来源
- [[05_vercel_agent_skills_react.md]] — Vercel Agent Skills React 系列深度解析

## 相关
- [[Vercel Agent Skills]] — part_of
- [[React]] — implements
- [[Next.js]] — implements