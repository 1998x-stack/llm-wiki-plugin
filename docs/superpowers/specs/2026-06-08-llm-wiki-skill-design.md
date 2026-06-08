# LLM Wiki Skill — 设计规格

> 2026-06-08 | 从现有 vault/ 系统提取可复用内核，封装为可安装的 Claude Code skill
>
> 经 grill-with-docs（命令层 + 架构层）、grill-me（scripts 层）、系统论/控制论视角（结构层）三轮审查

## 1. 目标

将 llm-wiki 的知识管理系统提取为一个可复用的 Claude Code skill (`llm-wiki`)，用户安装后可在任意目录初始化个人知识库，支持独立文件夹和 Obsidian vault 注入两种部署模式。

## 2. 范围

**包含**：核心引擎（11 个保留 Python 脚本 + 1 个新增 ingest_loop.py + wiki.sh 包装器）、5 个 Claude Code 命令（+ init）、Schema 默认定义、页面/Journal 模板、wiki 页面生命周期管理、自适应自动化

**不包含**：静态站点生成（`build_wiki_pages.py`、`build_statistics.py`）、raw/ 重组工具（`reclassify_raw.py`、`build_raw_wiki_map.py`）、`split_chat_json.py`、ralph-loop 脚本、硬编码 cron 任务、fswatch 监控、`_memory/` 独立目录

## 3. Skill 文件结构

```
llm-wiki/
├── SKILL.md                    # 入口：核心规则 + 路径发现 + 命令索引（精简）
├── commands/                   # 命令详情（按需用 Read 加载）
│   ├── init.md                 # 一次性初始化
│   ├── ingest.md               # 知识录入（含 convert + qa 路由）
│   ├── ingest-loop.md          # 批量 ingest（脚本驱动，末尾自动 relink）
│   ├── query.md                # 统一搜索 + 回答
│   ├── journal.md              # 日记/反思/判断（含 !insight 标记支持）
│   ├── review.md               # 周/月/季回顾 + 健康检查 + 结晶化 + 自适应自动化
│   └── maintain.md             # 健康检查 + lint + reindex + keywords + graph
├── scripts/
│   ├── wiki.sh                 # 包装器（CWD 保证 + PYTHONPATH）
│   ├── wiki_utils.py           # discover_wiki_root() + 模块级路径常量
│   ├── bm25_index.py
│   ├── search_wiki.py
│   ├── build_graph.py          # 移除 --full 模式
│   ├── build_maps.py           # 冷启动检测（< 20 页跳过）
│   ├── build_keywords.py
│   ├── build_ingest_context.py # 分层 schema/template 覆盖读取
│   ├── lint_wiki.py
│   ├── snapshot_index.py
│   ├── relink.py
│   ├── qwen_ingest.py          # scan_existing_pages() 改用 discover_wiki_root()
│   ├── ingest_loop.py          # hash 追踪 + 断点续传 + 末尾自动 relink
│   ├── requirements.txt
│   └── hooks/                  # 轻量 hook 脚本
│       ├── bm25.sh             # 从 stdin JSON 提取 file_path → BM25 增量更新
│       └── graph.sh            # 从 stdin JSON 提取 file_path → graph 重建（30s debounce）
├── schemas/                    # 默认 schema（只读，用户可 _schema/ 覆盖）
│   ├── entity-types.md
│   ├── relationship-types.md
│   └── quality-rules.md
├── templates/                  # 默认模板（只读，用户可 templates/ 覆盖）
│   ├── wiki-page.md
│   ├── daily.md
│   ├── reflection.md
│   ├── judgment.md
│   └── weekly-review.md
└── resources/
    └── init-kit/               # /llm-wiki:init 的脚手架
        ├── .wiki-root          # 空标记文件
        ├── raw/
        │   └── qa/
        ├── wiki/
        │   ├── entities/
        │   ├── concepts/
        │   └── syntheses/
        ├── journal/
        │   ├── daily/
        │   ├── reflections/
        │   ├── judgments/
        │   └── growth/
        ├── maps/
        ├── index.md             # 初始骨架
        └── log.md               # 空文件
```

