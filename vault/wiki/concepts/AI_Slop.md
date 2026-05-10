---
type: concept
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-issue, design-problem, frontend]
aliases: ["AI Slop", "AI Slops"]
relates_to: []
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# AI Slop

## 概述
[[AI Slop]] 指 AI 生成的前端界面高度同质化的问题，表现为所有界面都具有相同的视觉特征和设计模式。

## 关键内容
1. **具体表现**：
   - 清一色的 Inter / Roboto / system-ui 字体
   - 千篇一律的紫色渐变白色背景（`bg-gradient-to-br from-purple-500 to-white`）
   - 所有卡片统一 `rounded-2xl shadow-lg`
   - 居中 + 最大宽度容器的可预测布局
   - 毫无记忆点的"模板感"设计

2. **问题影响**：
   - 生成的前端界面缺乏独特性
   - 用户体验趋于雷同
   - 品牌识别度低

3. **解决方案**：
   - [[Anthropic]] 开发了 [[frontend-design Skill]] 来系统性解决此问题
   - 通过设计思考框架避免同质化生成

## 来源
- [[Anthropic 官方 frontend-design Skill 深度解析]] — 问题定义与解决方案

## 相关
- [[Anthropic]] — 问题定义与解决者
- [[Claude Code]] — 应用场景
- [[frontend-design Skill]] — 解决方案