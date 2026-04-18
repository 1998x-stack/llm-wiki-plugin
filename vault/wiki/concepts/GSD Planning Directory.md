---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [gsd, context-engineering, file-system, project-management]
aliases: [".planning/", "GSD Planning Directory", "规划目录"]
relates_to:
  - target: "[[GSD]]"
    type: part_of
  - target: "[[Context Engineering]]"
    type: implements
---

# GSD Planning Directory

## 概述
GSD 系统的结构化项目记忆目录（`.planning/`），通过外部化项目记忆、[[渐进式披露（Progressive Disclosure）|按需加载]]不同文件子集，解决 LLM [[上下文窗口]]限制和跨会话失忆问题。

## 关键内容

1. **核心文件**：
   - **PROJECT.md**：项目愿景锚点（2-3 页，每次调用都加载）
   - **REQUIREMENTS.md**：版本化需求边界（v1/v2/out-of-scope）
   - **ROADMAP.md**：阶段路线图 + 状态追踪
   - **STATE.md**：跨会话工程记忆
   - **CONTEXT.md**：单阶段实现偏好（discuss-phase 生成）
   - **RESEARCH.md**：阶段专属领域研究（plan-phase 生成）
   - **[[XML Plan|PLAN.md]]**：原子执行计划（XML 格式）
   - **SUMMARY.md**：执行存档
   - **VALIDATION.md**：Nyquist 验证层（需求-测试映射）

2. **特殊目录**：
   - **research/**：项目级领域研究
   - **seeds/**：前瞻性想法（带触发条件）
   - **threads/**：跨会话轻量知识存储
   - **todos/**：待处理/已完成任务
   - **debug/**：活跃调试会话
   - **codebase/**：棕地代码库分析
   - **phases/**：各阶段独立目录

3. **文件加载策略**：
   | 命令 | PROJECT | REQUIREMENTS | ROADMAP | STATE | CONTEXT | RESEARCH | PLAN |
   |------|---------|-------------|---------|-------|---------|----------|------|
   | new-project | - | 生成 | 生成 | 生成 | - | - | - |
   | discuss-phase | ✅ | ✅ | ✅ | ✅ | 生成 | - | - |
   | plan-phase | ✅ | ✅ | - | - | ✅ | 生成 | 生成 |
   | execute-phase | ✅ | - | - | - | - | - | ✅ |

4. **设计哲学**：
   - 外部化项目记忆
   - 结构化信息流
   - 按需注入上下文

## 来源
- [[02-context-file-system]] — 上下文文件系统

## 相关
- [[GSD]] — part_of
- [[Context Engineering]] — implements
- [[Context Rot]] — caused
