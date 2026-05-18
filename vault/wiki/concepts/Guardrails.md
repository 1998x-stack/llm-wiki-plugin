---
type: concept
title: Guardrails
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 4
tags: [AI, 技术, 方法论, AI工程]
aliases:
- 护栏机制
- Guardrails
- Agent Guardrails
relates_to:
- target: '[[ACI 设计原则]]'
  type: implements
  confidence: 1.0
- target: '[[Agent计算机接口]]'
  type: part_of
  confidence: 0.9
- target: '[[Agent循环]]'
  type: uses
  confidence: 0.85
supersedes: null
---

# Guardrails

## 概述

Guardrails（护栏机制）是 Agent 系统中的错误 containment 策略，用于在错误刚出现时将其截断，防止[[错误复合|错误传播]]污染整条轨迹。它是 [[ACI 设计原则]] 的第四条核心原则。

## 关键内容

### 核心问题

> "Agent 最大的问题之一不是犯错，而是犯错后继续在错的状态上推进。"

Guardrails 的作用是把错误显式化、局部化、可恢复化。

### 实现方式

| 类型 | 示例 | 作用 |
|------|------|------|
| **语法检查** | Linting（代码语法验证） | 编辑后即时检测语法错误 |
| **格式验证** | 命令格式合法性检查 | 防止非法命令执行 |
| **编辑恢复** | 无效编辑丢弃 + 错误反馈 | 让 agent 重新尝试 |
| **状态保护** | 错误命令不改变环境状态 | 防止错误操作污染环境 |

### Linting 作为 Guardrail

Linting 是一种典型的**局部验证器**：
- 不负责判断问题是否最终修好
- 但能快速判断"这次编辑是不是把代码直接写坏了"
- 本质是在 [[Agent循环]] 里插入一个 cheap critic
- 论文证据：带 linting 的编辑[[Settings|设置]]效果优于不带 linting

### 与人类开发流程的类比

如果说 ACI 是 agent 的"工作台"，那么 guardrails 就是"工作台上的护栏"。它不是为了让 agent 更聪明，而是为了让 agent 没那么容易把自己搞崩——这在长轨迹任务里尤为重要。

### 扩展方向

Linting 只是 guardrail 的一种。后续可扩展为：
- [[单元测试]]（功能正确性验证）
- 类型检查（类型安全验证）
- 静态分析（代码质量验证）
- LSP 增量诊断（语义级错误检测）
- 这些都可视为 cheap critic 的扩展形式

### LSP 增量诊断作为 Guardrail

[[SWE-agent]] 的 linter 实现（`flake8 --select=F821,F822,F831,E111,E112,E113,E999,E902`）是单文件、快速、偏语法与低级静态错误的校验。若要进一步增强，可引入 LSP 增量诊断：

**三层 Validate 架构：**
1. **Edit 后单文件增量**（0.2–2 秒）：parser/syntax/单文件 LSP diagnostics，只返回新引入问题
2. **Changed-files 级检查**（2–10 秒）：当 edit 涉及 public API/types/build files 时，跑 typecheck / LSP workspace slice
3. **提交前全量**（10–30 秒）：最小测试集 + changed-files lint/typecheck + repo smoke test

**增量诊断关键设计：**
- `previous errors filtering`：更新旧错误行号，过滤编辑窗口外的旧问题，只保留本次 edit 新引入的错误
- Observation 压缩：不直接返回 LSP 原始 JSON，而是压成 `file/range/severity/message/是否新引入/是否阻断提交` 的 agent-friendly 格式
- 触发策略：`on_edit(file)` → 单文件增量；`on_cross_file_signal` → 依赖图扩展；`on_submit` → changed-files workspace diagnostics

### 六层 Guardrail 体系

基于 [[SWE-agent]] 思想，完整的 guardrail 体系可分为 6 层：

| 层级 | 名称 | 保护对象 | 论文状态 |
|------|------|---------|---------|
| **1** | Protocol Guardrails | 交互协议（thought/action 格式、参数校验、非法输出重试） | 已实现 |
| **2** | Action Guardrails | 单个动作不推环境入不可解释状态（edit 只允许改打开文件、search 限制返回量） | 大部分实现 |
| **3** | State Guardrails | 始终能解释"现在是什么状态"（当前文件/窗口/目录显式回显） | 大部分实现 |
| **4** | Semantic Guardrails | 代码没有写坏（syntax/lint） | 已实现 |
| **5** | 扩展语义护栏 | type checker、build validation、unit-test subset rerun | 未来方向 |
| **6** | 隐式护栏 | 小动作空间、100-line viewer、summarized search | 已实现 |

### 隐式 Guardrails

论文虽未直接命名为 guardrail，但以下设计都在发挥护栏作用：
- **小动作空间**：通过 interface restriction 降低错误率
- **100-line viewer**：限制模型看到的窗口，Full file 反而更差
- **Summarized search**：限制 agent 不要在 next/prev 结果里机械穷举

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/03-SWE-agent 论文的所有核心概念 展开详细分析 一个一个.md]] — SWE-agent 核心概念分析
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/04-SWE agent 如何保证 搜索是否高效、编辑是否稳定、反馈是否足够、上下文是否可控、恢复机制是否.md]] — SWE-agent 五大保障机制分析
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/05-SWE agent 有哪些图表，每个图表核心内容和核心观点是什么？.md]] — SWE-agent 论文图表分析
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/10-swe-agent 每次 edit后，如何设计lintlsp 等validate？.md]] — Edit 后 validate 设计详解

## 相关

- [[ACI 设计原则]] — implements（Guardrails 是第四条设计原则的具体实现）
- [[Agent计算机接口]] — part_of（Guardrails 是 ACI 的组成部分）
- [[Agent循环]] — uses（Guardrails 在 Agent 循环中发挥作用）
- [[恢复机制]] — uses（恢复机制依赖护栏机制拦截错误）
- [[环境反馈设计]] — related_to（反馈设计本身就是一种护栏）
- [[Edit 后验证]] — caused（Guardrails 催生了具体的 edit 后验证实现）
