---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["batch-processing", "trajectory", "rl-training", "parallel-execution", "Agent系统"]
aliases: [Batch Runner, 批量运行器]
relates_to:
  - Atropos
  - 轨迹压缩
  - 自我进化代理
  - Hermes Agent
supersedes: null
---

# Batch Runner

## 概述
[[Hermes Agent|Hermes]] 的批量 Agent 执行工具，并行启动多个 Agent 实例收集同类型任务的完整轨迹，为 RL 训练生成大规模训练数据。

## 关键内容
- **核心功能**：并行启动 N 个 Agent 实例，每个实例独立执行同类型任务，记录完整轨迹（observation, action, reward）
- **在训练流程中的角色**：训练数据生成的第一步——定义任务类型和评估标准后，Batch Runner 负责大规模并行执行以收集训练数据
- **命令行使用**：`hermes batch run --task-file tasks/coding_tasks.jsonl --n-workers 8 --output-dir trajectories/ --model hermes-3.5`
- **关键参数**：`--task-file` 指定任务列表（[[JSONL格式|JSONL]] 格式）、`--n-workers` 控制并行 [[Worker Agent|Worker]] 数量、`--output-dir` 指定轨迹输出目录、`--model` 指定使用的模型版本
- **与[[轨迹压缩]]的衔接**：Batch Runner 输出的原始轨迹经 `hermes batch compress` 压缩后，再通过 `hermes batch export --format atropos` 导出为 [[Atropos]] RL 训练格式
- **研究价值**：是 [[Hermes Agent|Hermes]]"研究就绪"能力的核心组件，使 [[Nous Research]] 能够大规模收集工具调用训练数据，驱动下一代模型改进

## 来源
- [06_hermes_learning_loop.md](/raw/articles/ai-tools/hermes/06_hermes_learning_loop.md) — Hermes Agent 深度解析系列第六篇：闭环学习引擎

## 相关
- [[Atropos]] — extends
- [[轨迹压缩]] — extends
- [[自我进化代理]] — part_of
- [[Hermes Agent]] — implements
