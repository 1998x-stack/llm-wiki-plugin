---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [项目, Python, 数学, 开源, 符号计算]
aliases:
- Sympy
- SymPy
relates_to:
- target: '[[SWE-bench]]'
  type: uses
  confidence: 0.85
supersedes: null
---

# Sympy

## 概述
Sympy 是一个 Python 符号计算库，用于计算机代数系统（CAS），是 SWE-bench 评测中使用的真实开源仓库之一。

## 关键内容

1. **SWE-bench 中的角色**：Sympy 是 SWE-bench 评测框架中使用的真实开源仓库之一，代表数学/科学计算类 Python 库的代码特征。

2. **代码库特征**：作为符号计算库，Sympy 涉及大量数学算法实现、表达式树处理、简化规则等，对 AI Agent 的数学推理和代码理解能力提出独特挑战。

3. **测试验证**：Sympy 拥有完善的测试套件，SWE-bench 利用这些测试自动验证 AI 生成的补丁是否正确，体现了"真实测试用于验证"的评测理念。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/07_swe_bench_sonnet.md]] — SWE-bench 使用的真实开源仓库示例

## 相关

- [[SWE-bench]] — uses（Sympy 是 SWE-bench 评测中使用的真实开源仓库之一）
