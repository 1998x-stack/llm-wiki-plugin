---
type: concept
title: Clean State Protocol
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["context-management", "agent-pattern", "ralph-loop", "quality-gate", "Agent系统"]
aliases: ["Clean State Protocol", "干净状态协议", "迭代结束检查清单"]
relates_to:
  - target: "[[上下文策略]]"
    type: part_of
    confidence: 0.9
  - target: "[[Ralph Loop]]"
    type: implemented_by
    confidence: 0.85
  - target: "[[Session 交接机制]]"
    type: enables
    confidence: 0.85
  - target: "[[Dumb Zone]]"
    type: relates_to
    confidence: 0.8
supersedes: null
---

# Clean State Protocol（干净状态协议）

## 概述
Clean State Protocol 是[[上下文策略]]之一，要求每次 Agent 迭代结束前执行完整的状态验证检查清单（git 状态、构建、测试、prd.json 语法、progress.txt 更新），确保不把破损状态传递给下一个 Agent 实例。

## 关键内容

1. **五项验证检查清单**：
   - **Git 状态检查**：`git status --short` → 期望空输出（所有变更已提交）
   - **构建检查**：`npm run build` → 期望无错误
   - **测试检查**：`npm test -- --passWithNoTests` → 期望所有测试通过
   - **prd.json 语法检查**：`python3 -c "import json; json.load(open('prd.json')); print('OK')"` → 期望 OK
   - **progress.txt 更新检查**：`tail -10 progress.txt` → 期望包含当前 session 的记录

2. **核心原则**：若检查失败，在提交前修复，不要把破损状态传递给下一个 Agent。这保证了每个新 Agent 实例启动时面对的是一个干净、可运行的代码库。

3. **与 [[Session 交接机制]] 的关系**：Clean State Protocol 是 [[Session 交接机制]]的[[质量保障]]层。三文件（prd.json、progress.txt、[[项目约定手册|AGENTS.md]]）的交接只有在代码库处于干净状态时才有意义。

4. **与 [[Dumb Zone]] 的关系**：Clean State Protocol 通常在迭代即将结束、上下文接近 [[Dumb Zone]] 之前执行。它确保 Agent 在主动退出前留下一个可继续工作的状态，而非半完成的混乱状态。

5. **与 [[验证-before-完成]] 的关系**：Clean State Protocol 是 verification-before-completion 原则在 Agent 迭代场景的具体实现——在声明迭代完成之前，必须先验证所有质量指标。

## 来源
- [[raw/articles/ai-tools/ralph-loop/context-strategies.md]] — Context Strategies 文档中的策略六

## 相关
- [[上下文策略]] — part_of（Clean State Protocol 是六大上下文策略之一）
- [[Ralph Loop]] — implemented_by（Ralph Loop 在每次迭代结束时执行此协议）
- [[Session 交接机制]] — enables（干净状态是有效交接的前提）
- [[Dumb Zone]] — relates_to（在 Dumb Zone 之前执行检查并退出）
- [[AGENTS.md 项目约定文件]] — relates_to（检查清单中的已知问题记录到 AGENTS.md）
