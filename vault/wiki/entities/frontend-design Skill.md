---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, claude-skills, frontend, design, react, 工具与框架]
aliases: [frontend-design, frontend-design skill]
entity_type: tool
relates_to:
  - target: "[[Agent Skills]]"
    type: implements
  - target: "[[web-artifacts-builder Skill]]"
    type: complements
supersedes: null
---

# frontend-design Skill

## 概述
frontend-design 是一个专注于前端设计哲学的 [[Claude_Code|Claude]] [[Skills|Skill]]，与专注于工程实现的 [[web-artifacts-builder Skill]] 形成互补关系，负责提供美学指导和设计决策。

## 关键内容

1. **定位与用途**：
   - 专注于设计哲学，而 [[web-artifacts-builder Skill|web-artifacts-builder]] 专注工程实现
   - 适用于单文件 [[React]] JSX 或 HTML artifacts
   - 避免 AI 生成的常见视觉缺陷（AI slop）

2. **反 [[AI Slop]] 原则**：
   - 避免过度居中的布局
   - 避免紫色渐变
   - 避免统一的圆角
   - 避免使用 Inter 字体

3. **适用场景**：
   - 单文件 [[React]] JSX Artifact（无需构建）
   - 单文件 HTML Artifact
   - 作为 [[web-artifacts-builder Skill]] 的设计指导层

## 来源
- [[web-artifacts-builder Skill 深度解析]] — 深度调查文档

## 相关
- [[web-artifacts-builder Skill]] — 互补的工程实现技能
- [[Agent Skills]] — Claude 的各种技能工具
- [[Claude Connectors]] — Claude 连接外部工具的方式