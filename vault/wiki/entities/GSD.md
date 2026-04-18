---
type: project
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["claude-code", "workflow", "productivity", "open-source", "Agent系统"]
aliases: ["GSD", "get-shit-done", "Get Shit Done"]
relates_to:
  - target: "[[Context Rot]]"
    type: caused
  - target: "[[Claude Code]]"
    type: uses
---

# GSD

## 概述
为 [[Claude Code]] 设计的轻量级元提示、[[Context Engineering|上下文工程]]与规格驱动开发系统，由 TÂCHES 开发，GitHub Stars 40k+，被 [[Amazon]]/[[Google]]/Shopify 工程师使用。

## 关键内容

1. **核心洞见**：
   > "The complexity is in the system, not in your workflow."
   > 复杂度应该在系统里，不应该在工作流里。

2. **五大技术支柱**：
   - **[[Context Engineering|上下文工程]]**：每个命令只加载真正需要的文件
   - **XML 结构化 Prompt**：结构化任务定义（<task>、<action>、<verify>）
   - **[[Multi-Agent Orchestration|多智能体编排]]**：主会话轻量协调，[[Subagents-in-Claude-Code|子智能体]]深度专注
   - **原子 Git 提交**：每个任务完成后立即独立提交
   - **[[Wave Execution|波次并行执行]]**：DAG 依赖分析，可并行计划同时执行

3. **核心命令**：
   - `/gsd:new-project`：项目初始化
   - `/gsd:discuss-phase`：实现偏好捕获
   - `/gsd:plan-phase`：4 个并行研究智能体 + 计划验证
   - `/gsd:execute-phase`：DAG 依赖分析 + [[Wave Execution|波次并行执行]]
   - `/gsd:verify-work`：UAT 逐项引导

4. **解决的问题**：
   - ✅ [[Context Rot|上下文腐败]]
   - ✅ 风格漂移
   - ✅ 幻觉任务
   - ✅ 跨会话失忆
   - ✅ 执行缺乏验证

5. **不解决的问题**：
   - ❌ 坏需求
   - ❌ 领域知识缺失
   - ❌ 外部集成的本质复杂度
   - ❌ 团队协作工作流

## 来源
- [[01-overview-context-rot]] — Context Rot 与上下文工程
- GitHub: gsd-build/get-shit-done

## 相关
- [[Claude Code]] — uses
- [[Context Rot]] — caused
- [[Context Engineering]] — implements
- [[TÂCHES]] — created_by
