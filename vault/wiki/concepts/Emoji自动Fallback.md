---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [Emoji, 字体回退, NanoVG, UrhoX, 文本渲染, 游戏开发]
aliases: [Emoji回退, 表情符号支持, font fallback]
relates_to: [NanoVG字体创建规范, NanoVG]
supersedes: null
---

# Emoji自动Fallback

## 概述
[[UrhoX引擎|UrhoX]] 内置 Emoji 自动回退机制，文本渲染时无需指定额外的 Emoji 字体即可正常显示表情符号。

## 关键内容
1. **自动回退**：引擎在找不到字符时自动尝试 Emoji 字体，开发者无需手动[[Configuration|配置]]或创建额外的 Emoji 字体。
2. **使用方式**：创建普通字体后（`nvgCreateFont`），直接在文本中使用 Emoji 字符即可，如 `nvgText(vg, 100, 100, "Hello 😀")`。
3. **限制**：回退机制依赖引擎内置的 Emoji 字体资源，如果引擎未打包对应字体，回退可能失败。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，规则 #7.5

## 相关
- [[NanoVG字体创建规范]] — relates_to（字体创建后可直接使用 Emoji）
- [[NanoVG]] — relates_to（渲染库）
