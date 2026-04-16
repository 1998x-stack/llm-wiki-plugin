---
type: concept
title: "PDDL"
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 工具，方法论, 机器人学]
aliases: ["Planning Domain Definition Language", "规划领域定义语言"]
relates_to:
  - target: "[[STRIPS 规划器]]"
    type: extends
    confidence: 1.0
  - target: "[[国际规划竞赛]]"
    type: implements
    confidence: 0.9
supersedes: null
---

# PDDL

## 概述
PDDL（Planning Domain Definition Language，规划领域定义语言）是自动规划领域的标准建模语言，由 Drew McDermott 等人于 1998 年为国际规划竞赛（IPC）设计。PDDL 本质上是 [[STRIPS 规划器]] 表示法的形式化、标准化及扩展版本。它采用 [[STRIPS 规划器|STRIPS]] 风格的操作符定义（前提条件、效果）来描述规划领域，并用逻辑谓词描述初始状态和目标条件。随着版本的演进（如 PDDL 2.1 引入时间和数值，PDDL 3.0 引入偏好），PDDL 已成为连接不同规划算法与应用程序的通用接口，支撑着全球规划器的基准评测与研究交流。

## 关键内容

### 起源与 STRIPS 的继承
PDDL 的诞生旨在解决自动规划研究中缺乏统一测试标准的问题。其核心语法和语义直接继承自 1971 年的 [[STRIPS 规划器|STRIPS]] 框架：
*   **领域定义（Domain Definition）**：定义类型、谓词（Predicates）和操作符（Actions/Operators）。每个操作符依然遵循 [[STRIPS 规划器|STRIPS]] 的“前提条件 - 添加列表 - 删除列表”结构（在 PDDL 中表现为 `:precondition` 和 `:effect`）。
*   **问题定义（Problem Definition）**：定义具体的对象实例、初始状态（Initial State）和目标状态（Goal State）。

这种设计使得经典的 [[STRIPS 规划器]]可以直接处理早期的 PDDL 子集，保证了技术的延续性。

### 版本演进与功能扩展
为了适应更复杂的现实应用，PDDL 经历了多次重要升级：
*   **PDDL 1.2**：引入了基本的需求限制，支持量化效果。
*   **PDDL 2.1**：这是一个里程碑式的版本，引入了时间维度（Durative Actions）和数值 fluents（Numeric Fluents），使得规划器可以处理资源约束和时序规划问题，突破了原始 [[STRIPS 规划器|STRIPS]] 仅处理离散逻辑状态的局限。
*   **PDDL 3.0**：增加了软约束、偏好表达以及轨迹约束，允许用户指定“最好避免”的状态而不仅仅是“必须避免”的状态。

### 在国际规划竞赛中的作用
PDDL 是国际规划竞赛（IPC）的官方输入格式。每届竞赛中，来自世界各地的研究团队提交各自的规划器（如 Fast Downward, LAMA 等），在统一的 PDDL 问题集上进行比拼。这种标准化的评测机制极大地推动了规划算法的效率提升和技术创新，使得现代规划器能够在秒级时间内解决包含数千个谓词的复杂问题，而这些问题是原始 [[STRIPS 规划器|STRIPS]] 无法想象的。

### 与大语言模型的结合
在人工智能的新时代，PDDL 展现出了新的生命力。研究者发现，大语言模型（LLM）擅长将模糊的自然语言指令转化为结构化的 PDDL 描述，而经典的 PDDL 规划器则能保证生成计划的逻辑正确性和完备性。这种"LLM + PDDL"的混合架构正在成为具身智能和复杂任务自动化的重要技术路线，证明了 [[STRIPS 规划器|STRIPS]]/PDDL 范式在半个世纪后依然具有核心价值。

## 来源
- [[raw/books/机器人学/04-fikes-nilsson-strips-planner.md]]

## 相关
- [[STRIPS 规划器]]
- [[国际规划竞赛]]