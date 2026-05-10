# GBrain 深度调研 · Artifact 02
# 核心组件深度解析

> 覆盖：PostgresEngine · 混合搜索引擎 · CLI 工具集 · MCP Server · 知识数据模型 · 实体丰富系统

---

## 1. PostgresEngine — 核心存储引擎

### 1.1 定位

GBrain 以**库优先**方式分发。`PostgresEngine` 是所有功能的核心类，CLI 和 MCP Server 都是它的薄包装。

```typescript
import { PostgresEngine } from 'gbrain';

const engine = new PostgresEngine({ connectionUrl: process.env.DATABASE_URL });
await engine.init();

// 导入文件
await engine.importDirectory('/path/to/brain/');

// 混合搜索
const results = await engine.search('biggest risks', { limit: 5 });

// 获取页面
const page = await engine.get('people/jane-chen');
```

### 1.2 数据库 Schema（核心表）

```sql
-- 页面主表
CREATE TABLE brain_pages (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug        TEXT UNIQUE NOT NULL,   -- 路径标识，如 people/jane-chen
  type        TEXT,                   -- person|company|concept|original|meeting
  title       TEXT,
  content     TEXT,                   -- 完整 markdown 内容
  content_hash TEXT,                 -- SHA-256，用于增量同步去重
  tags        TEXT[],
  created_at  TIMESTAMPTZ DEFAULT now(),
  updated_at  TIMESTAMPTZ DEFAULT now()
);

-- 分块表（用于向量搜索）
CREATE TABLE brain_chunks (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  page_id     UUID REFERENCES brain_pages(id),
  chunk_index INT,
  content     TEXT,
  embedding   VECTOR(3072),           -- text-embedding-3-large 维度
  tsvector_col TSVECTOR,              -- 全文搜索索引
  created_at  TIMESTAMPTZ DEFAULT now()
);

-- 知识图谱边表
CREATE TABLE brain_links (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_slug TEXT NOT NULL,
  target_slug TEXT NOT NULL,
  rel_type    TEXT,   -- attended|works_at|invested_in|founded|advises|etc.
  context     TEXT,   -- 链接来源的上下文摘要
  created_at  TIMESTAMPTZ DEFAULT now()
);

-- 时间轴事件表
CREATE TABLE brain_timeline (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug        TEXT NOT NULL,           -- 关联的 brain page
  event_date  DATE,
  event_text  TEXT,
  source_slug TEXT,                   -- 来源页面（反向引用）
  created_at  TIMESTAMPTZ DEFAULT now()
);
```

### 1.3 关键技术决策

| 决策 | 选择 | 原因 |
|------|------|------|
| tsvector 生成 | **触发器触发（非生成列）** | 支持 Supabase Transaction 模式池的限制 |
| pgvector 索引 | **HNSW** | 比 IVFFlat 召回率更高，查询更快 |
| 连接池 | Session 模式（端口 6543）| Transaction 模式会导致 `.begin()` 错误 |
| 内容去重 | SHA-256 内容哈希 | 重跑 import 不会重复导入未变更文件 |
| slug 解析 | 写入用精确 slug；读取支持 pg_trgm 模糊匹配 | 兼顾数据完整性和使用便利性 |

---

## 2. 混合搜索引擎

### 2.1 搜索管道全流程

```
用户查询: "when should you ignore conventional wisdom?"
                        │
                        ▼
        ┌─── 多查询扩展（Claude Haiku）───┐
        │  "contrarian thinking startups" │
        │  "going against the crowd"      │
        │  "ignoring received wisdom"     │
        └────────────────────────────────┘
                        │
           ┌────────────┴────────────┐
           ▼                         ▼
     向量搜索                    关键词搜索
  (HNSW cosine                (tsvector +
   text-embedding-3-large)     ts_rank)
           │                         │
           └────────────┬────────────┘
                        ▼
              RRF（Reciprocal Rank Fusion）
                   分数融合
                        │
                        ▼
           反向链接加权提升（Backlink Boosting）
                        │
                        ▼
              Top-K 结果（默认 5 条）
              每条结果附带：slug、type、score、摘要
```

### 2.2 RRF 融合算法

```
RRF_score(d) = Σ 1 / (k + rank_i(d))

k = 60（经典值，防止高排名文档过度主导）
rank_i(d) = 文档 d 在搜索方法 i 中的排名
```

对每个查询的向量结果和关键词结果分别排名，然后用 RRF 合并，取最终 top-K。

