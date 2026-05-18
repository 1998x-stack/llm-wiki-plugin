---
type: concept
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [技术, AI, 方法论, AI工程]
aliases: ["think tool", "Think Tool", "思考工具", "显式思考工具"]
relates_to:
  - target: "[[Agent工作流模式]]"
    type: part_of
    confidence: 0.85
  - target: "[[Agent Harness模式]]"
    type: related_to
    confidence: 0.8
supersedes: null
---

# Think 工具

## 概述

[[Think 工具]]是一个无副作用的特殊工具：模型调用它时，输入文本被追加到日志中作为"思考"，不获取新信息，不修改任何状态。它为模型在复杂工具链中提供一个**结构化的中间推理空间**，在 [[τ-Bench]] 航空领域基准中实现了 **54% 的相对性能提升**。

## 关键内容

### Think 工具 vs 扩展思考（Extended Thinking）

| | [[Think 工具]] | [[扩展思维|扩展思考]]（[[扩展思维|Extended Thinking]]） |
|--|--|--|
| 时机 | 响应生成过程中（处理工具调用结果后） | 开始生成响应之前 |
| 用途 | 分析新收到的工具结果，判断下一步 | 深度规划，迭代考虑方案 |
| 适合 | 长工具链、策略密集型环境、顺序决策 | 简单工具调用、编码/数学/物理（无需调用工具） |
| 推理深度 | 更聚焦于新发现的信息 | 更全面 |

### 标准工具定义

```json
{
  "name": "think",
  "description": "Use the tool to think about something. It will not obtain new information or change the database, but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.",
  "input_schema": {
    "type": "object",
    "properties": {
      "thought": {
        "type": "string",
        "description": "A thought to think about."
      }
    },
    "required": ["thought"]
  }
}
```

### 性能数据（τ-Bench）

| [[Configuration|配置]] | 航空域 pass^1 | 零售域 pass^1 |
|------|-------------|-------------|
| 基线（无 think，无[[扩展思维|扩展思考]]） | 0.370 | 0.783 |
| 仅[[扩展思维|扩展思考]] | 0.412 | 0.770 |
| 仅 [[Think 工具]] | 0.404 | **0.812** |
| [[Think 工具]] + 优化提示 | **0.570** | — |

航空领域：Think + 优化提示 **54% 相对提升**（0.370→0.570）。优化提示需提供领域特定的推理示例。

### 最佳使用场景

[[Think 工具]]最有价值的三种情境：
1. **工具输出分析**：需要仔细处理前序工具调用的结果再行动，可能需要回溯方法
2. **策略密集型环境**：需要遵循复杂政策并验证合规
3. **顺序决策**：每步基于前步构建，错误代价高

**不适合场景**：非顺序工具调用（单次或多并行调用）、简单指令遵循。

### 提示工程实践

仅提供 [[Think 工具]]而不加额外提示，可获得基线改善；但**配合优化提示效果更显著**——尤其是复杂域。

有效的系统提示应包含：
- 何时以及如何使用 [[Think 工具]]的说明
- 域特定推理示例（如：检查取消规则的步骤清单，[[计算]]行李费的方法）

建议：将复杂的 [[Think 工具]]指导放在**系统提示**中，而非工具描述中，提供更广泛的上下文。

### SWE-bench 中的应用

[[Think 工具]]的适应版本在 [[SWE-bench]] 评估中使用，描述调整为"用于头脑风暴修复方案和分析测试结果"，n=30 样本与基线比较，孤立效果：**平均提升 1.6%**（p < 0.001，d = 1.47，统计显著）。

**注意**：随 [[扩展思维|Extended Thinking]] 能力改进，[[Anthropic]] 建议在大多数情况下优先使用[[扩展思维|扩展思考]]，保留 [[Think 工具]]用于需要处理工具输出的复杂场景。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/The _think_ tool_ Enabling Claude to stop and think.md]]

## 相关

- [[Agent工作流模式]] — part_of（Think 工具是增强 Agent 决策质量的组件）
- [[Agent Harness模式]] — related_to（Think 工具是 Harness 中可选的推理增强模块）
- [[Agent评估方法论]] — related_to（τ-Bench 是验证 Think 工具效果的基准）
