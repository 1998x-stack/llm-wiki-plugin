---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [项目, Python, Web框架, 开源, 工具与框架]
aliases:
- Django
- Django 框架
relates_to:
- target: '[[SWE-bench]]'
  type: uses
  confidence: 0.85
supersedes: null
---

# Django

## 概述
Django 是一个高级 [[Python]] Web 框架，鼓励快速开发和干净、实用的设计，是 [[SWE-bench]] 评测中使用的真实开源[[仓库]]之一。

## 关键内容

1. **[[SWE-bench]] 中的角色**：Django 是 [[SWE-bench]] [[Evaluation Harness|评测框架]]中使用的真实开源[[仓库]]之一，代表大型 [[Python]] Web 项目的代码库复杂度。

2. **多文件修改挑战**：Django [[仓库]]中的 Issue 修复常需要修改多个相互关联的文件——主功能代码、测试文件、[[Configuration|配置]]文件、文档，是 long-horizon task 的典型场景。

3. **代码库特征**：作为成熟的 Web 框架，Django 具有复杂的路由系统、ORM、[[ROS (Robot Operating System)|中间件]]、模板引擎等模块，对 AI Agent 的跨文件理解能力提出高要求。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/07_swe_bench_sonnet.md]] — SWE-bench 使用的真实开源仓库示例

## 相关

- [[SWE-bench]] — uses（Django 是 SWE-bench 评测中使用的真实开源仓库之一）
