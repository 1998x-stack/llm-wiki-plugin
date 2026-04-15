# Changelog

## [v2.3] - 2026-04-15

### Enhanced
- `wiki:reindex` command: detailed step-by-step workflow with tag taxonomy, maps format spec, error handling
- `qwen_ingest.py`: multi-page extraction — one raw file can produce multiple wiki pages via `---PAGE_BREAK---` delimiter
  - New JSON output: `{"status": "SUCCESS", "pages": [{"type", "wiki_name", "markdown"}]}`
  - Legacy `--wiki` mode preserved for backwards compatibility
- `ingest-loop-qwen.md`: updated to use multi-page mode, auto-determines entity/concept paths from JSON
- `CLAUDE.md`: updated scripts table with all V2.1-V2.3 additions
- `README.md`: added static site features (statistics dashboard, wiki viewer), updated commands table

## [v2.2] - 2026-04-15

### Fixed
- Created missing hook scripts (`hook_lint.sh`, `hook_bm25.sh`, `hook_graph.sh`) — were referenced but never created
- Recovered `index.md` from hub-rewrite, now contains all 121 page entries
- Fixed View Page button in graph.html — removed duplicate `wiki/` prefix in URL
- Replaced `build_reindex.py` with `snapshot_index.py` — validates index integrity without overwriting

### Enhanced
- `build_graph.py`: added `--full` flag to also build statistics JSON + wiki HTML pages
- `deploy.yml`: simplified from 4 build steps to single `build_graph.py --full`
- `wiki:graph` command: updated to use `--full` flag

## [v2.1] - 2026-04-15

### Added
- `build_wiki_pages.py`: converts wiki/*.md to static HTML with topbar nav, metadata cards, wikilinks
- `statistics.html`: Chart.js dashboard with type/confidence/tag/growth/relationship charts
- `build_statistics.py`: generates `graph-statistics.json` from graph + frontmatter
- `build_reindex.py`: topic-clustered index maps in `vault/maps/`
- `wiki:reindex` command: topic-clustered indexing
- Graph.html: topbar navigation (Graph | Statistics | Wiki) + "View Page" button in sidebar
- `deploy.yml`: added wiki pages, statistics, reindex build steps

### Content
- Batch ingest: 50+ new wiki pages from 数值分析 and 概率论 chapters

## [v2.0] - 2026-04-15

### Added — Scripts Foundation
- `scripts/bm25_index.py`: BM25 全文检索索引构建与查询（jieba 中文分词 + rank_bm25）
- `scripts/build_graph.py`: 知识图谱 JSON 构建器（frontmatter + wikilink 提取，连通分量分析）
- `scripts/lint_wiki.py`: Wiki 质量检查器（frontmatter 校验、链接完整性、index 一致性）
- `scripts/qwen_ingest.py`: 通义千问 API 驱动的 wiki 页面提取（OpenAI 兼容接口）
- `requirements.txt`: Python 依赖声明（jieba, rank_bm25, pyyaml, openai）

### Added — Commands
- `scripts/setup-ingest-loop.sh`: Ralph-loop 自动逐文件 ingest（Claude 驱动）
- `scripts/setup-ingest-loop-qwen.sh`: Ralph-loop 自动逐文件 ingest（Qwen API 驱动）
- `scripts/build_graph.py`: 知识图谱构建命令（`python3 scripts/build_graph.py`）
- `vault/qa/`: QA 数据存放目录
- `vault/wiki/qa-insights/`: QA 洞见提取输出目录

### Added — Hooks & Automation
- `scripts/hook_bm25.sh`: ingest 后自动重建 BM25 搜索索引
- `scripts/hook_graph.sh`: ingest 后自动重建知识图谱 JSON
- `scripts/hook_lint.sh`: ingest 后自动运行质量检查
- `vault/log.hook.md`: Hook 执行日志
- `scripts/setup-ingest-loop.sh`: Claude ingest-loop 自动化设置
- `scripts/setup-ingest-loop-qwen.sh`: Qwen ingest-loop 自动化设置

### Added — Documentation
- `docs/wiki.md`: Wiki 系统技术文档
- `USERGUIDE.md`: 完整用户指南（中文，覆盖安装、命令、工作流、排障）
- `graph.html`: D3.js 交互式知识图谱可视化页面
- `.github/workflows/deploy.yml`: GitHub Actions 自动部署 graph.html 到 GitHub Pages

### Enhanced
- `wiki:ingest` 命令：支持 hook 触发链（BM25 + graph + lint）
- `wiki:query` 命令：集成 BM25 搜索结果作为候选来源
- `wiki:lint` 命令：新增 Python lint 脚本后端支持
- `templates/wiki-page.md`: 增加 confidence、sources、relates_to frontmatter 字段
- `vault/CLAUDE.md`: 新增 hook 系统说明和 BM25 查询指引
- `vault/_schema/CLAUDE.md`: 更新 ingest/query/lint 操作规范
- `README.md`: 重写为专业 GitHub 项目 README（架构图、命令表、快速开始）

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