### 2.3 反向链接加权

被多个页面链接到的页面，在搜索结果中得分更高。这类似于 PageRank：
- 高度被引用的人 → 更可能出现在相关搜索中
- 链接越多 = 系统认为越重要

### 2.4 三种搜索接口

```bash
# 1. 混合搜索（推荐）—— 向量 + 关键词 + RRF
gbrain search "competitive dynamics"

# 2. 直接获取（已知 slug）
gbrain get people/jane-chen

# 3. LLM 综合查询（多步推理，更慢更贵）
gbrain query "what have I said about the relationship between shame and founder performance?"
```

| 接口 | 场景 | 速度 | 成本 |
|------|------|------|------|
| `search` | 不确定 slug，语义查询 | 快 | 低 |
| `get` | 已知精确 slug | 极快 | 零 |
| `query` | 复杂多跳问题 | 慢 | 高 |

---

## 3. CLI 工具集完整参考

### 3.1 核心命令

```bash
# ── 初始化 ──────────────────────────────────
gbrain init --supabase         # 向导式 Supabase 初始化
gbrain init --url <pg_url>     # 连接任意 Postgres + pgvector

# ── 导入 ────────────────────────────────────
gbrain import <path>           # 导入目录（增量，SHA-256 去重）
gbrain import <path> --no-embed  # 跳过嵌入，快速导入
gbrain sync --repo <path>      # 增量同步（只处理变更文件）
gbrain sync --watch --repo <path>  # 前台轮询（每60秒）
gbrain embed --stale           # 补充嵌入所有未向量化的 chunk

# ── 搜索 ────────────────────────────────────
gbrain search "<query>"        # 混合搜索
gbrain get <slug>              # 直接获取页面
gbrain query "<question>"      # LLM 综合查询

# ── 写入 ────────────────────────────────────
gbrain put <slug> --content "..." # 写入/更新页面
gbrain put <slug> --file <path>   # 从文件写入

# ── 知识图谱 ─────────────────────────────────
gbrain extract links --source db   # 从现有 pages 提取所有链接
gbrain extract links --source db --dry-run  # 预览，不提交
gbrain extract timeline --source db  # 提取时间轴事件

# ── 集成 ────────────────────────────────────
gbrain integrations list       # 列出所有可用集成 recipes
gbrain integrations show <id>  # 查看某集成的详情
gbrain integrations doctor     # 健康检查所有已配置集成

# ── 运维 ────────────────────────────────────
gbrain stats                   # 页面数、chunks数、嵌入数、链接数
gbrain doctor --json           # 全面健康检查（7项）
gbrain check-update --json     # 检查版本更新（不自动更新）
gbrain post-upgrade            # 应用 schema 迁移后置工作
gbrain jobs                    # 查看所有 Minion 后台任务状态
gbrain files sync              # 将 binary 文件移至 Supabase Storage

# ── 调试 ────────────────────────────────────
gbrain repair-jsonb            # 修复 JSONB 列损坏（v0.12.2+ 后升级使用）
```

### 3.2 `gbrain stats` 输出示例

```
Pages:    342     ← 总页面数
Chunks:   1,847   ← 分块总数
Embedded: 1,847   ← 已向量化的 chunks（=Chunks 时搜索最优）
Links:    2,341   ← 知识图谱边数
Timeline: 891     ← 时间轴事件数
```

若 `Embedded < Chunks`：需运行 `gbrain embed --stale` 补充向量化。

### 3.3 `gbrain doctor` 7 项健康检查

```
[1] ✓ Database connection reachable
[2] ✓ pgvector extension enabled
[3] ✓ Schema migrations up to date
[4] ✓ Live sync working (last sync: 8 min ago)    ← 最重要！
[5] ✓ Embeddings not stale (0 chunks unembedded)
[6] ✓ No orphaned chunks
[7] ✓ Link extraction current
```

---

## 4. MCP Server

GBrain 暴露 MCP（Model Context Protocol）接口，使任何 MCP 客户端（Claude Desktop、OpenClaw 等）可以直接操作 brain。

```typescript
// MCP 工具暴露的核心操作
{
  "tools": [
    "brain_search",     // 混合搜索
    "brain_get",        // 获取指定 slug 页面
    "brain_put",        // 写入/更新页面
    "brain_query",      // LLM 综合查询
    "brain_stats",      // 获取 brain 统计信息
    "brain_link",       // 创建知识图谱链接
    "brain_timeline"    // 追加时间轴事件
  ]
}
```