**关键设计决策**：
- `_memory/` 目录已删除。记忆状态嵌入 wiki 页面自身 frontmatter（status + confidence + decay_rate），wiki/ 是知识的唯一载体。
- `wiki/qa-insights/` 合并到 `syntheses/`。QA 洞见本质上就是综合分析。
- `_schema/` 和 `templates/` 不在 init-kit 中复制。命令读取时采用分层覆盖：skill 默认值 + 用户可选覆盖。
- Hook 脚本放在 `scripts/hooks/` 下（轻量 shell，3-5 行），init 时写入 `.claude/settings.local.json` 的绝对路径。

## 4. 路径发现机制

### 4.1 发现优先级

```
1. 环境变量 LLM_WIKI_ROOT（显式设置，最高优先）
2. 从 CWD 向上查找 .wiki-root 标记文件
3. 未找到 → 报错，提示运行 /llm-wiki:init
```

### 4.2 wiki_utils.py 实现

路径常量在模块导入时计算（`discover_wiki_root()` 在模块级调用一次），保持现有 `from wiki_utils import VAULT_DIR, WIKI_DIR, ...` 的导入兼容性：

```python
def discover_wiki_root() -> Path:
    if env_root := os.environ.get("LLM_WIKI_ROOT"):
        return Path(env_root)
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".wiki-root").exists():
            return parent
    raise WikiRootNotFound("未找到 .wiki-root")

VAULT_DIR = discover_wiki_root()
WIKI_DIR = VAULT_DIR / "wiki"
INDEX_DIR = VAULT_DIR / "index" / "BM25"
MAPS_DIR = VAULT_DIR / "maps"
GRAPH_PATH = VAULT_DIR / "graph.json"
INDEX_FILE = VAULT_DIR / "index.md"
KEYWORDS_PATH = WIKI_DIR / "keywords.txt"
```

### 4.3 wiki.sh 适配

`wiki.sh` 中：
- `SCRIPT_DIR` 从自身路径（`$0`）推导，指向 skill 内 `scripts/`
- `VAULT_DIR` 通过从 CWD 向上查找 `.wiki-root` 确定
- `cd "$VAULT_DIR"` 保证 Python 脚本执行时 CWD=wiki root（`discover_wiki_root()` 从 CWD 向上查找，始终成功）
- `PYTHONPATH` 指向 `$SCRIPT_DIR`，保证 `from wiki_utils import ...` 可用

`wiki.sh` 是脚本的唯一入口——不通过 wiki.sh 直接调用 Python 脚本的行为不受支持。

### 4.4 Hook 脚本

`scripts/hooks/bm25.sh`：
```bash
FILE=$(cat | python3 -c 'import sys,json; print(json.load(sys.stdin)["tool_input"]["file_path"])')
WIKI_ROOT=$(while [ ! -f .wiki-root ] && [ "$PWD" != "/" ]; do cd ..; done; pwd)
cd "$WIKI_ROOT" && bash <skill>/scripts/wiki.sh bm25_index update "$FILE"
```

`scripts/hooks/graph.sh`：
```bash
FILE=$(cat | python3 -c 'import sys,json; print(json.load(sys.stdin)["tool_input"]["file_path"])')
WIKI_ROOT=$(while [ ! -f .wiki-root ] && [ "$PWD" != "/" ]; do cd ..; done; pwd)
GRAPH="$WIKI_ROOT/graph.json"
if [ -f "$GRAPH" ]; then
    AGE=$(( $(date +%s) - $(stat -f %m "$GRAPH") ))
    [ "$AGE" -lt 30 ] && exit 0
fi
cd "$WIKI_ROOT" && bash <skill>/scripts/wiki.sh build_graph
```

lint 不设 hook——它是诊断工具，在 maintain 流水线中全量运行。

## 5. 命令设计

所有命令以 `/llm-wiki:` 为前缀。SKILL.md 仅含命令索引和核心规则，命令详细步骤在 `commands/*.md` 中按需读取。

### 5.1 命令清单

