---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [LLM, 工具调用, 技能库, Claude Code]
aliases: ["Claude Code .skill 文件", "Skill 文件设计"]
relates_to: []
supersedes: null
---

# Claude Code .skill 文件

## 概述
[[Claude Code]] .skill文件是学术界LLM[[Skills|技能]]研究的工程实践产物，将多年研究的[[Skills|技能]]管理、工具调用、任务规划等理论转化为可操作的工程实现。它代表了学术洞见在实际开发中的应用。

## 关键内容

1. **设计哲学与学术支撑**：
   - description字段对应Gorilla的检索机制，是LLM检索相关[[Skills|技能]]的语义锚点
   - 代码模板对应[[CRAFT]]的代码复用理念，提供可执行的代码[[骨骼系统|骨架]]
   - 工作流对应GITM的任务分解树，将复杂任务分解为可验证子目标
   - 约束规则对应[[Toolformer]]的负样本过滤机制

2. **核心组成部分**：
   - name：[[Skills|技能]]标识
   - description：触发词密集的自然语言描述，用于[[Skills|技能]]检索
   - 工作流：任务分解的线性展开
   - 代码模板：可执行的代码[[骨骼系统|骨架]]
   - 约束与禁忌：负样本示例和使用限制
   - 示例：Few-shot示例

3. **与学术研究的对应关系**：
   - 工具检索 ←→ Gorilla、[[AnyTool]]
   - [[Skills|技能]]库 ←→ [[Voyager]]
   - 任务分解 ←→ GITM、[[HuggingGPT]]
   - 示例演示 ←→ [[ReAct]]、[[Toolformer]]
   - 文档质量 ←→ [[API-Bank]]
   - 验证机制 ←→ [[AssistGPT]] PEIL

4. **未来发展路径**：
   - 从纯人工定义到半自动生成（结合LATM工具制造思路）
   - 支持[[Skills|技能]]冲突处理、动态[[Skills|技能]]生成、版本管理等功能

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Claude-Code-Docs]] — Claude Code官方文档

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Tool-Use]] — relates_to
- [[Skill-Library]] — relates_to
- [[Code-Template]] — relates_to
- [[Task-Decomposition]] — relates_to