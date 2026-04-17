---
type: concept
title: ACI 设计原则
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 3
tags: [AI, 方法论, 技术, AI工程]
aliases:
- ACI Design Principles
- Agent-Computer Interface 设计原则
relates_to:
- target: '[[Agent计算机接口]]'
  type: part_of
  confidence: 1.0
- target: '[[Guardrails]]'
  type: extends
  confidence: 0.9
- target: '[[LM Agent]]'
  type: uses
  confidence: 0.9
- target: '[[环境反馈设计]]'
  type: extends
  confidence: 0.95
- target: '[[状态变化感知]]'
  type: extends
  confidence: 0.95
- target: '[[恢复机制]]'
  type: extends
  confidence: 0.9
supersedes: null
---

# ACI 设计原则

## 概述

ACI 设计原则是 [[SWE-agent]] 论文在 [[Agent计算机接口]] 研究中总结的一组方法论，包括四条核心原则：动作简单明确、反馈简洁高密度、[[状态变化感知|状态可见性]]、[[Guardrails|护栏机制]]。这些原则是论文最有方法论价值的贡献。

## 关键内容

### 原则一：动作要简单、容易理解

> "Actions should be simple and easy to understand for agents."

- 很多 bash 命令太灵活、太开放、语义负担太重，对 LM 不友好
- 少量、清晰、功能边界明确的动作更好
- 背后的逻辑：语言模型对"语义上明确的工具"更容易形成稳定使用模式，而对几乎无限制的 shell 容易出现动作选择混乱

**实验支撑**：Shell-only baseline 对比证明，为 LM 专门设计的动作集优于原始 Linux shell。

### 原则二：反馈要简洁、信息密度高

> "Feedback should be specific and concise."

- 人类可以忽略无关信息，但对 LM 来说所有内容都有固定 token 成本和干扰成本
- ACI 的反馈设计本质上是"压缩状态表示"——加工成足够行动、又不至于淹没[[上下文窗口]]的观察
- 这个点对今天所有 agent 仍然成立

### 原则三：帮助模型感知状态变化

- 好的 ACI 应该帮助 agent 理解当前状态、此前改动的后果、以及最近动作的结果
- 编辑后给出更新后的文件片段，就是"[[状态变化感知|状态可见性]]"的例子
- 本质：把软件工程从"token continuation"变成"stateful control"

### 原则四：要有 Guardrails（护栏）

- [[Guardrails]] 可以减少错误传播、加速恢复
- 例如在编辑动作中加入 syntax checker
- 不是锦上添花，而是 agent 系统稳定性的核心——LM 很容易在早期引入小错误，然后整条轨迹被污染
- Guardrail 的作用是在"错误刚出现时"把它截断

### 实验验证

论文通过 [[Ablation Study|消融实验]] 验证了这些原则：
- 总结式搜索优于迭代式搜索（原则二：反馈简洁）
- 100-line viewer 优于太小或全文件（原则二：信息密度）
- Edit + linting 优于无 linting（原则四：[[Guardrails]]）
- 最近 5 条 observation 优于 full history（原则二：简洁反馈）

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/03-SWE-agent 论文的所有核心概念 展开详细分析 一个一个.md]] — SWE-agent 核心概念分析
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/04-SWE agent 如何保证 搜索是否高效、编辑是否稳定、反馈是否足够、上下文是否可控、恢复机制是否.md]] — SWE-agent 五大保障机制分析

## 相关

- [[Agent计算机接口]] — part_of（ACI 设计原则是 ACI 研究的方法论核心）
- [[Guardrails]] — extends（原则四的具体实现）
- [[LM Agent]] — uses（这些原则服务于 LM Agent 的有效行动）
- [[环境反馈设计]] — extends（原则二"反馈简洁高密度"的具体实现）
- [[状态变化感知]] — extends（原则三"状态可见性"的具体实现）
- [[恢复机制]] — extends（原则四"护栏机制"的恢复策略实现）
