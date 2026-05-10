---
type: concept
title: HumanEvalFix
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 3
tags: [AI, 方法论, AI工程]
aliases:
- HumanEvalFix
- 代码修复基准
relates_to:
- target: '[[SWE-bench]]'
  type: compares_to
  confidence: 0.9
- target: '[[Agent计算机接口]]'
  type: uses
  confidence: 0.85
supersedes: null
---

# HumanEvalFix

## 概述

HumanEvalFix 是代码修复能力的基准测试，评估 AI 模型或 Agent 在给定有缺陷的代码后，能否正确修复 bug 并通过所有测试用例。与 [[SWE-bench]] 聚焦真实[[仓库]] issue 不同，HumanEvalFix 更侧重单函数级别的代码修复能力。

## 关键内容

### 测试机制

- 提供包含 bug 的代码片段
- Agent/模型需要识别并修复 bug
- 通过运行预定义的测试用例验证修复正确性
- **pass@1**：单次尝试成功修复的比例

### 代表性结果

- **[[SWE-agent]]**（GPT-4 Turbo）：
  - [[Python]]：**87.7%** pass@1
  - JavaScript：**89.7%** pass@1
  - Java：**87.9%** pass@1
- 与 [[SWE-bench]] 上的 12.5% 形成对比——在简单函数级修复上表现优秀，但在真实[[仓库]]级 issue 修复上仍有很大提升空间

### 与 SWE-bench 的对比

| 维度 | HumanEvalFix | [[SWE-bench]] |
|------|-------------|--------------|
| 粒度 | 单函数级别 | 真实[[仓库]] issue 级别 |
| 复杂度 | 低（上下文有限） | 高（需跨文件导航） |
| [[SWE-agent]] pass@1 | 87.7% | 12.5% |
| 评估重点 | 代码修复正确性 | 完整工程工作流 |

这一差距说明：ACI 设计在复杂任务上的价值远大于简单任务——当任务复杂度提升时，好的交互界面带来的优势更加显著。

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/02-SWE-agent 论文的 5 页读书笔记版".md]] — ChatGPT 对话总结
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/03-SWE-agent 论文的所有核心概念 展开详细分析 一个一个.md]] — SWE-agent 24 个核心概念词条分析
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/05-SWE agent 有哪些图表，每个图表核心内容和核心观点是什么？.md]] — SWE-agent 论文图表分析

## 相关

- [[SWE-bench]] — compares_to（不同粒度的代码修复基准）
- [[Agent计算机接口]] — uses（SWE-agent 在 HumanEvalFix 上的结果支撑 ACI 有效性）
