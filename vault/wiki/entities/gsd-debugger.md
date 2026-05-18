---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [gsd-agent, debugging, problem-solving, Agent系统]
aliases: ["gsd-debugger", "GSD Debugger", "GSD调试智能体"]
relates_to: 
  - target: "[[GSD Framework]]"
    type: part_of
    confidence: 0.9
  - target: "[[GSD 多智能体编排架构]]"
    type: implements
    confidence: 0.9
  - target: "[[gsd-verifier]]"
    type: responds_to
    confidence: 0.8
  - target: "[[GSD核心工作流]]"
    type: part_of_workflow
    confidence: 0.8
supersedes: null
---

# gsd-debugger

## 概述
GSD框架中的调试智能体，负责在verify-work阶段用户报告验收失败时进行问题分析和根因定位，并生成具体的修复计划。

## 关键内容

1. **触发条件**：
   - verify-work阶段中用户报告某项验收失败
   - 执行验证或功能测试发现问题
   - 代码与预期行为不一致的情况

2. **分析流程**：
   - 复现分析：根据用户描述和代码推断失败路径
   - 根因定位：找出最可能的失败原因，而非简单的"代码有bug"
   - 修复规划：生成具体的XML格式修复计划，可直接被execute-phase执行

3. **输入输出**：
   - 输入：用户描述的失败现象、相关源代码文件、对应的[[XML Plan|PLAN.md]]（原始意图）、git diff（实际实现与原始意图的偏差）
   - 输出：结构化的修复计划PLAN文件

4. **问题解决能力**：
   - 提供精确的根因分析
   - 生成可执行的修复方案
   - 维护开发流程的连续性

## 来源
- [[raw/articles/ai-tools/claude-skills/04-multi-agent-orchestration.md]] — GSD多智能体编排架构详解

## 相关
- [[GSD Framework]] — 整体框架
- [[GSD 多智能体编排架构]] — 所属编排系统
- [[gsd-verifier]] — 响应验证失败
- [[GSD核心工作流]] — 所属工作流程