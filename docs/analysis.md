# Vault 系统架构分析

> 2026-06-08 | 基于 v3.10 代码完整审计（14 个 Python 脚本、3 个 Shell Hook、4 个 Shell 辅助脚本）

---

## 1. 总体架构

### 1.1 三层模式

```
raw/ (不可变源)  →  wiki/ (LLM 生成知识)  →  static/ (发布产出)
        ↑ ingest              ↑ query/lint              ↑ build
```

- **raw/** — 只读源材料。PDF、DOCX、Markdown、JSONL。由人类放入，LLM 只读不写。
- **wiki/** — LLM 创建和维护的知识页面。四个子目录：`entities/`（人物/公司/项目）、`concepts/`（理论/方法/算法）、`syntheses/`（综合分析）、`qa-insights/`（QA 洞见）。
- **static/** — GitHub Pages 静态站点。`graph.html`（D3.js 图谱可视化）、`statistics.html`（Chart.js 统计面板）、`wiki/`（静态 HTML 页面）。

### 1.2 数据流全景

```
                        ┌──────────────────────┐
                        │   raw/ 源材料          │
                        └─────────┬────────────┘
                                  │
                   ┌──────────────┼──────────────┐
                   │              │              │
              markitdown    wiki:ingest    qwen_ingest.py
            (格式转换)    (Claude 驱动)   (Qwen API 驱动)
                   │              │              │
                   └──────────────┼──────────────┘
                                  │
                        ┌─────────▼─────────┐
                        │   wiki/ 知识页面    │
                        └─────────┬─────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
       PostToolUse Hooks    wiki:relink         wiki:reindex
       (lint/bm25/graph)  (自动双链补全)     (索引+主题聚类)
              │                   │                   │
              ▼                   ▼                   ▼
         log.hook.md         修改后的页面      topic-to-wiki.json
                                                 maps/*.md
              │
    ┌─────────┴─────────┐
    │  search_wiki.py   │ ◄── BM25 + maps + graph + RRF
    │  wiki:query       │
    └─────────┬─────────┘
              │
    ┌─────────▼─────────┐
    │  wiki:build       │
    │  graph.json       │
    │  statistics       │
    │  wiki HTML        │
    └─────────┬─────────┘
              │
    ┌─────────▼─────────┐
    │  static/ GitHub   │
    │  Pages 发布        │
    └───────────────────┘
```

---

## 2. 子系统分析

### 2.1 知识录入（Ingestion）

#### 两条路径

| 路径 | 引擎 | 质量 | 上下文占用 | 适用场景 |
|------|------|------|------------|----------|
| `wiki:ingest` | Claude (Sonnet) | 最高 — 理解上下文、查重、关系建立全部由 Claude 完成 | 高（需加载源文件 + 已有页面 + schema） | 单个重要文档 |
| `wiki:ingest-loop --engine=qwen` | Qwen3-Plus API | 中等 — API 提取+内置 lint，无语义查重 | 不占 Claude 上下文 | 大批量处理 |

#### wiki:ingest 执行流程（Claude 驱动，8 步）

1. 读取源文件 → 根据格式解析
2. 提取实体和概念 → 参考 `_schema/entity-types.md`
3. 查找已有页面 → 读取 slim `index.md` 全局名称列表快速去重 + `maps/*.md` 获取主题上下文
4. 创建或更新页面 → 新实体→`wiki/entities/`，新概念→`wiki/concepts/`
5. 建立关系 → frontmatter `relates_to` 双向链接
6. 矛盾检查 → `type: contradicts` 或 `supersedes`
7. 更新 index.md → `snapshot_index --slim`
8. 更新 log.md

#### qwen_ingest.py 核心逻辑

- **多页面提取**：一个源文件可产出多个 wiki 页面，用 `---PAGE_BREAK---` 分隔
- **内置 lint**：critical 错误（缺少 type/title/confidence、概述<20字、缺失 ## 概述/## 关键内容）阻止写入；warning 允许写入
- **去重**：`scan_existing_pages()` 扫描已有页面按文件名 + aliases 匹配
- **重试**：指数退避 3 次（2s/4s/8s）
- **截断**：源内容 > 100K 字符自动截断
- **think 标签过滤**：`strip_thinking_tags()` 移除 Qwen3 的 `<think>` 块
- **代码块剥离**：API 返回被 ` ```markdown ` 包裹时自动去除

#### 关键技术决策

- **文件名做标题**：文件名用自然中文（如 `牛顿法.md`），不使用 slug
- **Slim index**：v3.8 将 index.md 从 ~626 行精简到 ~35 行，详细清单移至 `maps/*.md`
- **Topic 过滤**：`build_ingest_context.py --topic` 将 ingest 子代理上下文从 ~600 页缩减到 ~20-70 页

### 2.2 搜索与检索（Search & Retrieval）

#### search_wiki.py — 统一搜索的核心

**三种检索策略 + RRF 融合**：

```
用户查询
    │
    ├─→ BM25 全文检索 (jieba 分词 + rank_bm25)
    │   取 top_k * 2 候选
    │
    ├─→ Maps 主题扩展
    │   扫描 maps/*.md，按 token 重叠+子串匹配找最佳主题
    │   返回该主题下所有 [[页面]]
    │
    └─→ Graph 图遍历
        以 BM25 top-5 为种子，1-hop BFS 扩展邻居
        (已验证文件存在)
         │
         ▼
    RRF (k=60) 融合排序 → top_k 结果
```

**RRF 公式**：`score = Σ 1/(k + rank_i + 1)`，`k=60`

**亮点**：
- maps 匹配的"子串回退"：token 重叠为 0 时检查 `qt in topic or topic in qt`，确保中文长查询能匹配短主题名
- 图遍历带文件存在性验证：`candidate.exists()` 防止图中有死链
- 结果带 `sources` 标注，可追溯每个页面来自哪些检索源

#### BM25 索引管理（bm25_index.py）

- **存储格式**：`corpus.pkl`（文档语料）+ `index.pkl`（BM25Okapi 对象）+ `docmap.json`（ID→路径映射）
- **分词**：jieba 搜索模式（`cut_for_search`），加载 `wiki/keywords.txt` 自定义词典
- **预处理**：去除 frontmatter → 展开 `[[双链]]` 为纯文本 → 清除 Markdown 标记 → 过滤停用词和长度≤1 的 token
- **增量更新**：`update` 命令移除旧条目、分配新 ID 后重新索引

#### keywords.txt — jieba 自定义词典

`build_keywords.py` 从所有 wiki 页面提取 title（权重 5）、aliases（权重 3）、tags（权重 2），过滤年份范围模式（`\d{4}-{1,2}\d{0,4}$`）防止 `1707--1783` 类污染。

### 2.3 知识图谱（Knowledge Graph）

#### build_graph.py — 双遍扫描构建

**Pass 1**：构建节点。从 frontmatter 提取 type、confidence、tags。
**Pass 2**：提取边。两个来源：
- frontmatter `relates_to` → 带关系类型的边
- 正文 `[[双链]]` → `wikilink` 类型的边

**边的方向性处理**：
- 有向关系（contradicts、supersedes、extends、implements、caused、depends_on）：`(source, target, relation)` 作为去重键，保留方向
- 无向关系（wikilink、related_to 等）：`(sorted(a,b), relation)` 作为去重键

**连通分量分析**：BFS 遍历，识别孤节点（edge_count=0 的单节点分量）。

**`--full` 模式**：级联调用 `build_statistics.py` + `build_wiki_pages.py`，输出到 `static/`。

#### build_statistics.py

基于 networkx 的高级图指标：degree 分布、betweenness centrality、PageRank、clustering coefficient、diameter/radius/center、bridge edges。输出 `graph-statistics.json` 供 `statistics.html` 前端消费。

### 2.4 质量与维护（Quality & Maintenance）

#### lint_wiki.py — 9 项检查

| 代码 | 检查 | 严重度 |
|------|------|--------|
| F1 | 缺失必需 frontmatter 字段（type, status, confidence, created, tags, relates_to） | error |
| F2 | YAML frontmatter 无法解析 | error |
| F3 | 概述 > 200 字 | warning |
| F4 | 空段落（有 heading 无内容） | warning |
| B1 | `[[链接]]` 指向不存在的页面 | warning |
| B2 | 页面不在 BM25 docmap 中 | warning |
| I1 | 页面不在 index.md 中（支持 wikilink + slim 纯文本两种格式） | warning |
| I2 | index.md 有指向不存在页面的条目（自动跳过 `maps/` 前缀） | warning |
| O1 | 孤页 — 无入链 | warning |

**性能优化**：全局扫描时缓存文件内容（`file_texts` dict），避免 O1 检查时的二次读取（~185 次文件读取消除）。

**退出码**：0 = 无 error，2 = 有 error。

#### snapshot_index.py — Index 完整性管理

三种模式：
- **check**（默认）：对比 wiki 页面 vs index.md，报告缺失和孤条目
- **--update**：将缺失页面按 type 插入 index.md 对应分区（仅支持旧版 verbose 格式）
- **--slim**：将 index.md 重写为紧凑格式：统计表 + 逗号分隔全局名称列表
- **--snapshot**：保存快照到 `.claude/reindex.snapshot.json`

#### relink.py — 自动双链补全

**算法**：
1. 从所有 wiki 页面收集 term→page 映射（title + aliases，共 ~1003 词条）
2. 按 term 长度降序排列（最长匹配优先）
3. 对每个页面，在正文中查找裸 term 出现
4. 跳过保护区（frontmatter、已有 `[[]]`、代码块、内联代码、标题行、`## 来源` 及之后）
5. 跳过自引用
6. 已消耗字符范围防止短 term 覆盖长 term

**保护区设计**：frontmatter、已有 wikilink、fenced code、inline code、heading、`## 来源`→ 末尾。排序合并重叠区间后检查。

**幂等性**：运行两次添加零个新链接。已验证。

**英文 term 处理**：ASCII-only term 最小长度 5（防止 `rg`→ripgrep、`fd`→fd、`uv`→uv 类误匹配）；CJK 最小长度 2。

### 2.5 记忆系统（Memory）

四层记忆生命周期：

```
Working Memory          Episodic Memory        Semantic Memory         Procedural Memory
_memory/working/       _memory/episodic/       _memory/semantic/       _memory/procedural/
会话级临时观察    →    按天聚合         →    跨天确认事实       →    稳定行为模式
                     (3+ episode 重复)        (5+ semantic 描述)
```

**置信度衰减（Ebbinghaus）**：
- slow（半衰期 180 天）：架构决策、核心概念
- medium（半衰期 60 天）：一般事实
- fast（半衰期 14 天）：临时 bug、短期观察
- confidence < 0.3 → `status=stale`

**Memory vs Wiki 边界规则**：semantic/ = 单一事实声明（不跨主题），syntheses/ = 跨 3+ 概念的跨主题分析。严禁重复。

### 2.6 自动化系统（Automation）

#### PostToolUse Hooks

三个钩子在每次 Write/Edit 到 `wiki/**/*.md` 时触发：

| 钩子 | 动作 | 去重/优化 |
|------|------|-----------|
| `hook_lint.sh` | 单文件 lint check | — |
| `hook_bm25.sh` | 增量 BM25 更新 | — |
| `hook_graph.sh` | 全量 graph 重建 | 30s debounce（文件 mtime 差 < 30s 时跳过） |

**Hook 协议**：从 stdin JSON 读取 `tool_input.file_path`（Claude Code hooks 协议），过滤 `.claude/` 路径。错误写入 `log.hook.md`（经 v3.9 修复，之前 `2>/dev/null` 静默吞噬错误）。

#### Cron 自动化

| 时间 | 操作 |
|------|------|
| 每日 02:07 | `wiki:consolidate` — 记忆晋升 + 衰减 |
| 每周日 20:13 | `wiki:lint` + `wiki:review weekly` |
| 每月 1 号 03:17 | `wiki:consolidate --deep` — Semantic→Procedural + 月度报告 |

#### 文件监控

`watch-raw.sh` 使用 fswatch 监听 `raw/` 目录，新文件出现时自动触发 `wiki:ingest`。

---

## 3. 关键设计模式

### 3.1 共享工具模块（wiki_utils.py）

v3.3 引入，消除了 6 个重复的 frontmatter 解析器、2 个重复的停用词列表、2 个重复的分词器。所有脚本导入同一套 `parse_frontmatter`、`tokenize`、`STOP_WORDS`、路径常量。

**设计细节**：
- jieba 延迟加载（`_get_jieba()`）避免导入开销
- `keywords.txt` 自定义词典仅在首次调用 `tokenize()` 时加载一次（`_jieba_dict_loaded` 标志）
- yaml 未安装时的 fallback：简单 `key: value` 行解析

### 3.2 Wrapper 模式（wiki.sh）

所有 Python 脚本通过 `wiki.sh` 统一调用：处理 CWD（cd 到 vault/）+ PYTHONPATH + 脚本发现。解决了从不同目录调用脚本时的路径问题。

### 3.3 Computed Artifacts 模式

多个文件从 wiki/ 内容计算生成，不手动维护：
- `graph.json` ← `build_graph.py`
- `graph-statistics.json` ← `build_statistics.py`
- `maps/*.md` ← `build_maps.py`（从 `topic-to-wiki.json` 生成）
- `wiki/keywords.txt` ← `build_keywords.py`
- `index.md`（slim 格式）← `snapshot_index --slim`
- `raw/raw-wiki-map.json` ← `build_raw_wiki_map.py`

### 3.4 最长匹配优先（relink.py）

按 term 长度降序处理，已消耗字符范围防止短 term 覆盖长 term 的已链接部分。标准 NLP 方法，实现清晰。

### 3.5 JSON 输出一致性

所有 Python 脚本输出 JSON（或带 `--json` 标志），便于被 Hook、CI、和外部工具消费。

---

## 4. 代码质量观察

### 4.1 做得好的地方

- **wiki_utils.py 消除重复**：从 7 个脚本中抽取出共享逻辑，v3.3 重构质量高
- **relink.py 的保护区设计**：frontmatter、代码块、已有链接、来源段的保护周全，幂等性经过验证
- **search_wiki.py 的模块化**：三种检索策略独立函数 + RRF 融合，干净可测试
- **qwen_ingest.py 的错误处理**：重试、截断、去重、lint、think 标签过滤 — 生产级别的鲁棒性
- **hook_graph.sh 的 debounce**：30s 内重复编辑不重建图，避免 185 文件全扫描
- **snapshot_index.py 的完整性**：check/update/snapshot/slim 四种模式覆盖所有使用场景

### 4.2 值得注意的地方

**pickle 的可移植性问题**：BM25 索引使用 pickle 序列化，跨 Python 版本和环境可能不兼容。文档中已记录（gotcha #19），但未解决。

**Hook 重复工作**：每次 wiki 编辑触发 lint + BM25 + graph 三个 hook，而 `wiki:ingest` 结束时会再次执行这些操作。文档已记录（NEXT_STEPS §2.2），决策是"接受重复，500+ 页时再优化"。

**index.md 双格式支持**：`load_index_links()` 同时支持 wikilink 格式和 slim 纯文本格式，因为历史页面可能还包含旧格式引用。这是技术债务，但在当前规模下合理。

**qwen_ingest.py 的 `--wiki` legacy 模式**：单文件输出模式保留用于向后兼容，增加了代码路径复杂度。

**网络依赖**：`build_statistics.py` 需要 networkx（可选），`build_wiki_pages.py` 需要 markdown（必需），`bm25_index.py` 需要 rank_bm25（必需）。非 Python 依赖已明确记录在 requirements.txt。

**`_is_valid_keyword()` 正则**：`r'^\d{4}-{1,2}\d{0,4}$'` 可能漏掉其他异常 alias 模式（如纯数字、特殊字符），但 28 个年份范围的已知问题已解决。

### 4.3 规模考虑

当前系统处理 ~3,000 页（26 个 topics），以下模式可能在更大规模时成为瓶颈：
- `build_graph.py` 全量重建（每次 wiki 编辑触发）
- BM25 pickle 索引不支持分布式
- `search_wiki.py` 的 maps 匹配是线性扫描
- hook lint 和 hook BM25 对单文件操作是 O(1)，但 hook graph 是 O(n)

---

## 5. 已解决的重大 Bug（v3.0-v3.10）

| 版本 | 问题 | 修复 |
|------|------|------|
| v3.10 | slim 格式 index.md 导致 953 页 I1 误报 | `load_index_links()` 增加纯文本解析 |
| v3.9 | setup-ingest-loop.sh 产生无效 YAML | 修复换行符 |
| v3.9 | split_chat_json.py 在验证前删除源文件 | 移到验证后删除 |
| v3.9 | Hook 静默吞噬 JSON 解析错误 | 移除 `2>/dev/null` |
| v3.8 | guidelines/ 和 maps/ 双目录维护 | 合并到 maps/ |
| v3.7 | 28 个 entity 页面的年份范围污染 keywords.txt | `_is_valid_keyword()` 正则过滤 |
| v3.7 | 125 个页面的 `## 来源` 格式不标准 | 批量修复为 `[[双链]]` 或 `[text](URL)` |
| v3.4 | macOS 大小写不敏感导致文件夹比较错误 | case-insensitive 比较 |
| v3.3 | XSS in build_wiki_pages.py | `html.escape()` 转义 wikilink 名称 |
| v3.3 | 边方向性丢失（contradicts/supersedes 等） | 有向边保留 source→target 顺序 |
| v3.1.1 | Qwen3 `<think>` 标签破坏 frontmatter 解析 | `strip_thinking_tags()` |
| v3.2 | Hook 未收到文件路径（`$CLAUDE_TOOL_ARG_file_path` 不是真实变量） | 从 stdin JSON 读取 `tool_input.file_path` |

---

## 6. 脚本依赖关系

```
wiki_utils.py ◄── bm25_index.py
              ◄── search_wiki.py
              ◄── build_graph.py
              ◄── build_statistics.py
              ◄── build_wiki_pages.py
              ◄── lint_wiki.py
              ◄── snapshot_index.py
              ◄── build_maps.py
              ◄── build_keywords.py
              ◄── build_ingest_context.py
              ◄── relink.py
              ◄── qwen_ingest.py

build_graph.py ──→ build_statistics.py (via --full)
               ──→ build_wiki_pages.py  (via --full)

build_maps.py ◄── .claude/topic-to-wiki.json
build_ingest_context.py ◄── .claude/topic-to-wiki.json

search_wiki.py ◄── index/BM25/*.pkl
              ◄── maps/*.md
              ◄── graph.json

lint_wiki.py ◄── index/BM25/docmap.json
            ◄── index.md
            ◄── maps/*.md
```

`wiki_utils.py` 是整个系统的唯一共享依赖，所有脚本通过它获得一致的路径解析、frontmatter 解析、分词和 HTML 转义。

---

## 7. 数据文件总览

| 文件 | 格式 | 生产者 | 消费者 |
|------|------|--------|--------|
| `graph.json` | JSON | build_graph.py | search_wiki.py, build_statistics.py, graph.html, lint_wiki.py |
| `graph-statistics.json` | JSON | build_statistics.py | statistics.html |
| `index/BM25/corpus.pkl` | pickle | bm25_index.py | bm25_index.py, search_wiki.py |
| `index/BM25/index.pkl` | pickle | bm25_index.py | bm25_index.py, search_wiki.py |
| `index/BM25/docmap.json` | JSON | bm25_index.py | lint_wiki.py, search_wiki.py |
| `wiki/keywords.txt` | jieba dict | build_keywords.py | wiki_utils.py (tokenize) |
| `index.md` | Markdown | snapshot_index.py | lint_wiki.py, wiki:ingest, wiki:query |
| `maps/*.md` | Markdown | build_maps.py | search_wiki.py, wiki:ingest, wiki:query, lint_wiki.py |
| `.claude/topic-to-wiki.json` | JSON | wiki:reindex (LLM subagent) | build_maps.py, build_ingest_context.py, snapshot_index.py |
| `.claude/reindex.snapshot.json` | JSON | snapshot_index.py | 完整性审计 |
| `raw/re-map.json` | JSON | wiki:reorganize-raw (LLM) | reclassify_raw.py |
| `raw/raw-wiki-map.json` | JSON | reclassify_raw.py, build_raw_wiki_map.py | wiki:query |
| `log.md` | Markdown | 各命令 | 操作审计 |
| `log.hook.md` | Markdown | 三个 Hook | Hook 调试 |
