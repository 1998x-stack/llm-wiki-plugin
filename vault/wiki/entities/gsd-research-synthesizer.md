---
type: entity
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [gsd-agent, synthesis, consolidation]
aliases: ["gsd-research-synthesizer", "GSD Research Synthesizer", "GSD研究合成智能体"]
relates_to: 
  - target: "[[GSD Framework]]"
    type: part_of
    confidence: 0.9
  - target: "[[GSD 多智能体编排架构]]"
    type: implements
    confidence: 0.9
  - target: "[[gsd-phase-researcher]]"
    type: consolidates_output_from
    confidence: 0.9
  - target: "[[gsd-planner]]"
    type: provides_input_for
    confidence: 0.8
supersedes: null
---

# gsd-research-synthesizer

## 概述
GSD框架中的研究报告合成智能体，专门负责将多个[[gsd-phase-researcher]]生成的不同维度研究报告进行合并和整合，为后续的规划阶段提供统一的输入。

## 关键内容

1. **核心职责**：
   - 合并来自多个[[gsd-phase-researcher]]的多份研究报告
   - 将不同维度的研究结果（技术栈、功能、架构、陷阱）整合为统一视图
   - 消除不同研究报告之间的矛盾或重复信息
   - 生成结构化的综合研究结论

2. **执行位置**：
   - 在plan-phase阶段执行
   - 串行执行（非并行）
   - 在[[gsd-planner]]之前运行

3. **输入输出**：
   - 输入：多份来自不同[[gsd-phase-researcher]]的研究报告
   - 输出：统一的综合研究报告，供[[gsd-planner]]使用

## 来源
- [[raw/articles/ai-tools/claude-skills/04-multi-agent-orchestration.md]] — GSD多智能体编排架构详解

## 相关
- [[GSD Framework]] — 整体框架
- [[GSD 多智能体编排架构]] — 所属编排系统
- [[gsd-phase-researcher]] — 合并其输出
- [[gsd-planner]] — 为其提供输入