| 命令 | 用途 | 说明 |
|------|------|------|
| `init` | 一次性初始化知识库 | 创建目录结构、.wiki-root、pip install、写 hooks |
| `ingest` | 源材料 → wiki 页面 | 自动检测格式路由；支持 `all` 批量模式；支持 `!insight` 直接输入 |
| `ingest-loop` | 批量 ingest（脚本驱动） | ingest_loop.py：hash 追踪 + 断点续传 + 末尾自动 relink |
| `query` | 统一搜索 + 回答 | BM25 + maps + graph + RRF |
| `journal` | 日记/反思/判断 | 支持 `!insight` 标记直接创建 wiki 页面 |
| `review` | 系统健康检查 + 周/月/季回顾 + 结晶化 + 自适应自动化 | 合并原 review + crystallize + consolidate |
| `maintain` | 一键知识库维护 | check + lint + reindex + keywords + graph（不含 relink，已移至 ingest-loop 末尾） |

### 5.2 合并对照

| 原命令 | 去向 |
|--------|------|
| `ingest` + `convert-to-markdown` + `qa-import` | → `ingest`（自动格式路由） |
| `check` + `lint` + `reindex` + `build` | → `maintain`（内部步骤） |
| `crystallize` + `consolidate` + `review` | → `review`（阶段性沉淀 + 健康检查） |
| `relink` | → `ingest-loop` 末尾自动触发 + `maintain` 中保留（保险） |
| `journal` | → `journal`（保持独立，新增 `!insight`） |

### 5.3 ingest 格式路由

```
输入检测：
├─ !insight 标记（从 journal 中）
│   → 直接创建/更新 wiki 页面
├─ 非 markdown (.pdf/.docx/.pptx/.xlsx/.html/.epub/.csv)
│   → 先调用 markitdown 转换为 .md
│   → 然后走 markdown 提取逻辑
├─ markdown，路径在 raw/qa/ 下
│   → Q&A 聚类 + 跨轮洞见提取
│   → 输出 wiki/syntheses/
└─ markdown，路径在 raw/ 其他位置
    → 实体/概念提取
    → 输出 wiki/entities/ + wiki/concepts/
```

### 5.4 maintain 内部步骤

```
1. check   → 只读全量诊断（F1-F4, B1-B2, I1-I2, O1, M1-M2，9 项检查）
2. lint    → 基于诊断结果自动修复
3. reindex → snapshot_index --slim + build_maps（topic-to-wiki.json → maps/*.md）
             冷启动保护：wiki 页面 < 20 时跳过 topic 聚类和 maps 生成
4. build   → build_keywords.py + build_graph.py（keywords.txt + graph.json）
```

graph 和 keywords 也由 PostToolUse hooks 实时维护（BM25 hook + graph hook 30s debounce），此处为全量保险重建。

### 5.5 review 命令流程

```
0. 系统健康检查
   ├─ 读取 log.md 上次 maintain 时间戳 → > 7 天提醒
   └─ 读取 wiki/ 文件数 vs 上次 maintain 快照差值 → > 20 页提醒

1. 收集素材（扫描过去 7/30/90 天 journal）
2. 模式发现（高频主题、新连接）
3. 结晶化（3+ 概念形成新洞见 → wiki/syntheses/）
4. Journal → Wiki 链接扫描
   ├─ 扫描近期 journal 中的 [[wiki链接]] 引用
   └─ 某页面 3+ 天被引用 + confidence < 0.5 → 提议提升置信度或补充内容
5. !insight 处理
   └─ 扫描 journal 中的 !insight 标记段落 → 创建/更新 wiki 页面
6. 记忆衰减（wiki 页面 confidence 按 Ebbinghaus 衰减）
   ├─ slow（180d半衰期）、medium（60d）、fast（14d）
   └─ confidence < 0.3 → status: stale
7. 自适应自动化检测
   ├─ 操作频率检测 → 提议 cron
   └─ 维护提醒 → X 天未 maintain 主动建议
```

## 6. 初始化命令 (`/llm-wiki:init`)

```
1. 检测当前目录
   ├─ 空目录 / 新目录 / 无 .obsidian/ → 完整初始化（复制 init-kit/ 目录结构）
   └─ 已有 .obsidian/ → Obsidian 注入模式（合并目录，不覆盖已有文件）

2. 写入 .wiki-root 标记文件

3. 创建目录结构（从 init-kit/ 复制骨架）

4. pip install -r <skill>/scripts/requirements.txt

5. 写入 .claude/settings.local.json：
   - PostToolUse hooks：BM25 实时索引 + graph 30s debounce
   - 过滤规则：wiki/**/*.md（排除 .claude/）

6. 输出完成提示
```

