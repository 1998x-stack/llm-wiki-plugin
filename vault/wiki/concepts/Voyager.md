---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: [LLM, 工具调用, 技能库, Minecraft, 自动课程, AI工程]
aliases: ["Voyager: An Open-Ended Embodied Agent with Large Language Models"]
relates_to: []
supersedes: null
---

# Voyager

## 概述
Voyager是由Wang等人提出的开放世界Minecraft环境中的具身智能体，它通过LLM实现了自动课程学习、[[Skills|技能]]库积累和迭代优化，是首个实现持久化[[Skills|技能]]存储的代表性系统。

## 关键内容

1. **系统架构**：
   - 自动课程模块：生成适当难度的任务序列
   - [[Skills|技能]]库：持久化存储可复用的[[Skills|技能]]程序
   - 迭代提示：[[代码生成]]与自我修复循环

2. **[[Skills|技能]]库机制**：
   - 每个成功的[[Skills|技能]]程序被存储为JavaScript函数，包含自然语言描述和向量嵌入
   - 新任务时通过语义检索找到相关[[Skills|技能]]
   - 支持[[零样本学习|零样本]]泛化，在新环境中复用已学[[Skills|技能]]

3. **关键技术贡献**：
   - 动态[[Skills|技能]]积累：在运行时自动产生和存储[[Skills|技能]]
   - 自动课程学习：根据当前状态生成合适的下一目标
   - 迭代自我修复：执行失败时反馈错误信息进行代码修复

4. **实验成果**：
   - 解锁的Minecraft物品种类是基线方法的3.3倍
   - 显著优于[[ReAct]]、Reflexion、AutoGPT等基线
   - 在新seed地图上保持[[零样本学习|零样本]]泛化能力

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Paper]] — "Voyager: An Open-Ended Embodied Agent with Large Language Models", NeurIPS 2023

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Skill-Library]] — relates_to
- [[Automatic-Curriculum]] — relates_to
- [[Self-Improvement]] — relates_to
- [[Embodied-Agent]] — relates_to