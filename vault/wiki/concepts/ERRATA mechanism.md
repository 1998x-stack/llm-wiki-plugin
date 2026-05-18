---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [versioning, documentation, maintenance, AI工程]
aliases: ["ERRATA机制"]
relates_to: []
supersedes: null
---

# ERRATA mechanism

## 概述
ERRATA机制是[[jezweb-claude-skills|jezweb/claude-skills]]项目中的[[ERRATA 机制|版本变更管理]]方法，用于优雅处理库更新导致的内容过时问题。

## 关键内容

1. **设计理念**：
   - 当库更新导致[[Skills|Skill]]内容过时时，不立即修改[[SKILL.md]]，而是创建[[ERRATA 机制|ERRATA.md]]
   - 保持[[Skills|Skill]]内容稳定，同时提供即时的错误修正能力

2. **文件结构**：
   ```
   skill-name/
   ├── SKILL.md          # 核心内容（稳定，少改）
   ├── ERRATA.md         # 版本变更记录（活跃更新）
   └── references/
       └── REFERENCE.md
   ```

3. **状态生命周期**：
   - active（当前有效的纠正）
   - → absorbed（已折叠进[[SKILL.md]]）
   - → outdated（库又变了，本条记录已过期）

4. **应用场景**：
   - 库更新导致原[[Skills|Skill]]内容失效
   - 发现[[Skills|Skill]]中的错误需要临时修正
   - 保持向后兼容的同时提供最新信息

## 来源
- [[jezweb/claude-skills]] — 前端插件工程
- [[]] —

## 相关
- [[jezweb/claude-skills]] — 项目
- [[Frontend Plugin]] — 前端插件体系
- [[Context Window]] — 上下文窗口
