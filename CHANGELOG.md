# Changelog

## [Unreleased]

### Phase 1 - 最小可行 vault (2026-04-15)
- 创建完整 vault 目录结构（_schema / _memory / raw / wiki / journal / templates）
- 写入主 schema `_schema/CLAUDE.md`（ingest/query/lint 操作手册 + frontmatter 规范 + 隐私规则）
- 写入类型定义（entity-types.md, relationship-types.md, quality-rules.md）
- 写入 5 套模板（daily, wiki-page, reflection, judgment, weekly-review）
- 创建 index.md, log.md, dashboard.md
- 创建 growth 跟踪文件（skills-tracker.md, cognitive-patterns.md）
- 实现 `wiki:ingest` Claude Code 命令

### Added
- 系统设计文档：Obsidian Brain 完整架构设计 (`docs/superpowers/specs/2026-04-14-obsidian-brain-design.md`)
  - 融合 LLM Wiki v1、v2、kepano-Obsidian 三套方法论
  - Vault 目录结构设计（_schema / _memory / raw / wiki / journal）
  - 四层记忆系统（Working → Episodic → Semantic → Procedural）
  - 8 个 Agent Skills 定义（ingest / query / lint / consolidate / crystallize / journal / review / qa-import）
  - 个人层（Journal 系统）：daily notes + reflections + judgments + growth tracking
  - QA jsonl 数据集成方案
  - 分层搜索架构（index.md → frontmatter graph → qmd → grep）
  - 全自动化事件表（零人工的 ingest / consolidate / lint）
  - 5 套模板（daily / wiki page / reflection / judgment / weekly review）
  - 7 阶段渐进实施路径
- README.md：项目概览
- CHANGELOG.md：变更记录
- v1 vs v2 对比分析 (`compare.md`)
- CLAUDE.md：项目指令文件
