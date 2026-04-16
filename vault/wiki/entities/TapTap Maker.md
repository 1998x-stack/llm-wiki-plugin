---
type: entity
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["AI工程", "工具与框架"]
aliases: ["TTM", "TapTap 游戏制作工具", "AI 游戏引擎"]
relates_to:
  - target: "[[Cursor]]"
    type: compares_to
    confidence: 0.8
  - target: "[[Unity]]"
    type: compares_to
    confidence: 0.85
  - target: "[[AI 原生架构]]"
    type: implements
    confidence: 0.9
supersedes: null
entity_type: project
---

# TapTap Maker

## 概述
TapTap 旗下的 AI 原生游戏开发工具（TTM），专为 AI 设计的游戏引擎，支持组件化开发、技能库系统，已支持 30 万行中型游戏，具备开发-发布全闭环能力。

## 关键内容

1. **[[AI 原生架构]]**：GUI 不适合 AI，优先为 Agent 设计架构，面向「Agent + 人」双端。给 AI 灌技能（游戏品类开发流程的抽象理解），而非灌知识或堆 Demo。

2. **技能库系统**：重质不重量，不乱加技能以保证不降低 Agent 性能，优先做组件化。

3. **[[上下文漂移]]问题**：行业通病"改 A 坏 B"，靠拆会话、组件解耦缓解，长期靠模型升级。

4. **隐藏代码设计**：普通用户编程不如 AI，不用看代码，专注玩法创意；未来可能开放，但现在不重要。

5. **规模能力**：已支持 30 万行中型游戏，架构不乱，几十万行都能扛。

6. **人机共创**：不自动判断可玩性，只执行创作者指令，AI 给方案，人做决定。

7. **竞争壁垒**：相比 Cursor 等通用工具——有专业游戏引擎 + 垂直数据 + 开发-发布全闭环；相比 Unity——无历史包袱，引擎专为 AI 设计。

8. **商业化**：现在免费是主动策略，算力成本逐年大跌，换平台独家内容更值；积分防滥用，商业化还在摸索。

## 来源
- [[黎叔的硅星人 Pro 的采访]] — 硅星人 Pro 采访笔记

## 相关
- [[Cursor]] — compares_to
- [[Unity]] — compares_to
- [[AI 原生架构]] — implements
