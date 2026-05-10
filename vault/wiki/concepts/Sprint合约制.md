---
type: concept
status: active
confidence: 0.88
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [技术, 方法论, AI, AI工程]
aliases: ["Sprint Contract", "Sprint合约谈判", "sprint contract"]
relates_to:
  - target: "[[生成器-评估器架构]]"
    type: part_of
    confidence: 0.92
  - target: "[[Agent Harness模式]]"
    type: part_of
    confidence: 0.85
  - target: "[[LLM-as-Judge]]"
    type: related_to
    confidence: 0.8
supersedes: null
---

# Sprint 合约制

## 概述

Sprint 合约制是[[生成器-评估器架构]]三 Agent 系统中的一个机制：在每个 Sprint 开始前，**[[生成器]]（[[生成器|Generator]]）和评估器（Evaluator）先行谈判并达成合约**，明确约定"完成"的具体标准和可验证行为，再开始编码实现。

## 关键内容

### 设计动机

产品规格（Planner 输出）是高层次的用户故事集合，刻意避免过度规定实现细节，以防止早期的错误规格向下游传播。但这带来了一个问题：**[[生成器]]在缺乏具体可测试目标时，容易构建表面正确但缺乏深度的实现**。

Sprint 合约制作为"规格与代码之间的桥梁"，将高层用户故事转化为具体的、可测试的实现约定。

### 工作流程

```
Planner 输出规格（高层）
      ↓
Generator 提案：我将构建 X，用 Y 方式验证成功
      ↓
Evaluator 审查提案（是否构建了正确的东西？）
      ↓
双方迭代直至达成合约
      ↓
Generator 依据合约构建
      ↓
Evaluator 对照合约执行 QA（Playwright MCP）
```

### 合约的粒度

合约非常细粒度，以确保 QA 可以精确验证。以全栈游戏制作工具为例，一个 Sprint（第 3 关卡编辑器）包含 **27 个独立测试条件**，例如：

- "矩形填充工具允许点击拖拽填充矩形区域"
- "用户可以选中并删除已放置的实体生成点"
- "用户可通过 API 重新排列动画帧顺序"

这种粒度使评估器的发现足够具体，可以直接触发修复，无需额外调查。

### 文件通信协议

合约通过文件传递实现：
- [[生成器]]写入提案文件
- 评估器读取并在同一文件（或新文件）中回应
- 前一 Agent 再读取响应继续迭代

这种文件驱动的通信方式保持了 Agent 间的松耦合，同时保留了完整的协商记录。

### 局限与演化

Sprint 合约制是 Sprint 分解结构的组成部分。当 [[Anthropic]] 在 [[Claude_Opus_4.6|Opus 4.6]] 上移除 Sprint 分解（模型能力提升，不再需要分块）时，Sprint 合约制也随之移除，评估器改为在完整构建结束后进行一次性 QA。

这再次印证了 Harness 组件随模型能力演化而调整的原则。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/Harness design for long-running application development.md]]

## 相关

- [[生成器-评估器架构]] — part_of（Sprint 合约制是三 Agent 架构中特定阶段的机制）
- [[Agent Harness模式]] — part_of（具体 Harness 设计决策）
- [[LLM-as-Judge]] — related_to（评估器在合约谈判中充当初步 Judge 角色）
- [[Prithvi-Rajasekaran]] — 设计者
