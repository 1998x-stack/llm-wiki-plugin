# Changelog

## [Unreleased]

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