**关键简化**：init 只创建空 `_schema/` 和 `templates/` 目录，不复制文件。命令读取时分层覆盖——skill 内默认为默认值，用户目录下同名文件为可选覆盖。不存在 `_memory/` 目录。

## 7. 脚本清单

### 7.1 保留 + 改动

| 脚本 | 改动量 | 内容 |
|------|--------|------|
| `wiki_utils.py` | 中 | 路径常量在 import 时通过 `discover_wiki_root()` 计算；新增 `SKILL_DIR` |
| `wiki.sh` | 中 | `VAULT_DIR` 改用 CWD + `.wiki-root` 发现；`SCRIPT_DIR` 指向 skill 内 scripts/ |
| `bm25_index.py` | 小 | 导入新路径（模块级常量，兼容现有 import 风格） |
| `search_wiki.py` | 小 | 同上 |
| `build_graph.py` | 小 | 同上；移除 `--full` 模式 |
| `build_maps.py` | 小 | 同上；新增冷启动检测（wiki 页面 < 20 → 跳过，输出 `{"status": "skipped", "reason": "insufficient pages"}`） |
| `build_keywords.py` | 小 | 同上 |
| `build_ingest_context.py` | 小 | 同上；SCHEMA_DIR 和 TEMPLATE_PATH 分层覆盖（用户覆盖优先，fallback 到 skill 默认） |
| `lint_wiki.py` | 小 | 同上；WIKI_SUBDIRS 改为 `["entities", "concepts", "syntheses"]` |
| `snapshot_index.py` | 小 | 同上；TYPE_SECTIONS 去掉 qa-insight |
| `relink.py` | 小 | 同上；WIKI_SUBDIRS 改为 `["entities", "concepts", "syntheses"]` |
| `qwen_ingest.py` | 小 | `scan_existing_pages()` 不再从 `__file__` 推导 wiki 路径，改用 `discover_wiki_root()`；`DASHSCOPE_API_KEY` 不变 |
| `ingest_loop.py` | **新增** | 扫描 raw/，维护 `raw/.ingest-state.json`（hash 追踪 SHA256 前 16 位）。断点续传：自动补扫新文件、跳过已删除文件、失败重试 1 次后标记 failed。末尾自动触发 relink。支持 `--engine=qwen` |

### 7.2 删除

| 脚本 | 原因 |
|------|------|
| `build_wiki_pages.py` | 静态 HTML 生成，不纳入 skill |
| `build_statistics.py` | 统计 JSON，不纳入 skill |
| `build_raw_wiki_map.py` | raw→wiki 映射，项目特定需求 |
| `reclassify_raw.py` | raw/ 重组，项目特定需求 |
| `split_chat_json.py` | 拆分逻辑合并到 ingest 的 Q&A 模式 |
| `setup-ingest-loop.sh` | ralph-loop 特定，由 ingest_loop.py 替代 |
| `setup-ingest-loop-qwen.sh` | 同上 |
| `cron-setup.sh` | 由自适应自动化替代 |
| `watch-raw.sh` | 由自适应自动化替代 |

### 7.3 Hook 配置

