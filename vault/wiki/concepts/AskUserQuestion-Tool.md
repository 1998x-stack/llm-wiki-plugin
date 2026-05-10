---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [AI, 工具, 方法论, AI工程]
aliases:
  - "AskUserQuestion"
  - "AskUserQuestion Tool"
  - "启发式提问工具"
relates_to:
  - target: "[[Claude-Code]]"
    type: implemented_by
    confidence: 0.95
  - target: "[[ExitPlanTool]]"
    type: extends
    confidence: 0.85
    note: "尝试 1 失败后独立设计"
  - target: "[[渐进式披露 -Progressive-Disclosure]]"
    type: uses
    confidence: 0.9
  - target: "[[Agent-Skills]]"
    type: related_to
    confidence: 0.85
  - target: "[[TodoWrite-Tool]]"
    type: compares_to
    confidence: 0.8
  - target: "[[Task-Tool]]"
    type: related_to
    confidence: 0.85
supersedes: null
---

# AskUserQuestion Tool

## 概述

[[Claude Code]] 中的专用工具，用于在计划模式（plan mode）下向用户提出结构化问题。通过模态框 UI 展示问题并提供多个选项，降低用户回答摩擦，提升沟通带宽。是"像智能体一样观察"设计哲学的典型应用。

## 关键内容

### 设计目标

**优化启发式提问（Elicitation）**：
- 提升 [[Claude_Code|Claude]] 向用户提问的效率和质量
- 降低用户回答问题的时间成本
- 增加用户与 [[Claude_Code|Claude]] 之间的沟通带宽

### 演进历程

**尝试 1：修改 [[ExitPlanTool]]**
- 方案：在 [[ExitPlanTool]] 中添加参数，同时输出计划和一组问题
- 失败原因：
  - [[Claude_Code|Claude]] 困惑：同时要求生成计划和问题导致混淆
  - 潜在冲突：用户回答可能与计划内容矛盾
  - 需要多次调用：可能需要调用 [[ExitPlanTool]] 两次
- 结论：此路不通，需要重新设计

**尝试 2：更改输出格式**
- 方案：更新 [[Claude_Code|Claude]] 输出指令，使用修改的 Markdown 格式（如带括号选项的 bullet points）
- 失败原因：
  - 不可靠：[[Claude_Code|Claude]] 通常能生成格式，但不稳定
  - 常见问题：额外添加句子、遗漏选项、放弃结构
- 结论：解析不可靠，需要更强约束

**尝试 3：AskUserQuestion Tool（最终方案）**
- 方案：创建独立工具，[[Claude_Code|Claude]] 可在任意时刻调用（特别是计划模式）
- 工作机制：
  - 工具触发时显示模态框
  - 展示结构化问题和多个选项
  - 阻塞 Agent 循环直到用户回答
- 成功原因：
  - [[Claude_Code|Claude]]"喜欢"调用这个工具
  - 输出效果好，结构化可靠
  - 用户可组合使用（如在 Agent SDK 中调用或在 [[Agent Skills|Skills]] 中引用）

### 核心特性

**结构化输出**：
- 强制 [[Claude_Code|Claude]] 提供多个选项
- 模态框 UI 提升用户体验
- 阻塞机制确保问题得到回答

**可组合性**：
- 可在 [[Agent SDK]] 中调用
- 可在 [[Agent Skills]] 中引用
- 支持自定义触发条件

### 设计哲学启示

**工具与能力的匹配**：
- 工具设计需要契合模型自身能力
- 即使设计精良的工具，如果 [[Claude_Code|Claude]] 不理解如何调用也无效
- 需要"像智能体一样观察"才能设计出好工具

**演进必要性**：
- 随着 [[Claude_Code|Claude]] 能力提升，工具也需要演进
- AskUserQuestion 可能不是最终形态
- 需要持续实验、阅读输出、尝试新方法

### 与相关工具的关系

**vs [[ExitPlanTool]]**：
- [[ExitPlanTool]]：专注于生成执行计划
- AskUserQuestion：专注于收集用户输入
- 分离关注点，避免单一工具承担过多职责

**vs [[TodoWrite-Tool|TodoWrite]]/Task**：
- [[TodoWrite-Tool|TodoWrite]]/Task：跟踪任务进度
- AskUserQuestion：在计划阶段收集需求
- 可能协同使用（先问问题，再生成任务）

## 来源

- [[raw/articles/ai-engineering/claude-blog/Seeing like an agent_ how we design tools in Claude Code.md]] — 详细设计历程和演进原因

## 相关

- [[Claude-Code]] — 所属项目
- [[ExitPlanTool]] — 演进前身（尝试 1）
- [[渐进式披露-Progressive-Disclosure]] — 设计方法论
- [[Agent-Skills]] — 可引用和组合该工具
- [[TodoWrite-Tool]] — 被 Task Tool 取代的旧工具
- [[Task-Tool]] — 任务协调工具，可能与 AskUserQuestion 协同使用
