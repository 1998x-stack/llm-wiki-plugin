---
type: entity
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["rl", "training", "hermes", "nous-research", "强化学习"]
aliases: []
relates_to:
  - Hermes Agent
  - Nous Research
  - 轨迹压缩
  - Batch Runner
  - 自我进化代理
supersedes: null
---

# Atropos

## 概述
[[Nous Research]] 开发的[[强化学习]]训练环境，专为工具调用模型的 RLHF 训练设计，是 [[Hermes Agent|Hermes]] 研究就绪能力的核心组件。

## 关键内容
- **核心定位**：[[强化学习]]（RL）训练环境，支持工具调用模型的 RLHF（[[强化学习|Reinforcement Learning]] from Human Feedback）
- **在 [[Hermes Agent|Hermes]] 中的角色**：[[Hermes Agent|Hermes]] 既是用户产品，也是 [[Nous Research]] 的训练基础设施，Atropos 提供 RL 训练环境
- **训练流程**：批量运行 Agent 会话 → 导出 (observation, action, reward) 轨迹 → Atropos RL 环境训练工具调用模型 → 下一代 [[Hermes Agent|Hermes]] 更聪明
- **批量轨迹生成**：支持大规模并行运行 Agent 收集训练数据
- **[[轨迹压缩]]**：压缩冗余上下文，减少训练成本
- **训练数据生成流程**：定义任务类型和评估标准 → [[Batch Runner]] 批量并行运行 Agent 收集轨迹 → trajectory.py 压缩轨迹去除冗余保留关键决策节点 → Atropos RL 环境使用 PPO/GRPO 等[[算法]]训练 → 策略蒸馏回模型权重发布新版本
- **[[Batch Runner]]**：`hermes batch run --task-file tasks/coding_tasks.jsonl --n-workers 8 --output-dir trajectories/ --model hermes-3.5`，并行启动 N 个 Agent 实例独立执行同类型任务
- **[[轨迹压缩]]命令**：`hermes batch compress --input trajectories/ --output compressed_trajectories/ --max-tokens 4096`
- **导出为 Atropos 格式**：`hermes batch export --input compressed_trajectories/ --format atropos --output training_data.jsonl`
- **RL vs SFT**：SFT 学习已有正确示例（模仿），只能学习已有数据；RL 通过奖励信号试错学习，可发现 SFT 数据中没有的更优策略
- **多维度评估**：奖励[[计算]]基于正确性、效率、代码质量等多维度评分

## 来源
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — 2026 年 4 月版本
- [06_hermes_learning_loop.md](/raw/articles/ai-tools/hermes/06_hermes_learning_loop.md) — Hermes Agent 深度解析第六篇：闭环学习引擎，Atropos RL 训练流程、Batch Runner、轨迹压缩

## 相关
- [[Hermes Agent]] — part_of
- [[Nous Research]] — created
- [[闭环学习系统]] — extends
- [[轨迹压缩]] — uses
- [[Batch Runner]] — uses
- [[自我进化代理]] — extends
