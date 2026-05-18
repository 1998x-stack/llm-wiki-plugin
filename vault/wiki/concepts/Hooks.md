---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-tools, automation, lifecycle, constraints, AI工程]
aliases: ["Hooks System", "Lifecycle Hooks", "Hook System", "钩子系统"]
relates_to:
  - target: "[[Claude Code]]"
    type: extends
  - target: "[[Agent Skills]]"
    type: complements
  - target: "[[CLAUDE.md]]"
    type: implements
  - target: "[[Permissions]]"
    type: implements
supersedes: null
---

# Hooks

## 概述
[[Claude Code]]中的生命周期钩子机制，在特定阶段（PreTool、PostTool等）自动执行，是扩展机制全家桶的重要组成部分。Hooks 用于实现架构约束和[[Permissions|权限]]控制，通过强制执行[[刚性规则|硬性规则]]而非概率性建议来确保系统行为的一致性。

## 关键内容

1. **基本特征**：
   - 在[[Claude Code]]特定阶段自动执行
   - 包括PreTool、PostTool等阶段
   - 是扩展机制的一部分

2. **在扩展机制中的位置**：
   - 与[[CLAUDE.md]]、[[Agent Skills]]、[[MCP|MCP Servers]]、[[Claude Connectors]]、[[Plugins]]、[[Agents]]共同构成扩展机制全家桶
   - 在特定生命周期节点触发

3. **应用场景**：
   - 在工具调用前后的自动化处理
   - 代码质量检查
   - 自动索引更新（如BM25索引、图谱重建等）
   - 实现架构约束：所有 [[Python]] 文件必须通过 `ruff check` + `mypy --strict`
   - [[Permissions|权限]]控制：[[Tool Hook Mechanism|PreToolUse Hook]] 进行确定性拦截，命中黑名单立即拦截

4. **架构约束实现**：
   - 结合 [[CLAUDE.md]] 实现硬性约束（通过 Hook 强制执行）
   - 与行为建议不同，通过技术手段确保规则执行
   - 例如：数据库变更必须通过 Alembic migration，禁止直接 DDL

## 来源
- [[raw/articles/ai-tools/claude-skills/01_claude_code_skill_system_overview.md]] — 全文
- [[05_to_08_combined.md]] — 05 · CLAUDE.md & 上下文管理系统

## 相关
- [[Claude Code]] — extends
- [[Agent Skills]] — complements
- [[CLAUDE.md]] — implements
- [[Permissions]] — implements
- [[Tool Hook Mechanism]] — relates_to