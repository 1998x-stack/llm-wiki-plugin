---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["design", "frontend", "ai-generation", "anti-pattern", "LLM能力"]
aliases: ["AI Slop", "AI 糟粕"]
relates_to:
  - target: "[[frontend-design Skill]]"
    type: contradicts
---

# AI Slop

## 概述
AI 生成的前端界面高度同质化现象，表现为千篇一律的字体、配色、布局和缺乏记忆点的"模板感"设计。

## 关键内容

1. **典型表现**：
   - 清一色的 Inter / Roboto / system-ui 字体
   - 千篇一律的紫色渐变白色背景（`bg-gradient-to-br from-purple-500 to-white`）
   - 所有卡片统一 `rounded-2xl shadow-lg`
   - 居中 + 最大宽度容器的可预测布局
   - 毫无记忆点的"模板感"设计

2. **产生原因**：
   - LLM 训练数据中常见模式的过度学习
   - 缺乏明确的设计决策指导
   - 安全选择偏向（保守的默认样式）

3. **[[Anthropic]] 的回应**：
   - 推出 `frontend-design` [[Skills|Skill]]
   - 强制要求在编码前进行设计决策
   - 提供具体可操作的五维设计指导
   - 建立清晰的"禁止清单"

4. **Anti-[[AI生成代码的质量问题|AI-Slop]] 原则**：
   - **独特性**（distinctive）：每次生成的设计都应该不同
   - **有[[意识]]的选择**：Purpose → Tone → Constraints → Differentiation
   - **彻底执行**：选定美学方向后要彻底贯彻
   - **记忆锚点**：找到设计中令人难忘的那个点

## 来源
- [[02_anthropic_frontend_design_skill]] — frontend-design Skill 解析

## 相关
- [[frontend-design Skill]] — contradicts
- [[Design Thinking]] — relates_to
- [[Typography]] — relates_to
