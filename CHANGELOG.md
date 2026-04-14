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

### Phase 2 - 知识重建准备 (2026-04-15)
- 从旧系统迁移 65 个源文件到 vault/raw/（articles + books）
- 实现 `wiki:query` Claude Code 命令
- 实现 `wiki:lint` Claude Code 命令

### Phase 7 - 自动化 (2026-04-15)
- 添加 `scripts/watch-raw.sh`：fswatch 监控 raw/ 目录自动 ingest
- 添加 `scripts/cron-setup.sh`：安装定时 consolidate/lint/review 任务

### Final - Obsidian 配置 (2026-04-15)
- 添加 `.obsidian/app.json` 和 `core-plugins.json`
- 添加 vault 级 CLAUDE.md 快速参考

### Phase 3 - 个人层 (2026-04-15)
- 实现 `wiki:journal` Claude Code 命令（daily / reflection / judgment）
- 实现 `wiki:review` Claude Code 命令（weekly / monthly / quarterly 分形回顾）

### Phase 4 - 记忆系统 (2026-04-15)
- 实现 `wiki:consolidate` Claude Code 命令（Working→Episodic→Semantic→Procedural 晋升 + 置信度衰减 + journal 模式扫描）
- 实现 `wiki:crystallize` Claude Code 命令（会话结晶化 → working memory + wiki synthesis）

### Phase 5 - QA 集成 (2026-04-15)
- 实现 `wiki:qa-import` Claude Code 命令（jsonl/md 解析 → 主题聚类 → 洞见提取 → 双向链接）

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
