---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [项目, Python, Web框架, 开源, 微框架, 工具与框架]
aliases:
- Flask
- Flask 框架
relates_to:
- target: '[[SWE-bench]]'
  type: uses
  confidence: 0.85
supersedes: null
---

# Flask

## 概述
Flask 是一个轻量级 [[Python]] Web 框架（微框架），以简洁灵活著称，是 [[SWE-bench]] 评测中使用的真实开源[[仓库]]之一。

## 关键内容

1. **[[SWE-bench]] 中的角色**：Flask 是 [[SWE-bench]] [[Evaluation Harness|评测框架]]中使用的真实开源[[仓库]]之一，代表轻量级 [[Python]] Web 项目的代码库特征。

2. **与 [[Django]] 的对比**：相比 [[Django]] 的"全功能"设计，Flask 作为微框架代码库更精简，但同样需要 AI Agent 具备跨文件理解和多步骤修改能力。

3. **真实 Bug 场景**：[[SWE-bench]] 使用 Flask [[仓库]]中真实用户报告的 Bug 作为评测任务，测试套件自动验证修复是否正确。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/07_swe_bench_sonnet.md]] — SWE-bench 使用的真实开源仓库示例

## 相关

- [[SWE-bench]] — uses（Flask 是 SWE-bench 评测中使用的真实开源仓库之一）