MCP Server 与 CLI 使用完全相同的 `PostgresEngine`，保证 CLI/MCP 行为一致（有 drift tests 验证）。

---

## 5. 知识数据模型详解

### 5.1 Brain Page 类型系统

```
brain/
├── people/          # 人物页面
│   └── {slug}.md    # 如 people/sam-altman.md
├── companies/       # 公司页面
│   └── {slug}.md
├── meetings/        # 会议记录
│   └── YYYY-MM-DD-{title}.md
├── concepts/        # 概念/框架
│   └── {slug}.md    # 如 concepts/do-things-that-dont-scale.md
├── originals/       # 用户原创想法（最高价值）
│   └── {slug}.md
├── ideas/           # 产品/商业想法
│   └── {slug}.md
├── personal/
│   └── reflections/ # 个人反思
├── sources/         # 文章/书籍等外部源
│   └── {slug}.md
└── reports/         # Agent 生成的报告
    └── {date}-{title}.md
```

### 5.2 完整 Brain Page 示例（Person 类型）

```markdown
---
type: person
title: Jane Chen
tags: [strategy, vp, portfolio-company]
company: acme-corp
role: VP Strategy
tier: 1
---

## 编译真相

Jane Chen 是 Acme Corp 的 VP Strategy，2023年加入。她主导了
Q1 竞争分析项目，发布了评估竞争威胁的内部框架。在多个场合
表现出对定价策略的深度思考。我们有6个月的合作记录。

**关键背景**: 她在企业细分市场的定价压力问题上与我们有
直接分歧，值得在下次董事会准备时重点跟进。

**链接**: [[acme-corp]] | [[competitive-moats]] | [[board-prep-2025-03]]

---

## 时间轴

- **2023-06-15** | 加入 Acme Corp 担任 VP Strategy
- **2025-01-10** | 会议讨论 Q1 竞争分析 → [meeting/2025-01-10-q1-strategy]
- **2025-03-05** | 董事会准备会议中被提及 → [meetings/2025-03-board-prep]
- **2025-03-20** | 发布竞争威胁评估内部框架
```

### 5.3 实体丰富三层系统

```
提及一次 → Tier 3（存根页面）
       │
       ▼ 3次跨不同来源提及
Tier 2（Web + Social 丰富）
  → 自动调用 Crustdata / Happenstance / Exa 等 API
       │
       ▼ 有过会议 OR 8次以上提及
Tier 1（完整 pipeline 丰富）
  → 完整外部数据丰富 + 编译真相重写
```

大脑自动学习谁重要，无需手动指定。

---

## 6. 分块策略（3层分块）

```
文档输入
    │
    ▼
层1：结构化分块（Markdown headers）
    按 H1/H2/H3 分割，保持语义完整
    │
    ▼
层2：LLM 分块（Claude Haiku）
    对结构不清晰的段落，用 LLM 判断语义边界
    │
    ▼
层3：滑动窗口分块（固定长度 + 重叠）
    对超长段落的兜底策略
    │
    ▼
每块：文本 + SHA-256 哈希 + 向量嵌入 + tsvector
```

---

## 7. Brain vs Memory vs Session：三层分离

这是使用 GBrain 最关键的架构概念：

```python
on_new_information(info):
    if info.is_about_the_world:
        # GBRAIN：人、公司、交易、会议、概念、原创想法
        gbrain.put(slug, content)

    elif info.is_about_operations:
        # AGENT MEMORY：偏好、决策、工具配置、会话连续性
        memory.write(info)

    elif info.is_current_conversation:
        # SESSION CONTEXT：当前会话内容
        # 不持久化，随对话消失
        pass
```

| 层 | 存储什么 | 持久化 | 示例 |
|----|---------|--------|------|
| **GBrain** | 世界知识 | 是（Postgres） | "Pedro 是 Brex CEO" |
| **Agent Memory** | 操作状态 | 部分（取决于平台） | "用户偏好简洁格式" |
| **Session Context** | 当前对话 | 否 | "用户刚说了什么" |

**关键验证测试**：
```bash
# 正确：Agent 重置后 GBrain 知识依然存在
gbrain get people/pedro

# 错误信号：在 brain 里找到操作偏好
gbrain search "user prefers"  # 应该返回空
```

---

*下一篇：[Artifact 03 - GBrain Skills 系统]*
