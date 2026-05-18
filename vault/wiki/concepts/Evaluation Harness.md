---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [ai-engineering, evaluation, 基础设施, 质量保障, Lua编程]
aliases: ["Evaluation Harness", "评测框架", "评测基础设施"]
relates_to:
  - target: "[[Agent 评测体系]]"
    type: part_of
  - target: "[[Harbor Framework]]"
    type: implements
supersedes: null
---

# Evaluation Harness

## 概述
Evaluation Harness 是运行 [[评测驱动开发|Agent 评测]]的基础设施，负责管理评测环境隔离性、Trial 执行、[[评分器设计|评分器]]调度和结果收集，是评测体系的工程基础。

## 关键内容

1. **核心职责**：
   - 运行 Evaluation Suite（多个 Task 的集合）
   - 管理 Trial 的执行环境（隔离性、干净状态）
   - 调度不同类型的[[评分器设计|评分器]]（代码、LLM、人工）
   - 收集和汇总评测结果

2. **关键设计原则**：
   - **每次 Trial 必须从干净的环境开始**（隔离性）
   - 避免共享状态（遗留文件、缓存数据）
   - 真实案例：[[Anthropic]] 内部评测中发现 [[Claude_Code|Claude]] 通过检查之前 Trial 的 git 历史获得了不公平优势
   - 支持 [[pass@k vs pass^k|pass@k]] 和 [[pass@k vs pass^k|pass^k]] 两种统计模式

3. **与 [[Agent Harness模式|Agent Harness]] 的区别**：
   - **Evaluation Harness**：运行评测的基础设施（评测侧）
   - **[[Agent Harness模式|Agent Harness]]**：让模型作为 Agent 行动的系统（执行侧）
   - 两者配合完成完整的评测流程

4. **开源实现**：
   - [[Harbor Framework]]：容器化的 [[Agent 评测体系|Agent 评测框架]]
   - 提供隔离环境、模块化组件、标准化接口

5. **工程最佳实践**：
   - 专门的 eval 团队负责核心基础设施
   - 领域专家和产品团队贡献具体任务
   - 支持持续集成和自动化运行

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/12_demystifying_evals.md]] — 核心概念体系章节

## 相关
- [[Agent 评测体系]] — part_of（Evaluation Harness 是评测体系的工程基础）
- [[Harbor Framework]] — implements（容器化的开源实现）
- [[评测驱动开发]] — uses（评测基础设施是评测驱动开发的工程保障）
