---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, react-native, mobile, performance, skills, AI工程]
aliases: ["react-native-skills", "React Native Skills", "Expo Mobile UI Skills"]
relates_to:
  - target: "[[Vercel Agent Skills]]"
    type: part_of
    confidence: 0.8
  - target: "[[React Native]]"
    type: implements
    confidence: 0.8
  - target: "[[Expo]]"
    type: implements
    confidence: 0.7
supersedes: null
---

# React Native Skills

## 概述
[[Vercel Agent Skills]] 中的移动端[[Skills|技能]]，专注于 [[React]] Native + Expo 的性能与规范，提供移动端 UI 性能优化指导。

## 关键内容

1. **核心重点**：FlashList 替代 FlatList 的使用，这是 CRITICAL 级别的优化规则

2. **列表性能 8 条规则**：
   - FlashList 替代 FlatList（大幅优化内存和帧率）
   - 列表 item 组件用 `React.memo` 包裹
   - 稳定化回调引用（`useCallback`）
   - 避免 inline style object
   - 将函数提取到组件外部
   - 优化列表中的图片（使用 `expo-image`）
   - 将昂贵[[计算]]移到组件外部
   - 使用 `itemType` 处理异构列表

3. **移动端性能关注点**：60fps 流畅体验的关键路径优化

## 来源
- [[05_vercel_agent_skills_react.md]] — Vercel Agent Skills React 系列深度解析

## 相关
- [[Vercel Agent Skills]] — part_of
- [[React Native]] — implements
- [[Expo]] — implements