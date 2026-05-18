---
type: concept
title: LM Agent
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [AI, 方法论, AI工程]
aliases:
- Language Model Agent
- 语言模型智能体
- LM as Agent
relates_to:
- target: '[[Agent计算机接口]]'
  type: uses
  confidence: 1.0
- target: '[[Agent循环]]'
  type: implements
  confidence: 0.95
- target: '[[Agent工作流模式]]'
  type: related_to
  confidence: 0.85
supersedes: null
---

# LM Agent

## 概述

LM Agent 是将[[Language-Model|语言模型]]从"回答问题的文本系统"重新定义为"在环境中反复采取行动并接收反馈的决策体"的[[规范化理论|范式]]。这一[[规范化理论|范式]]转换是 [[SWE-agent]] 论文最底层的理论基础。

## 关键内容

### 定义

> "LM acts as an agent when it iteratively takes actions and receives feedback."

论文将 LM Agent 定义为：一个[[Language-Model|语言模型]]在环境中反复采取动作并接收反馈的系统。这决定了整篇论文的视角——研究的不是"[[代码生成]]"，而是"模型如何在软件工程环境里完成任务"。

### 范式转换

| 维度 | 传统视角 | LM Agent 视角 |
|------|---------|-------------|
| 模型角色 | 文本[[生成器]] | 环境中的决策体 |
| 关注点 | Prompt 和代码 token 预测 | 动作空间、反馈格式、状态表示、错误恢复 |
| 任务性质 | 静态生成 | 迭代交互 |
| 评估方式 | 输出质量 | 任务完成度（% Resolved） |

### 为什么重要

这一定义是整篇论文的[[规范化理论|范式]]转换。只要接受"LM 是 agent"，后续 ACI、[[Guardrails|护栏机制]]、[[Context-Engineering|上下文管理]] 等概念才成立。否则会将 [[SWE-agent]] 误解为"一个会自动改代码的 prompt workflow"。

### 与 Agent 循环的关系

LM Agent 的实现依赖于 [[Agent循环]]：
```
while (true):
    response = LLM(messages + tools)
    if response.stopReason == "stop": break
    if response.stopReason == "toolUse": execute_tools()
```
[[SWE-agent]] 在此基础上采用 [[ReAct 风格循环]]：每一步生成 thought + command，再接收执行结果。

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/03-SWE-agent 论文的所有核心概念 展开详细分析 一个一个.md]] — SWE-agent 核心概念分析

## 相关

- [[Agent计算机接口]] — uses（LM Agent 需要专门的 ACI 才能有效行动）
- [[Agent循环]] — implements（LM Agent 的运行机制）
- [[Agent工作流模式]] — related_to（LM Agent 在工作流中的角色）
