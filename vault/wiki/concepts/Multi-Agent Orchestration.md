---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["gsd", "multi-agent", "orchestration", "architecture", "Agent系统"]
aliases: ["Multi-Agent Orchestration", "多智能体编排", "GSD Orchestration"]
relates_to:
  - target: "[[GSD]]"
    type: part_of
  - target: "[[GSD Commands]]"
    type: implements
  - target: "[[GSD 多智能体编排架构]]"
    type: has_variant
    confidence: 0.8
---

# Multi-Agent Orchestration

## 概述
GSD 系统的核心架构模式，通过编排者（主会话）协调 11 个专家[[Subagents-in-Claude-Code|子智能体]]，每个[[Subagents-in-Claude-Code|子智能体]]有明确职责边界，接收精确裁剪的上下文，产出结构化输出，通过文件系统通信。

## 关键内容

1. **为什么需要多智能体**：
   - **[[Context Window Pollution|上下文污染]]累积**：单智能体上下文会被各类信息填满
   - **角色冲突**：规划者和执行者需要不同思维模式
   - **串行瓶颈**：研究+规划+执行在单上下文中需数小时

2. **11 个专家[[Subagents-in-Claude-Code|子智能体]]**：

   | 智能体 | 职责 | 并发度 |
   |--------|------|--------|
   | `gsd-planner` | 生成 [[XML 结构化 Prompt|XML 结构化计划]] | 串行 |
   | `gsd-roadmapper` | 需求分解为路线图 | 串行 |
   | `gsd-executor` | 执行 [[XML Plan|PLAN.md]] 任务 | **并行** |
   | `gsd-phase-researcher` | 阶段领域研究（4 维） | **×4 并行** |
   | `gsd-project-researcher` | 项目级领域研究 | **×4 并行** |
   | `gsd-research-synthesizer` | 合并研究报告 | 串行 |
   | `gsd-debugger` | 诊断失败根因 | 按需 |
   | `gsd-codebase-mapper` | 代码库分析（4 维） | **×4 并行** |
   | `gsd-verifier` | 验证阶段目标达成 | 串行 |
   | `gsd-plan-checker` | 8 维计划质量验证 | 串行 |
   | `gsd-integration-checker` | 跨模块集成检查 | 串行 |

3. **编排者设计原则**：
   - **编排者永远不做重型任务**
   - ✅ 读取状态、构建上下文、spawn [[Subagents-in-Claude-Code|子智能体]]、收集结果、路由决策
   - ❌ 自己研究、自己生成代码、自己分析大量代码

4. **波次并行调度**：
   - 解析计划依赖关系 → 拓扑排序构建波次
   - 同波次计划并行执行
   - 等待波次完成后才开始下一波次

5. **上下文构建策略**：
   - `gsd-executor`：只接收 PROJECT.md + 当前 [[XML Plan|PLAN.md]]
   - `gsd-planner`：接收 PROJECT + REQUIREMENTS + CONTEXT + 4 份研究

6. **模型分配策略**：
   - `gsd-planner`：Opus（关键架构决策）
   - `gsd-codebase-mapper`：Haiku（信息提取任务）
   - `gsd-phase-researcher`：budget 模式可用 Haiku

## 来源
- [[04-multi-agent-orchestration]] — 多智能体编排架构

## 相关
- [[GSD]] — part_of
- [[GSD Commands]] — implements
- [[GSD 多智能体编排架构]] — variant_of
- [[Wave Execution]] — uses
- [[Context Engineering]] — implements
