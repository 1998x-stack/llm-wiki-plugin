---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["superpowers", "multi-agent", "execution", "workflow", "Agent系统"]
aliases: ["subagent-driven-development", "Subagent-Driven Development Skill"]
relates_to:
  - target: "[[Superpowers]]"
    type: part_of
  - target: "[[Multi-Agent Orchestration]]"
    type: implements
---

# subagent-driven-development Skill

## 概述
[[Superpowers]] 技能，通过为每个任务派遣全新子 Agent 实现计划，配合两阶段评审（规格合规性 → 代码质量），是 [[Superpowers]] 在有子 Agent 支持平台的首选执行引擎。

## 关键内容

1. **核心公式**：
   > Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration

2. **为什么不让主 Agent 直接做**：
   - [[上下文窗口]]污染（需求讨论占用空间）
   - 污染推理路径（被否定的方案干扰）
   - 降低执行精度（协调与执行认知模式冲突）

3. **子 Agent 状态协议**：
   | 状态 | 含义 | 处理 |
   |------|------|------|
   | `DONE` | 任务完成，测试通过 | 进入 Phase A 评审 |
   | `DONE_WITH_CONCERNS` | 完成但有问题 | 评估后处理 |
   | `NEEDS_CONTEXT` | 缺少信息 | 提供信息后重派 |
   | `BLOCKED` | 无法解决的阻碍 | 升级模型/拆分/人工 |

4. **两阶段评审**：
   - **Phase A：规格合规性评审**（Spec Compliance Review）
     - 确认做了正确的事
     - 评审员角色：怀疑论者
   - **Phase B：代码质量评审**（Code Quality Review）
     - 确认做得对不对
     - 代码组织、命名规范、可维护性

5. **平台要求**：
   - ✅ [[Claude Code]]
   - ✅ [[Codex CLI|Codex]]（需 `multi_agent = true`）
   - ❌ [[Gemini CLI]]（无子 Agent，用 executing-plans）

## 来源
- [[05-subagent-driven-development]] — subagent-driven-development Skill 解析

## 相关
- [[Superpowers]] — part_of
- [[Multi-Agent Orchestration]] — implements
- [[writing-plans Skill]] — precedes
