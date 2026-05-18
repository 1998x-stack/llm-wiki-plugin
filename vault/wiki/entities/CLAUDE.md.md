---
type: entity
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [configuration, architecture, constraints, AI工程]
aliases: ["CLAUDE Configuration System", "概率性 AI 系统宪法"]
relates_to: []
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# CLAUDE.md

## 概述
CLAUDE.md 是概率性 AI 系统的"宪法"——跨[[会话持久化]]的项目记忆与架构约束体系，提供多层级[[Configuration|配置]]管理。

## 关键内容

1. **三级层级结构**：
   - 全局层（~/.claude/CLAUDE.md）：个人代码风格偏好、常用工具链[[Configuration|配置]]
   - 项目层（./CLAUDE.md）：团队共享的技术栈、架构规则、禁止事项
   - 子目录层（./src/api/CLAUDE.md）：特定目录的覆盖规则

2. **架构约束实现**：
   - 结合 [[Hooks]] 强制执行硬性约束（如代码检查、数据库变更规则）
   - 与行为建议不同，通过技术手段确保规则执行

3. **[[上下文管理系统]]**：
   - 自动[[上下文压缩]]（[[Compressor wU2]]）在窗口达到92%阈值时触发
   - 保留关键代码片段和用户显式请求的内容
   - CLAUDE.md 规则跨会话持久，不受压缩影响

4. **[[Skills]] [[渐进式披露（Progressive Disclosure）|按需加载]]机制**：
   - 会话启动时加载所有 [[Skills|Skill]] 描述（轻量）
   - [[Claude_Code|Claude]] 识别需要哪个 [[Skills|Skill]] 后[[渐进式披露（Progressive Disclosure）|按需加载]]完整内容
   - [[Skills|Skill]] 用完可从上下文卸载，保持上下文开销最小

5. **[[三层记忆架构]]**：
   - 层 1：CLAUDE.md（稳定规则，每月变化）- 架构约束、技术栈声明、禁止事项
   - 层 2：记忆文件（累积上下文，每周变化）- 已尝试方案、调试决策记录、重要发现备忘
   - 层 3：[[Skills]]（复用指令集，按需演化）- 调试模式、[[代码审查]]模式等

## 来源
- [[05_to_08_combined]] — CLAUDE.md & 上下文管理系统
- [[]] — 

## 相关
- [[三层记忆架构]] — relates_to
- [[Context Management]] — relates_to
- [[Claude Code]] — relates_to
- [[Skills]] — relates_to
- [[Compact Instructions]] — relates_to

## 指令