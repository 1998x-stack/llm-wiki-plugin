---
type: concept
title: Localization
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 3
tags: [AI, 技术, AI工程]
aliases:
- 代码定位
- Localization
- File-level Localization
- Line-level Localization
relates_to:
- target: '[[Agent计算机接口]]'
  type: uses
  confidence: 0.9
- target: '[[SWE-bench]]'
  type: related_to
  confidence: 0.85
supersedes: null
---

# Localization

## 概述

Localization（代码定位）是软件工程 Agent 的关键子任务，包括文件级定位（找到相关文件）和行级定位（找到精确修改位置）。它是 SWE agent 的本质瓶颈之一。

## 关键内容

### 两层定位

| 层级 | 任务 | 难度 |
|------|------|------|
| **File-level** | 找到相关文件 | 中 |
| **Line-level** | 找到精确修改位置 | 高 |

### 为什么是瓶颈

> "找不到正确位置，再强的编辑能力也没有意义；找错位置，后续动作都会建立在错误假设上。"

真实软件工程最难的往往不是"最后改那几行代码"，而是先**找到该改哪里**。[[仓库]]级搜索能力实际上决定了 agent 是否能把问题缩到可操作范围。

### 搜索方式的发现

论文 Table 3 显示不同搜索接口差异明显：
- **Summarized search** 效果最好
- **Iterative search** 次之——让 agent 容易把每个结果都看一遍，导致成本和上下文被耗尽
- **No search** 不是最差，但也不如总结式搜索

这说明"搜索能力"不是简单加个 grep 就行，关键在**结果呈现方式**。

### 后续演进方向

[[SWE-agent]] 虽然没把 localization 当成唯一主题，但它实际上指出：
> SWE agent 的本质瓶颈之一是"从 issue 文本到代码位置"的映射能力。

后续工作因此更关注：
- Repository maps
- Symbol index
- Static analysis
- Call graph

### 成功轨迹的行为模式（Figure 7）

Figure 7 统计了成功解决的 [[SWE-bench]] 任务中各 turn 的动作调用频率：
- **前几轮**：主要是 `find_file`、`search_dir`、`open` 等定位动作
- **后几轮**：主要是 `edit`、`python`、`pytest` 等修改和验证动作

这说明成功的 [[SWE-agent]] 轨迹不是一上来就改代码，而是**先定位，再进入编辑-验证闭环**。

### 失败模式分布（Figure 8）

Figure 8 把未解决任务按失败类型做了分布统计：
- **Incorrect Implementation** + **Overly Specific Implementation**：~52.0%（最[[大类]]别）
- **Failed to Recover from Edit**：~23.4%（与编辑恢复相关）
- **Failed to Find Edit Location**：定位失败
- **Failed to Find Relevant File**：文件级定位失败

这说明 [[SWE-agent]] 的主要瓶颈已经不只是"找不到文件"，而是"方案本身不够对"或"改坏后恢复不了"。接口设计解决了不少导航/编辑问题，但真正的功能性推理和泛化实现仍然是主要难点。

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/03-SWE-agent 论文的所有核心概念 展开详细分析 一个一个.md]] — SWE-agent 核心概念分析
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/05-SWE agent 有哪些图表，每个图表核心内容和核心观点是什么？.md]] — SWE-agent 论文图表分析
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/07-SWE-agent 轨迹 格式长什么样，怎么进行分析，怎么判断轨迹中哪些问题导致了后续任务的失败？.md]] — SWE-agent 轨迹分析方法论

## 相关

- [[Agent计算机接口]] — uses（Localization 是 ACI 的核心组件之一）
- [[SWE-bench]] — related_to（Localization 能力直接影响 SWE-bench 表现）
