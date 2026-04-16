# Wiki Guidelines 虚拟分区设计

**Date:** 2026-04-16
**Status:** Approved
**Approach:** Plan B — Virtual Partition (不移动文件，拆分 index → guidelines)

## Problem

wiki/ 下 concepts (269) + entities (182) 持续增长，导致多个痛点叠加：
1. `build_ingest_context.py` 生成的 existing_pages 列表过长，撑大子代理上下文
2. `index.md` 452 条完整清单被多个命令读入 prompt，占用过多 token
3. `relink`/`lint`/`reindex` 全目录扫描速度下降

## Decision

采用虚拟分区：文件保持 flat 目录不动，新增 `guidelines/` 目录作为面向 LLM 的按主题分片索引。

**不采用物理子文件夹的理由：**
- 主题边界不稳定（maps 聚类随 wiki 增长变化），物理移动文件代价过高
- 451 个文件路径变化产生大量 git diff
- 所有脚本和命令文档需要更新 ~20 处硬编码路径

## Architecture

### 数据流

```
wiki:reindex
    │
    ▼
topic-to-wiki.json (权威数据源)
    │
    ├──→ maps/*.md        (面向脚本/自动化，不变)
    ├──→ guidelines/*.md  (新增：面向 LLM prompt)
    └──→ index.md         (瘦身：统计表 + 全局名称表)
```

### 职责分界

| 维度 | maps/*.md | guidelines/*.md |
|------|-----------|-----------------|
| 用途 | 面向脚本/自动化的聚类产物 | 面向命令 prompt 的上下文包 |
| 内容 | 完整页面清单 + confidence 分数 | 页面清单 + 集群概述 |
| 消费者 | reindex, build_statistics.py | ingest, query, build_ingest_context.py |
| 生成时机 | wiki:reindex 时重建 | wiki:reindex 结束后从 topic-to-wiki.json 派生 |
| 格式优化 | 结构化，方便脚本解析 | 紧凑，优化 token 消耗 |

**关键原则：** `topic-to-wiki.json` 是 source of truth，maps 和 guidelines 都是它的衍生物。

## File Formats

### guideline.md

```markdown
---
type: guideline
topic: AI
page_count: 72
updated: 2026-04-16
---

## 概述

AI 工程、Agent 架构、LLM 工具链相关概念与实体的集群。
核心主题：上下文工程、多Agent协作、检索增强生成、注意力机制。

## 概念 (45)

- [[Context-Engineering]] — 上下文工程 (0.85)
- [[检索增强生成]] — RAG 架构 (0.90)
- ...

## 实体 (27)

- [[Anthropic]] — AI 安全公司 (0.88)
- ...
```

- frontmatter 带 `type: guideline`
- 概述段 ≤100 字，由 reindex 从 maps 内容提炼
- 页面清单可按需裁剪（仅 active 状态页面）

### index.md (瘦身后)

```markdown
---
type: index
updated: 2026-04-16
---

本文件由 LLM 自动维护。详细清单见各 guidelines/*.md。

## 统计

| 主题 | 概念 | 实体 | 合计 | guideline |
|------|------|------|------|-----------|
| AI | 45 | 27 | 72 | [[guidelines/AI]] |
| 方法论 | 30 | 11 | 41 | [[guidelines/方法论]] |
| 其他 | 100 | 43 | 143 | [[guidelines/其他]] |
| ... | ... | ... | ... | ... |

总计: 452 页 (264 概念, 180 实体, 5 综合, 3 QA)

## 全部页面

Context-Engineering, 检索增强生成, Anthropic, ...
```

从 ~450 行压缩到 ~20 行 + 全局名称表（~2KB 逗号分隔）。

## Command Changes

| 命令 | 改造内容 |
|------|----------|
| `wiki:ingest` | 去重时不再读完整 index.md，改为：读 index.md 名称表快速去重 + 读对应主题 guideline 获取上下文 |
| `wiki:ingest-loop` | 子代理 `build_ingest_context.py` 接受 `--topic` 参数，只输出该主题的 existing_pages |
| `wiki:query` | 先读 index.md 定位相关主题 → 只加载相关 guideline(s) → BM25 搜索 |
| `wiki:reindex` | 末尾新增步骤：从 topic-to-wiki.json 生成 guidelines/*.md + 重建精简 index.md |
| `wiki:check` / `wiki:lint` | 新增检查项：guideline 与 topic-to-wiki.json 一致性 |
| `wiki:maintain` | 流程不变，reindex 阶段自动覆盖 guideline 生成 |

## Script Changes

| 文件 | 改动 |
|------|------|
| `snapshot_index.py` | 新增 `--guidelines` 模式：生成 guidelines/*.md + 精简 index.md |
| `build_ingest_context.py` | 接受 `--topic AI` 参数，只输出该主题的 existing_pages |
| `wiki_utils.py` | 新增 `GUIDELINES_DIR = "guidelines"` 常量，`WIKI_SUBDIRS` 不变 |
| `relink.py` | 无需改动（递归扫描 wiki/） |
| `build_graph.py` | 无需改动（递归遍历 wiki/） |
| `build_wiki_pages.py` | 无需改动（递归遍历） |
| `lint_wiki.py` | 无需改动（逐文件检查） |
| Hook 脚本 | 无需改动（只检查 `wiki/` 前缀） |

## Ingest Context Reduction

**Before:**
```
build_ingest_context.py → existing_pages: 全部 452 条 → 子代理 prompt
```

**After:**
```
1. 主代理读 index.md 统计表 → 判断源材料属于哪个主题（如 "AI"）
2. build_ingest_context.py --topic AI → existing_pages: 仅 72 条
3. 子代理 prompt 从 ~452 条缩减到 ~72 条
```

跨主题源材料：传 `--topic AI,方法论` 合并多个 guideline。

## Risks & Mitigations

| 风险 | 应对 |
|------|------|
| "其他" 集群太大（143 页） | 如果占总量 >30%，在 reindex 时对 "其他" 做二级拆分 |
| 主题边界漂移 | guideline 重新生成即可，无需移文件 |
| 跨主题去重遗漏 | index.md 保留全局页面名称列表（逗号分隔，~2KB） |
| guidelines/ 在 Obsidian 中可见 | 放在 `wiki/guidelines/` 下，与 maps/ 同级。作为自动生成产物，Obsidian 可正常浏览但不需手动编辑 |
| 首次生成 | 需一次 `wiki:reindex` 生成全部 guideline |

## No Changes Required

- Obsidian 配置（`newLinkFormat: "shortest"` 天然兼容）
- Hook 脚本（只检查 `wiki/` 前缀，路径无关）
- `build_graph.py`, `build_wiki_pages.py`, `lint_wiki.py`（递归遍历）
- 现有 `[[wikilink]]` 引用（shortest 模式自动解析）

## Success Criteria

1. index.md 从 ~450 行降至 ~20 行 + 名称表
2. ingest 子代理上下文中 existing_pages 从 452 条降至目标主题的 ~70 条
3. 所有现有命令正常工作（wiki:maintain 全流程通过）
4. Obsidian 中 [[wikilink]] 跳转不受影响
5. guidelines/*.md 由 wiki:reindex 自动生成和维护
