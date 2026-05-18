---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [feature-flag, development, growthbook, AI工程]
aliases: ["Feature Flag System", "功能标志系统", "GrowthBook"]
relates_to: 
  - target: "[[Claude Code]]"
    type: used_in
    confidence: 0.9
  - target: "[[GrowthBook]]"
    type: implements
    confidence: 0.9
  - target: "[[Anthropic]]"
    type: developed_by
    confidence: 0.8
supersedes: null
---

# Feature Flag 系统

## 概述
Feature Flag 系统是 [[Claude Code]] 中使用的特性标志系统，用于控制不同功能的开启与关闭，支持多种编译时开关。

## 关键内容

1. **技术实现**：
   - [[Claude Code]] 使用 GrowthBook 作为特性标志系统
   - 同时辅以编译时 Feature Flag
   - 支持动态开启/关闭功能，无需重新部署

2. **主要功能标志**：
   - [[KAIROS]]: 常驻[[KAIROS|自主守护进程]]（未发布）
   - PROACTIVE: 主动行为触发（未发布）
   - [[Buddy|BUDDY]]: Tamagotchi 宠物系统（计划 2026/05）
   - [[ULTRAPLAN]]: 云端 30 分钟规划会话（未发布）
   - [[VOICE_MODE]]: 语音接口（未发布）
   - BRIDGE_MODE: IDE [[Bridge Mode|桥接模式]]（部分发布）
   - COORDINATOR: 多智能体协调（部分发布）
   - ANTI_DISTILLATION_CC: 反蒸馏保护（内部启用）
   - NATIVE_CLIENT_ATTESTATION: 原生[[客户端证明]]（内部启用）
   - [[PENGUIN_MODE]]: [[PENGUIN_MODE|企鹅模式]]（含义未知，实验性）

3. **应用价值**：
   - 支持灰度发布和 A/B 测试
   - 控制未完成功能的可见性
   - 在不同环境中启用/禁用特定功能
   - 允许快速回滚有缺陷的功能

## 来源
- [[01_overview_architecture]] — Feature Flag 系统描述

## 相关
- [[Claude Code]] — used_in
- [[GrowthBook]] — implements
- [[KAIROS]] — feature_flag