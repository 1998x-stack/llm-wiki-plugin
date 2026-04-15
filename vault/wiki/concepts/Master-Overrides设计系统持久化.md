---
type: concept
title: "Master + Overrides 设计系统持久化"
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [UI, 设计系统, AI, 持久化, 上下文工程]
aliases:
  - Master Overrides 模式
  - 设计系统持久化
  - design system persistence
  - Master + Overrides
relates_to:
  - target: "[[UI-UX-Pro-Max]]"
    type: part_of
    confidence: 0.95
  - target: "[[LLM-Statelessness]]"
    type: related_to
    confidence: 0.9
  - target: "[[Context-Engineering]]"
    type: related_to
    confidence: 0.85
  - target: "[[AI设计推理层]]"
    type: related_to
    confidence: 0.8
supersedes: null
---

# Master + Overrides 设计系统持久化

## 概述

Master + Overrides 是一种解决 AI 无状态（Stateless）导致"设计失忆症"的文件架构模式：将设计决策写入项目文件系统，AI 通过读文件获得"记忆"。全局规范存 MASTER.md，页面专属差异存 pages/<page>.md，仅记录与 MASTER 不同之处。

## 关键内容

### 核心问题

每次新对话，AI 对项目的设计规范一无所知——颜色、字体、间距、风格全部重置。传统解法是在提示词里重复粘贴规范，但低效且随项目增长不可维护。

**根本解法**：把"有状态的设计决策"写入文件系统，让无状态的 AI 通过读文件获得持久"记忆"。

### 文件结构

```
design-system/
├── MASTER.md              # 全局设计规范（项目唯一真相来源）
└── pages/
    ├── dashboard.md       # 仪表板专属覆盖
    ├── checkout.md        # 结账页面专属覆盖
    └── landing.md         # 落地页专属覆盖
```

### 层级检索规则

```
1. 构建某页面时，先检查 design-system/pages/<page>.md
2. 若页面文件存在：其规则覆盖 MASTER.md 的对应部分
3. 若页面文件不存在：完全使用 MASTER.md
4. 页面文件只记录「与 MASTER 不同的地方」，不重复
```

### MASTER.md 标准包含

完整设计系统的 8 个维度：Identity（产品类型/目标用户）、Color System（亮/暗模式完整色板）、Typography System（字体 + 类型比例尺）、Spacing System（4px 基准网格）、Component Specifications（按钮/卡片/表单规格）、UI Style（主风格 + 动画 + 图标集）、Anti-Patterns（明确禁止事项）、Tech Stack Specifics（框架/工具链）。

### 页面覆盖示例（只记录差异）

```markdown
# Page Override: Checkout
> Overrides MASTER.md for /checkout route

## Color Overrides
- Error color: #DC2626 + red-50 background

## Anti-Patterns (Page-specific)
- ✗ NO dark mode on checkout（信任感问题）
- ✗ NO animations on payment confirmation
```

### 上下文感知提示词模板

```
我正在构建 [页面名] 页面。
1. 阅读 design-system/MASTER.md
2. 检查 design-system/pages/[页面名].md
3. 若存在页面文件：其规则 > MASTER（覆盖关系）
4. 若不存在：仅使用 MASTER.md
技术栈: [具体栈]
任务: [需求]
```

### 与 LLM-Statelessness 的关系

这是"以文件系统为状态"的具体应用——不依赖 AI 的记忆（跨会话不存在），而是依赖项目文件（始终存在）。类似模式：AGENTS.md、CLAUDE.md、GEMINI.md 等项目上下文文件。

## 设计哲学总结（UUPM 系列）

1. **知识结构化优先于丰富性** — CSV + 优先级 + 条件判断，使 AI 可推理而非仅检索
2. **反模式比正模式更有价值** — 161 条规则的核心是行业经验的负样本库
3. **工具链感知** — 设计决策与实现路径合一（15 个栈专项指南）
4. **持久化解决无状态** — 设计决策写入文件系统，AI 读文件获得"记忆"
5. **零依赖实用主义** — BM25 + CSV + 标准库，可用性优先于精确性

## 来源

- [[raw/articles/UI-skill/blog-07-persistence.md]]

## 相关

- [[LLM-Statelessness]] — 此模式解决的根本问题
- [[Context-Engineering]] — 文件系统作为上下文的工程策略
- [[UI-UX-Pro-Max]] — 实现此模式的工具（--persist 参数）
- [[AI设计推理层]] — Master + Overrides 是设计推理层的持久化层
