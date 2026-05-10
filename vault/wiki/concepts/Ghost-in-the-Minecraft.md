---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [LLM, 工具调用, 技能库, 任务分解]
aliases: ["Ghost in the Minecraft", "GITM"]
relates_to: []
supersedes: null
---

# Ghost in the Minecraft

## 概述
Ghost in the Minecraft（GITM）是由Zhu等人提出的开放世界环境中的一般能力代理系统，通过LLM结合基于文本的知识和记忆来实现。与[[Voyager]]不同，GITM强调任务分解而非单步操作。

## 关键内容

1. **核心理念**：
   - 对于复杂任务，先进行任务分解，再映射到基本原语（primitive action）
   - 将复杂目标分解为子目标树，通过LLM进行层次化分解

2. **任务[[Factorization Machines|分解机]]制**：
   - 复杂目标自动分解为子目标树
   - 每个子目标对应可验证的子任务
   - 示例："制作钻石剑"分解为获取钻石、制作钻石镐等多个子步骤

3. **记忆模块**：
   - 成功记忆：记录有效的分解策略
   - 失败记忆：记录会导致死锁的路径（如"想挖矿但没有镐"）
   - 这些记忆作为few-shot示例注入LLM以指导后续任务

4. **与[[Voyager]]的差异**：
   - [[Voyager]]使用代码函数作为[[Skills|技能]]单元
   - GITM使用任务分解树作为核心机制
   - GITM更强调任务分解和[[Memory-Management|记忆管理]]

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Paper]] — "Ghost in the Minecraft: Generally Capable Agents for Open-World Environments via Large Language Models with Text-based Knowledge and Memory", 2023

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Voyager]] — relates_to
- [[Task-Decomposition]] — relates_to
- [[Embodied-Agent]] — relates_to
- [[Memory-Module]] — relates_to