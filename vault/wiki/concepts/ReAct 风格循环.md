---
type: concept
title: ReAct 风格循环
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 2
tags: [AI, 方法论, AI工程]
aliases:
- ReAct-style Loop
- ReAct 循环
- Thought-Command Loop
relates_to:
- target: '[[Agent循环]]'
  type: implements
  confidence: 0.95
- target: '[[LM Agent]]'
  type: uses
  confidence: 0.9
- target: '[[Agent计算机接口]]'
  type: related_to
  confidence: 0.85
supersedes: null
---

# ReAct 风格循环

## 概述

ReAct 风格循环是 [[SWE-agent]] 的运行框架：每一步生成 thought（思考）和 command（命令），再接收命令执行结果。这种"想一点、做一点、看反馈、再想一点"的循环天然适合高反馈密度的软件工程任务。

## 关键内容

### 运行机制

```
while task not complete:
    thought = LLM_think(current_context)
    command = LLM_act(thought, current_context)
    result = execute(command)
    context.append(thought, command, result)
```

### 与传统循环的区别

| 维度 | 传统循环 | ReAct 风格循环 |
|------|---------|--------------|
| 推理方式 | 先想完再一次输出 | 想一点、做一点 |
| 反馈密度 | 低 | 高 |
| 适用任务 | 静态生成 | 交互式任务 |

### 为什么重要

这让 agent 的推理与行动形成**显式耦合**：不是先想完一切再一次输出，而是想一点、做一点、看反馈、再想一点。对于软件工程这种高反馈密度任务，这种循环天然更合适。

### 与 ACI 的关系

ReAct 在这篇论文里不是创新点本身，但它是 ACI 能发挥作用的**运行框架**。没有这个循环，ACI 就只是静态工具集；有了这个循环，ACI 才变成动态工作环境。

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/03-SWE-agent 论文的所有核心概念 展开详细分析 一个一个.md]] — SWE-agent 核心概念分析
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/07-SWE-agent 轨迹 格式长什么样，怎么进行分析，怎么判断轨迹中哪些问题导致了后续任务的失败？.md]] — SWE-agent 轨迹分析方法论

## 相关

- [[Agent循环]] — implements（ReAct 是 Agent 循环的一种具体实现）
- [[LM Agent]] — uses（LM Agent 的运行框架）
- [[Agent计算机接口]] — related_to（ACI 需要 ReAct 循环才能发挥动态作用）
