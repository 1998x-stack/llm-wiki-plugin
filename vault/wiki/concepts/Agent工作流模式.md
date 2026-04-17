---
type: concept
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 2
tags: [技术, AI, 方法论, AI工程]
aliases: ["Agent工作流", "LLM工作流", "Agentic Systems Patterns", "五种工作流模式", "workflow patterns"]
relates_to:
  - target: "[[Agent Harness模式]]"
    type: extends
    confidence: 0.9
  - target: "[[生成器-评估器架构]]"
    type: related_to
    confidence: 0.88
  - target: "[[Agent循环]]"
    type: part_of
    confidence: 0.85
  - target: "[[多Agent架构]]"
    type: related_to
    confidence: 0.85
supersedes: null
---

# Agent 工作流模式

## 概述

Anthropic 从与数十个客户团队协作中提炼的 LLM 系统架构分类：**工作流**（LLM 和工具经由预定义代码路径编排）与**Agent**（LLM 动态决定自身流程和工具使用）的根本区别，以及五种核心工作流构建块。

## 关键内容

### 工作流 vs. Agent 的根本区别

| | 工作流（Workflow） | Agent |
|--|--|--|
| 控制权 | 代码路径预定义，程序员掌控 | LLM 动态决定 |
| 预测性 | 高 | 低 |
| 适用场景 | 任务结构清晰，步骤可预知 | 开放性问题，步骤数量无法提前确定 |
| 代价 | 灵活性有限 | 延迟高、成本高、错误可累积 |

**核心原则**："Find the simplest solution possible, and only increase complexity when needed."——许多应用优化单个 LLM 调用 + 检索 + in-context 示例即可，不需要多步 Agent 系统。

### 五种核心工作流模式

#### 1. 提示链（Prompt Chaining）
将任务分解为顺序步骤，每次 LLM 调用处理前一次的输出，可加入程序化检查门（Gate）。

**适用**：任务可清晰分解为固定子任务，以延迟换精度。
**例**：生成营销文案 → 翻译为另一种语言；写大纲 → 检查标准 → 基于大纲写文档。

#### 2. 路由（Routing）
对输入分类，导向专门的后续处理路径，实现关注点分离和专业化提示。

**适用**：有多个明确类别需分别处理，且分类本身可以准确执行。
**例**：客服查询分流（退款 / 技术支持 / 一般问题）；简单问题路由到 Haiku 4.5，复杂问题路由到 [[Claude-Sonnet-4|Sonnet 4]].5。

#### 3. 并行化（Parallelization）
LLM 同时处理任务，结果聚合。两个变体：
- **Sectioning**：将任务拆分为独立子任务并行执行
- **Voting**：多次执行相同任务获得多样输出，取多数或最佳

**适用**：子任务可并行（速度），或需要多视角/多次尝试（置信度）。
**例**：一个实例处理用户查询，另一个同步筛查不当内容；多个提示分别审查代码漏洞。

#### 4. 编排者-工人（Orchestrator-Workers）
中心 LLM 动态分解任务，将子任务委派给工人 LLM，综合结果。

**与并行化的关键区别**：子任务由编排者基于输入动态决定，而非预先硬编码。
**适用**：无法预知子任务数量和性质的复杂任务（如代码修改涉及哪些文件）。

#### 5. 评估者-优化者（Evaluator-Optimizer）
一个 LLM 生成响应，另一个在循环中提供评估和反馈。

**与[[生成器-评估器架构]]的关系**：这是同一架构模式的通用描述，Anthropic 的三 Agent 系统是具体实现。
**适用标准**：① LLM 响应在人类反馈下可显著改善；② LLM 能够提供此类反馈。
**例**：文学翻译（译者 + 评审）；复杂信息搜集任务（评估者决定是否需要进一步搜索）。

### Agent（自主 Agent）

真正的 Agent 是 LLM 基于[[环境反馈设计|环境反馈]]在循环中使用工具。关键特征：
- 任务明确后**独立计划执行**，必要时回来寻求帮助
- 每步从环境获取"ground truth"（工具调用结果、代码执行结果）
- 支持停止条件（最大迭代数），必要时暂停等待人类反馈

**适用**：开放性问题，无法提前预知步骤数；需要扩展性自主任务。

### Agent 计算机接口（ACI）

类比人机接口（HCI），为 Agent 设计工具接口需要同等投入：
- 工具描述应像给初级开发者写文档
- 参数明确、无歧义（`user_id` 优于 `user`）
- 让 Agent 使用工具，观察错误，迭代改进描述
- Poka-yoke（防呆设计）：让错误难以发生（如强制使用绝对路径）

### 设计原则摘要

1. **保持 Agent 设计的简洁性**
2. **透明性**：明确展示 Agent 的规划步骤
3. **工具文档和测试**：与 [[Agent计算机接口|ACI]] 设计同等重要

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/Building Effective AI Agents.md]]
- [[raw/articles/ai-engineering/anthropic-engineering/Claude SWE-Bench Performance.md]]

## 相关

- [[Agent Harness模式]] — extends（五种模式是具体 Harness 实现的基础架构选择）
- [[生成器-评估器架构]] — related_to（评估者-优化者工作流的具体实现案例）
- [[Agent循环]] — part_of（五种工作流都基于 Agent 循环）
- [[多Agent架构]] — related_to（编排者-工人是多 Agent 系统的核心模式）
- [[LLM-as-Judge]] — related_to（评估者-优化者工作流的评估机制）
