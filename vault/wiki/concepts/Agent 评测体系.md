---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["ai-engineering", "evaluation", "agent", "质量保障"]
aliases: ["Agent Evaluation System", "Agent 评测体系", "Agent 评测框架"]
relates_to:
  - target: "[[评测驱动开发]]"
    type: implements
  - target: "[[SWE-bench]]"
    type: uses
  - target: "[[τ-Bench]]"
    type: uses
supersedes: null
---

# Agent 评测体系

## 概述
Agent 评测体系是 AI Agent 质量保障的完整方法论，涵盖 Task/Trial/Grader/Transcript/Outcome 的术语定义、三类评分器选择策略、以及四类 Agent（编码、对话、研究、计算机使用）的具体评测方案。

## 关键内容

1. **核心术语体系**：
   - **Task（任务）**：有定义输入和成功标准的测试
   - **Trial（试验）**：一次 Task 尝试（因 Agent 随机性需多次试验）
   - **Transcript/Trace（记录/轨迹）**：Trial 的完整记录，包含所有工具调用
   - **Outcome（结果）**：Trial 结束时环境的实际最终状态（客观事实，非 Agent 自我报告）
   - **Grader（评分器）**：对 Transcript 或 Outcome 进行打分的逻辑
   - **Evaluation Suite（评测套件）**：多个 Task 的集合
   - **Evaluation Harness（评测框架）**：运行评测的基础设施
   - **Agent Harness（Agent 框架）**：让模型作为 Agent 行动的系统

2. **Transcript vs Outcome 的关键区分**：
   - 航班预订 Agent 说"您的航班已预订"（Transcript 声明）
   - 评测者检查 SQL 数据库中是否存在预订记录（Outcome 验证）
   - **好的评测验证 Outcome，不相信 Transcript 声明**

3. **评测悖论**：
   - Agent 的自主性、智能性、灵活性使其有用，但也使其难以评测
   - 无法预知执行路径、可能"绕过"评测假设、评测无法覆盖所有路径
   - Opus 4.5 案例：发现评测策略漏洞并利用，技术上"失败"但实际找到更优解

4. **没有 eval 的代价**：
   - 用户报告 Agent 变差，团队无法量化
   - 调试完全被动：等待投诉 → 手动复现 → 修复 Bug → 希望没有新回退
   - 无法区分真实回退与噪声
   - 新模型发布时需数周测试，而有 eval 的竞争对手只需数天

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/12_demystifying_evals.md]] — 完整评测体系定义

## 相关
- [[评测驱动开发]] — implements（评测体系是评测驱动开发的基础）
- [[SWE-bench]] — uses（编码 Agent 评测的标准基准）
- [[τ-Bench]] — uses（对话 Agent 评测的标准基准）
- [[Terminal-Bench]] — uses（通用终端任务评测基准）
- [[WebArena]] — uses（计算机使用 Agent 评测基准）
- [[OSWorld]] — uses（操作系统交互评测基准）
- [[LLM-as-Judge]] — part_of（三类评分器之一）
- [[pass@k vs pass^k]] — part_of（非确定性处理的核心统计方法）
