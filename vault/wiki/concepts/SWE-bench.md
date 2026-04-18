---
type: concept
title: SWE-bench
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 4
tags: [AI, 方法论, AI工程]
aliases:
- SWE-bench
- Software Engineering Benchmark
relates_to:
- target: '[[Agent计算机接口]]'
  type: uses
  confidence: 0.9
- target: '[[Agent评估方法论]]'
  type: implements
  confidence: 0.9
- target: '[[DeepAgents评估体系]]'
  type: compares_to
  confidence: 0.8
- target: '[[HumanEvalFix]]'
  type: compares_to
  confidence: 0.9
supersedes: null
---

# SWE-bench

## 概述

SWE-bench 是软件工程 Agent 的基准测试集，用于评估 AI Agent 自动修复 GitHub 仓库中真实 issue 和 bug 的能力。采用 pass@1 指标，即 Agent 一次性成功修复问题的比例。

## 关键内容

### 测试机制

- 从真实 GitHub 仓库中抽取 issue 和对应的修复 commit
- Agent 接收 issue 描述和代码库访问权限
- 通过运行仓库测试套件验证修复是否正确
- **pass@1**：单次尝试成功修复的比例

### 代表性结果

- **[[SWE-agent]]**（Princeton 2024）：
  - SWE-bench Full：**12.47%** resolved（GPT-4 Turbo）
  - SWE-bench Lite：**18.00%** resolved（GPT-4 Turbo）
  - pass@k 曲线：k=6 时解决率升至 30%+，但单题波动明显
- **Shell-only agent**（GPT-4 Turbo）：Lite 上 **11.00%**
- **RAG**（GPT-4 Turbo）：Full 上 1.31%，Lite 上 2.67%

该结果被用来支撑核心论点：交互式 Agent + 专门设计的 ACI，比"只让模型直接输出 patch"更适合真实软件工程任务。

### 在 ACI 研究中的角色

[[Agent计算机接口]] 研究中，SWE-bench 被用作工具设计质量的验证平台：
- [[Anthropic]] 在 SWE-bench 中花费在工具优化上的时间多于整体提示词优化
- 仅改工具描述就在 SWE-bench 上达到 SOTA
- 证明了"接口设计质量直接决定 Agent 成功率"的核心假设

### 与其他评估体系的对比

| 维度 | SWE-bench | [[HumanEvalFix]] | [[DeepAgents评估体系]] |
|------|----------|-----------------|---------------------|
| 评估对象 | 真实仓库 issue 修复 | 单函数级代码修复 | 多轮 Agent 轨迹 |
| 粒度 | 仓库级（跨文件） | 函数级 | 工作流级 |
| 指标 | pass@1 成功率 | pass@1 成功率 | 成功断言 + 效率断言 |
| [[SWE-agent]] pass@1 | 12.5% | 87.7% | — |
| 场景 | 静态代码修复 | 静态代码修复 | 动态多步工作流 |

[[SWE-agent]] 在 [[HumanEvalFix]] 上 87.7% vs SWE-bench 上 12.5% 的巨大差距说明：ACI 设计在复杂任务上的价值远大于简单任务——当任务复杂度从函数级提升到仓库级时，好的交互界面带来的优势更加显著。

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/01-SWE agent论文 主要讲解什么核心点，什么观点？.md]] — ChatGPT 对话总结
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/02-SWE-agent 论文的 5 页读书笔记版".md]] — SWE-agent 论文 5 页读书笔记
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/03-SWE-agent 论文的所有核心概念 展开详细分析 一个一个.md]] — SWE-agent 24 个核心概念词条分析
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/05-SWE agent 有哪些图表，每个图表核心内容和核心观点是什么？.md]] — SWE-agent 论文图表分析

## 相关

- [[Agent计算机接口]] — uses（SWE-bench 是 ACI 设计质量的验证平台）
- [[Agent评估方法论]] — implements（软件工程 Agent 的标准基准）
- [[DeepAgents评估体系]] — compares_to（不同的评估范式）
- [[HumanEvalFix]] — compares_to（不同粒度的代码修复基准，SWE-agent 87.7% vs 12.5%）
