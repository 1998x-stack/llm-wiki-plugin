---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [LLM, 任务规划, 视觉任务, 反思学习, AI工程]
aliases: ["AssistGPT: A General Multi-modal Assistant that can Plan, Execute, Inspect, and Learn"]
relates_to: []
supersedes: null
---

# AssistGPT

## 概述
AssistGPT是由Gao等人提出的通用多模态助手，能够规划、执行、检查和学习。其PEIL框架强调了检查环节的重要性，允许模型在中间步骤发现问题时主动重新规划。

## 关键内容

1. **PEIL四步循环框架**：
   - Plan（规划）：制定任务计划
   - [[Execute]]（执行）：执行规划的步骤
   - Inspect（检查）：检查中间结果是否符合预期
   - Learn（学习）：记录成功和失败的策略作为未来规划的示例

2. **核心创新**：
   - Inspect阶段的主动检查机制：若中间结果不符合预期，则主动重新规划
   - Learn阶段的记忆机制：记录规划策略作为few-shot示例

3. **与其它方法的区别**：
   - 相比传统的线性执行流程，增加了主动检查和反思环节
   - 强调中间[[Transcript vs Outcome|结果验证]]而非等到最终失败才发现问题

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Paper]] — "AssistGPT: A General Multi-modal Assistant that can Plan, Execute, Inspect, and Learn", 2023

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Task-Planning]] — relates_to
- [[Self-Inspection]] — relates_to
- [[Multi-Modal-Assistant]] — relates_to