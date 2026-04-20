---
type: concept
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 3
tags: ["agent-pattern", "context-management", "orchestration", "Agent系统"]
aliases: ["Sub-Agent Pattern", "子 Agent 模式", "Agent 卸载", "上下文保护模式"]
relates_to:
  - target: "[[Ralph Loop]]"
    type: used_by
  - target: "[[上下文窗口]]"
    type: relates_to
  - target: "[[Orchestrator-Subagent-Pattern]]"
    type: compares_to
  - target: "[[脑手分离架构]]"
    type: compares_to
supersedes: null
---

# 子 Agent 模式（Sub-Agent Pattern）

## 概述
子 Agent 模式是一种上下文保护策略，将昂贵的操作（测试、编译、截图）offload 给独立的子 Agent 执行，主 Agent 仅接收结论而不被执行细节污染，从而保持主上下文的精简和决策能力。

## 关键内容

1. **核心架构**：
   ```
   主 Agent 上下文 (调度器):
     "请运行测试并告诉我 auth-001 是否通过"
         ↓ spawn subagent
     子 Agent 上下文 (执行器):
       运行 npm test -- auth.test.js
       截图 → 分析结果 → 返回: "PASS / FAIL"
         ↑ 只返回结论，不污染主上下文
     主 Agent: 收到结论 → 更新 prd.json → 提交
   ```

2. **主 Agent 的职责**：只做决策，不做重型执行。保持上下文精简，避免被测试输出、编译日志、截图分析等大量中间结果污染。

3. **子 Agent 的职责**：执行具体的重型操作，包括运行测试套件、编译构建、截图分析、文件转换等。子 Agent 拥有独立的[[上下文窗口]]，其内部的 token 消耗不会影响主 Agent。

4. **与 [[上下文窗口]] 的关系**：子 Agent 模式是保护主[[上下文窗口]]不被污染的关键手段。重型操作的输出通常包含大量 token（测试日志、编译错误、终端输出），如果直接在主 Agent 中执行，会快速消耗[[上下文预算管理|上下文预算]]。

5. **与 [[Orchestrator-Subagent-Pattern]] 的对比**：
   - Orchestrator-Subagent 是通用的任务分发模式，子 Agent 可能承担完整的子任务
   - 子 Agent 模式更聚焦于"上下文保护"——子 Agent 是执行器，返回精简结论

6. **与 [[脑手分离架构]] 的对比**：
   - [[脑手分离架构]]将"大脑"（决策）和"手"（执行）完全解耦为独立服务
   - 子 Agent 模式是[[脑手分离架构|脑手分离]]的轻量实现——在同一系统内通过 spawn 实现分离

7. **在 [[Ralph Loop]] 中的应用**：主 Agent 负责选择 Story、编写代码、更新状态文件，而将测试验证、浏览器自动化等重型操作委托给子 Agent。主上下文永远保持精简，只做决策。

## 来源
- [[raw/articles/ai-tools/ralph-loop/how-the-loop-works.md]] — Ralph Loop 核心原理深度解析
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/04_context_engineering.md]] — Anthropic 子 Agent 架构上下文流模式分析
- [[08_claude_code_best_practices.md]] — Anthropic 官方 Claude Code 最佳实践指南（子 Agent 用于调查的经验法则）

## 相关
- [[Ralph Loop]] — used_by（Ralph Loop 中用于保护主上下文）
- [[上下文窗口]] — relates_to（保护主上下文窗口不被重型操作污染）
- [[Orchestrator-Subagent-Pattern]] — compares_to（更通用的任务分发模式）
- [[脑手分离架构]] — compares_to（完全解耦的决策-执行分离架构）
