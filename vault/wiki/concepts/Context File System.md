---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, project-management, context-management]
aliases: ["Context File System", "上下文文件系统", ".planning directory", "持久化大脑"]
relates_to:
  - target: "[[Context Window]]"
    type: extends
  - target: "[[GSD]]"
    type: implements
  - target: "[[External Memory]]"
    type: implements
supersedes: null
---

# Context File System

## 概述
一种结构化的、[[渐进式披露（Progressive Disclosure）|按需加载]]的、多文件的项目外部记忆系统，用于解决LLM缺乏持久化记忆的问题，通过[[GSD Planning Directory|.planning/]]目录实现AI项目的持久化大脑功能。

## 关键内容

1. **设计目的**：
   - 解决LLM没有持久化记忆的问题
   - 避免传统单文件方案的三大缺陷：无差别加载、无结构混乱、无版本化需求
   - 提供[[渐进式披露（Progressive Disclosure）|按需加载]]的结构化项目记忆系统

2. **核心文件结构**：
   - PROJECT.md：项目愿景锚点（每次调用都加载）
   - REQUIREMENTS.md：版本化需求边界（防过度实现）
   - ROADMAP.md：阶段路线图 + 状态追踪
   - STATE.md：跨会话工程记忆
   - CONTEXT.md：单阶段实现偏好
   - RESEARCH.md：阶段专属领域研究
   - [[XML Plan|PLAN.md]]：原子执行计划
   - VALIDATION.md：[[Nyquist Validation Layer|Nyquist验证层]]（测试合约）

3. **关键特性**：
   - 按需注入的上下文[[矩阵]]：不同命令加载不同的文件子集
   - 外部化项目记忆，结构化信息流
   - 支持棕地项目分析（codebase/目录）
   - 阶段化的执行流程：discuss → plan → execute → verify

## 来源
- [[raw/articles/ai-tools/claude-skills/02-context-file-system.md]] — 全文

## 相关
- [[Context Window]] — extends
- [[GSD]] — implements
- [[External Memory]] — implements