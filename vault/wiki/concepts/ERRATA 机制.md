---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [version-control, documentation, skills-management, AI工程]
aliases: ["ERRATA 机制", "ERRATA.md", "版本变更管理"]
relates_to:
  - target: "[[jezweb/claude-skills]]"
    type: implements
  - target: "[[Agent Skills]]"
    type: enhances
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# ERRATA 机制

## 概述
[[jezweb-claude-skills|jezweb/claude-skills]] 项目中的版本变更管理机制，用于处理库更新导致的[[Skills|技能]]内容过时问题，通过分离核心内容和版本变更记录来保持[[Skills|技能]]内容的稳定性。

## 关键内容
1. **设计原理**：当库更新导致[[Skills|技能]]内容过时时，不立即修改 [[SKILL.md]]，而是创建 ERRATA.md 文件记录变更，保持核心内容稳定。

2. **文件结构**：
   - [[SKILL.md]]：核心内容（稳定，少改动）
   - ERRATA.md：版本变更记录（活跃更新）
   - REFERENCE.md：参考资料

3. **状态生命周期**：ERRATA 记录有三种状态 - active（当前有效的纠正）、absorbed（已合并到 [[SKILL.md]]）、outdated（库再次变更，记录已过时）。

4. **优势**：提供即时的错误修正能力，同时保持[[Skills|技能]]内容的稳定性，避免频繁的文档更新造成混乱。

5. **应用场景**：特别适用于快速发展的前端生态，如 [[Tailwind CSS]]、[[React]] 等库的频繁更新。

## 来源
- [[04_jezweb_claude_skills_frontend]] — ERRATA 机制解析

## 相关
- [[jezweb/claude-skills]] — 实现该机制的项目
- [[Agent Skills]] — 优化的技能类型