Hook 脚本位于 `scripts/hooks/`（轻量 shell，3-5 行），init 时写入 `.claude/settings.local.json` 的绝对路径：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash /absolute/path/to/skill/scripts/hooks/bm25.sh"
          },
          {
            "type": "command",
            "command": "bash /absolute/path/to/skill/scripts/hooks/graph.sh"
          }
        ]
      }
    ]
  }
}
```

仅 BM25（搜索正确性）和 graph（30s debounce）。lint 和 keywords 在 maintain 中全量运行。

## 8. Wiki 页面生命周期

去掉 `_memory/` 目录后，知识页面的记忆状态嵌入其自身 frontmatter：

```yaml
---
type: entity | concept | synthesis
status: draft | active | stale | archived
confidence: 0.0-1.0
decay_rate: slow | medium | fast
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_accessed: YYYY-MM-DD
source_count: N
tags: []
aliases: []
relates_to: []
---
```

**生命周期转换**（在 review 命令中执行）：

```
draft ──(confidence >= 0.5)──→ active
active ──(confidence < 0.3)──→ stale
stale ──(30天未更新)─────────→ archived
any ────(用户手动)───────────→ archived
```

**Ebbinghaus 衰减**（review 步骤 6）：
- slow（半衰期 180 天）：架构决策、核心概念
- medium（半衰期 60 天）：一般事实
- fast（半衰期 14 天）：临时观察
- confidence < 0.3 → `status: stale`

衰减参数可在 `_schema/preferences.md` 中覆盖。

## 9. Journal 系统

三类入口（daily / reflection / judgment），模板中英双语化。两项增强：

### 9.1 !insight 直接录入

用户在 journal 中标记 `!insight`，review 扫描后直接路由到 ingest 逻辑：

```
今天意识到：条件数描述了问题本身的属性，而算法稳定性
描述了求解过程的属性。两者正交——一个良态问题可以用
不稳定算法求错，反之亦然。 !insight
```

→ review 检测到 → 创建 `wiki/concepts/条件数与算法稳定性的正交关系.md`

### 9.2 Journal → Wiki 链接扫描

review 扫描近期 journal 中的 `[[wiki链接]]`。某页面 3+ 天在 journal 中被引用 + `confidence < 0.5` → 提议用户将观察结晶化到对应 wiki 页面。

## 10. 命名约定

- wiki/ 三个子目录：`entities/`、`concepts/`、`syntheses/`（原 `qa-insights/` 合并到 syntheses）
- 文件名用自然中文
- `[[双链]]` 语法
- 关系类型和实体类型定义沿用现有 schema
- `maps/` 从 `topic-to-wiki.json` 由 `build_maps.py` 生成，不手动维护
- topic 聚类冷启动阈值：wiki 页面 < 20 时跳过

## 11. 模板/Schema 分层覆盖

```
读取优先级（所有命令统一）：
1. <wiki-root>/_schema/xxx.md     （用户覆盖版，可选）
2. <skill>/schemas/xxx.md          （skill 默认版，始终存在）

1. <wiki-root>/templates/xxx.md   （用户覆盖版，可选）
2. <skill>/templates/xxx.md        （skill 默认版，始终存在）
```

`build_ingest_context.py` 的 `build_compact_schema()` 和 `build_template()` 按此优先级读取。

## 12. 系统反馈回路

| 检测点 | 触发 | 阈值 | 动作 |
|--------|------|------|------|
| maintain 过期 | review 步骤 0 | 距上次 maintain > 7 天 | 提醒用户执行 maintain |
| wiki 页面增长 | review 步骤 0 | 页面数 - 快照数 > 20 | 提醒用户执行 maintain |
| topic 聚类就绪 | maintain 步骤 3 | wiki 页面 >= 20 | 自动触发 maps 生成 |
| !insight 积压 | review 步骤 5 | journal 中存在未处理的 !insight | 自动处理 |
| stale 页面 | review 步骤 6 | confidence < 0.3 | 标记 stale |
| 自适应提议 | review 步骤 7 | 连续 3 天同时间同操作 | 提议 cron 任务 |

## 13. 不兼容变更

- 命令前缀从 `/wiki:` 改为 `/llm-wiki:`
- `_memory/` 目录删除；记忆状态迁移到 wiki 页面 frontmatter
- `wiki/qa-insights/` 合并到 `wiki/syntheses/`
- wiki 子目录从 4 个减为 3 个
- 脚本路径从 `vault/scripts/` 变为 skill 内部路径（`<skill>/scripts/`）
- `build_graph.py` 不再支持 `--full` 模式
- Hook 脚本从 `vault/scripts/hook_*.sh` 迁移到 `<skill>/scripts/hooks/*.sh`
- `ingest` 命令合并了 `convert-to-markdown` 和 `qa-import` 的功能
- `check`、`lint`、`relink`、`reindex`、`build` 不再作为独立命令暴露
- `crystallize` 和 `consolidate` 合并到 `review`
- `relink` 从 maintain 移至 ingest-loop 末尾（maintain 中保留为保险步骤）
- Cron 任务从硬编码变为自适应提议
