---
type: concept
status: active
confidence: 0.5
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [技术, 方法论, AI工程]
aliases: [Spec-Driven Development, SDD, 规格驱动开发]
relates_to:
  - Harness Engineering
  - Agent Skills
  - PRD 驱动开发
  - 结构化编程
supersedes: null
---

# SDD规格驱动开发

## 概述
SDD（Spec-Driven Development，规格驱动开发）是 AI 时代软件工程的范式跃迁，从"先写代码再补文档"转变为"先定义规格，让代码去满足规格"。规格是唯一可执行的真理来源，用结构化语言编写，可被机器读取和验证。

## 关键内容
1. **核心理念**：规格即蓝图，契约即真理。规格不是静态 Word 文档，而是结构化、可执行、可验证的定义
2. **完整流程**：
   - Specify（定义规格）：明确功能需求、非功能需求、接口规范、验收标准
   - Plan（技术规划）：将规格翻译成技术架构、技术栈、实现路径
   - Task（任务拆解）：将规划拆解为原子化开发任务，生成 todo list
   - Implement（实现）：AI 根据规格和任务自动生成代码，人类只做终审
3. **与 AI 编码的结合**：通过 Skill（如 planning with FILES）将 SDD 流程固化为 AI 可执行的 SOP
4. **解决的核心问题**：直接让 AI 写代码往往不符合预期，精确的规格是 AI 高效产出的前提
5. **与 Harness Engineering 的关系**：SDD 提供"定义任务和意图"的方法论，是 Harness 三件核心工作之一

## 来源
- [[raw/articles/essays/thinking-series/008-算法面试]] — 全文

## 相关
- [[Harness Engineering]] — extends（SDD 是 Harness 的核心组成部分）
- [[Agent Skills]] — uses（通过 Skill 固化 SDD 流程）
- [[PRD 驱动开发]] — compares_to
- [[结构化编程]] — relates_to
