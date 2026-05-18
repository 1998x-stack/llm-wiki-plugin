---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [ai-engineering, evaluation, 质量保障, AI工程]
aliases: ["Transcript vs Outcome", "结果验证", "Outcome 验证"]
relates_to:
  - target: "[[Agent 评测体系]]"
    type: part_of
  - target: "[[评分器设计]]"
    type: uses
supersedes: null
---

# Transcript vs Outcome

## 概述
Transcript vs Outcome 是 [[评测驱动开发|Agent 评测]]中的核心[[区分]]概念，强调好的评测应验证环境的实际最终状态（Outcome），而非 Agent 的自我报告（Transcript 声明）。

## 关键内容

1. **Transcript（记录/轨迹）**：
   - Agent 在 Trial 中的完整行为记录，包含所有工具调用和对话
   - 代表 Agent"做了什么"和"说了什么"
   - **局限**：Agent 可能声称完成任务但实际没有

2. **Outcome（结果）**：
   - Trial 结束时环境的实际最终状态
   - 代表"实际发生了什么"
   - **优势**：客观事实，不依赖 Agent 自我报告

3. **典型案例**：
   - 航班预订 Agent 说"您的航班已预订"（Transcript 声明）
   - 评测者检查 SQL 数据库中是否存在预订记录（Outcome 验证）
   - 前者是 Agent 自我报告，后者是客观事实

4. **设计原则**：
   - **好的评测验证 Outcome，不相信 Transcript 声明**
   - 避免检查 Agent 是否按特定步骤执行（路径评测）
   - **评测产出，不是路径**：Agent 经常找到评测设计者没有预期的有效方法
   - [[Opus 4.5]] 案例：发现评测策略漏洞并利用，技术上"失败"但实际找到更优解

5. **工程实践**：
   - 结果验证[[评分器设计|评分器]]：检查 DB 状态、文件系统、API 响应等
   - 需要可访问的持久化状态
   - 最接近真实用户体验的评测方式

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/12_demystifying_evals.md]] — 核心概念体系章节

## 相关
- [[Agent 评测体系]] — part_of（Transcript vs Outcome 是评测体系的核心概念）
- [[评分器设计]] — uses（结果验证是评分器设计的重要方法）
- [[评测驱动开发]] — uses（Outcome 验证是评测设计的核心原则）
