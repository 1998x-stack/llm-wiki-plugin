---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [AI-Agent, Game-Testing, Knowledge-Management, Prompt-Engineering, AI工程]
aliases: ["Game Knowledge Injection", "游戏知识注入", "Per-Game Knowledge System"]
relates_to: 
  - target: "[[TITAN 框架]]"
    type: part_of
    confidence: 0.8
  - target: "[[Prompt-Engineering]]"
    type: implements
    confidence: 0.7
supersedes: null
---

# TITAN-游戏知识注入

## 概述
[[TITAN 框架|TITAN]]框架中的知识[[Configuration|配置]]体系，通过[[Configuration|配置]]文件将游戏规则和玩法知识注入LLM，使AI能够理解特定游戏的目标、规则和玩法机制。

## 关键内容

1. **知识[[Configuration|配置]]体系**：
   - 每个游戏有独立[[Configuration|配置]]文件(titan/game_configs/<game>.py)
   - 包含动作空间、重启键、最大步数、反思阈值等参数
   - 包含游戏规则和玩法的详细知识文本

2. **知识注入方式**：
   - 知识文本作为LLM System Prompt的一部分注入
   - 让LLM理解游戏规则和目标、操作方式和效果、可能的Bug表现
   - 通过[[Configuration|配置]]注入而非硬编码，新游戏只需添加[[Configuration|配置]]文件

3. **知识内容**：
   - 游戏基本规则（如贪吃蛇在20x20网格上，箭头键改变方向）
   - 操作效果（如吃食物得10分，撞墙或撞自己游戏结束）
   - 特殊机制（如速度随长度增加）

4. **设计优势**：
   - 知识注入而非硬编码：游戏规则通过[[Configuration|配置]]文件注入LLM
   - 易扩展：新游戏只需添加[[Configuration|配置]]文件
   - 适应性强：LLM可根据知识调整策略和行为

## 来源
- [[TITAN-技术框架核心点报告]] — 核心技术点六

## 相关
- [[TITAN 框架]] — part_of
- [[Prompt-Engineering]] — implements
- [[TITAN-状态感知层]] — relates_to
- [[Knowledge-Management]] — relates_to