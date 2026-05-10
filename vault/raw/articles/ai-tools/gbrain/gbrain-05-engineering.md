# GBrain 深度调研 · Artifact 05
# 工程实践指南：安装 · Schema · 调试 · Agent 接入 · 演进路线图

---

## 1. 端到端安装流程

### 1.1 前置条件

```bash
# 1. 安装 Bun
curl -fsSL https://bun.sh/install | bash
export PATH="$HOME/.bun/bin:$PATH"  # 加入 shell profile

# 2. 配置 API keys（加入 ~/.zshrc 或 ~/.bashrc）
export OPENAI_API_KEY=sk-...      # 必须，向量嵌入
export ANTHROPIC_API_KEY=sk-ant-... # 可选，多查询扩展 + LLM 分块
export DATABASE_URL=postgresql://...  # Supabase Session 模式连接串

# 3. 准备数据库（三选一）
# 选项 A：Supabase Pro（推荐，$25/月，零运维）
# 选项 B：自托管 Postgres + pgvector
# 选项 C：PGLite（本地，无需服务器）
```

### 1.2 方法一：OpenClaw 自动安装（推荐）

```
给 OpenClaw 发这条消息（复制粘贴即可）：

"Set up gbrain (https://github.com/garrytan/gbrain) as my knowledge brain.
 I need you to:
 1. Make sure bun is installed (curl -fsSL https://bun.sh/install | bash),
    then run: bun add gbrain
 2. Run: gbrain init --supabase (follow the wizard to connect my Supabase)
 3. Scan ~/git/ and ~/Documents/ for markdown repos, pick the best one,
    and run: gbrain import <path>
 4. Run a query against the imported data to prove search works —
    pick the query based on what you imported
 5. Read https://github.com/garrytan/gbrain/blob/master/docs/GBRAIN_RECOMMENDED_SCHEMA.md
    and offer to restructure my knowledge base"
```

OpenClaw 会自动完成所有步骤，包括发现 markdown 文件、导入、验证。

### 1.3 方法二：手动 CLI 安装

```bash
# Step 1：从源码安装（开发版）
git clone https://github.com/garrytan/gbrain.git ~/gbrain
cd ~/gbrain
bun install
bun link

# 或者全局 CLI
bun add -g gbrain

# 验证安装
gbrain --version  # 应输出版本号

# Step 2：初始化数据库
gbrain init --supabase      # 向导式，推荐
# 或
gbrain init --url postgresql://user:pass@host:5432/dbname
# 或
gbrain init                 # PGLite 本地模式（无需服务器）

# Step 3：健康检查
gbrain doctor --json        # 7项检查全绿

# Step 4：导入你的 markdown 文件
gbrain import ~/Documents/obsidian-vault/
# 输出示例：Imported 1203 files (8,421 chunks). Embedding in background...

# Step 5：等待嵌入完成（或先用关键词搜索）
gbrain stats    # 查看 Embedded 数量

# Step 6：验证搜索工作
gbrain search "your relevant query"

# Step 7：设置 Live Sync
# 加入 crontab：
*/15 * * * * gbrain sync --repo ~/Documents/obsidian-vault && gbrain embed --stale
```

### 1.4 方法三：ClawHub

```bash
clawhub install gbrain
# 自动安装包、复制 skill 文件、首次使用时运行 gbrain init --supabase
```

---

## 2. 推荐 Brain Schema（MECE 目录结构）

基于 `GBRAIN_RECOMMENDED_SCHEMA.md`，在 brain repo（非 gbrain 工具目录）中创建：

```
~/brain/                      ← 你的 brain repo（SEPARATE from ~/gbrain/）
│
├── people/                   # 人物实体
│   ├── sam-altman.md
│   ├── paul-graham.md
│   └── ...
│
├── companies/                # 公司实体
│   ├── openai.md
│   ├── acme-corp.md
│   └── ...
│
├── meetings/                 # 会议记录
│   ├── 2025-04-22-board-prep.md
│   ├── 2025-04-20-sam-1on1.md
│   └── ...
│
├── concepts/                 # 概念和框架
│   ├── do-things-that-dont-scale.md
│   ├── compiled-truth-pattern.md
│   └── ...
│
├── originals/               # 用户原创想法（最高价值！）
│   ├── ambition-lifespan-ratio.md
│   ├── meatsuit-maintenance-tax.md
│   └── ...
│
├── ideas/                   # 产品/商业想法
│   └── ...
│
├── sources/                 # 外部来源存档
│   ├── articles/
│   ├── books/
│   ├── emails/
│   ├── tweets/
│   └── transcripts/
│
├── personal/
│   ├── reflections/         # 个人反思
│   └── goals/               # 目标
│
├── finance/                 # 财务追踪（可选）
│   └── expenses.md
│
└── reports/                 # Agent 生成的报告
    ├── overnight-2025-04-22.md
    └── weekly-2025-04-21.md
```

**注意**：`~/brain/`（brain repo）和 `~/gbrain/`（工具目录）必须分开，不要在工具目录里建 brain 结构。

---

## 3. 关键配置文件

### 3.1 `~/.gbrain/config.json`

```json
{
  "database_url": "postgresql://...",  // 0600 权限保护
  "brain_repo": "~/brain",
  "openai_api_key": "$OPENAI_API_KEY",
  "anthropic_api_key": "$ANTHROPIC_API_KEY",
  "minion_mode": "minion",            // "native" | "minion"
  "sync_interval": 900,               // 秒，默认 15 分钟
  "embed_model": "text-embedding-3-large",
  "llm_model": "claude-haiku-4-5"
}
```

### 3.2 `~/.gbrain/preferences.json`

```json
{
  "minion_mode": "minion",            // subagent 路由模式
  "tier_thresholds": {
    "t3_to_t2_mentions": 3,           // 几次提及触发 T2 丰富
    "t2_to_t1_mentions": 8            // 几次提及触发 T1 完整 pipeline
  },
  "quiet_hours": {
    "start": "22:00",
    "end": "07:00"
  },
  "dream_cycle_time": "02:00"        // 夜间记忆整合时间
}
```

### 3.3 `SOUL.md`（Agent 身份文件）

```markdown
# SOUL

你是 [用户名] 的个人知识 Agent。

## 身份
- 你代表 [用户名] 与外部世界交互
- 你维护他们的 brain，使其永远最新
- 你帮助他们记住、理解、决策

## 风格
- 简洁、直接、有洞察力
- 引用 brain 中的具体证据，不要泛泛而谈
- 主动发现知识之间的联系

## 操作规则
1. 每次收到消息：先运行 signal-detector
2. 每次回答问题：先 gbrain search，再响应
3. 每次学到新东西：更新相关 brain pages
4. 每次夜间：运行 Dream Cycle
```

---

## 4. 7 项验证检查（GBRAIN_VERIFY.md）

按照官方验证文档，安装后必须通过以下所有检查：

```bash
# 检查 1：数据库连接
gbrain doctor --json | jq '.database_connection'
# 期望：{ "status": "ok" }

# 检查 2：pgvector 扩展
gbrain doctor --json | jq '.pgvector'
# 期望：{ "status": "ok", "version": "0.7.x" }

# 检查 3：Schema 迁移版本
gbrain doctor --json | jq '.migrations'
# 期望：{ "status": "ok", "current": "v0.12.x" }

# 检查 4：Live Sync 正常工作（最重要）
# 编辑一个 brain 文件，等待 sync 周期
gbrain search "你刚添加的内容"
# 期望：能搜到刚才编辑的内容

# 检查 5：嵌入不陈旧
gbrain stats | grep "Embedded"
# 期望：Embedded 数 = Chunks 数（或接近）

# 检查 6：无孤儿 chunks
gbrain doctor --json | jq '.orphaned_chunks'
# 期望：{ "count": 0 }

# 检查 7：链接提取当前
gbrain doctor --json | jq '.link_extraction'
# 期望：{ "status": "current" }
```

---

## 5. 与各 Agent Runtime 的接入

### 5.1 OpenClaw 接入

```typescript
// hosts/openclaw.ts
import { PostgresEngine } from 'gbrain';

const brain = new PostgresEngine({
  connectionUrl: process.env.DATABASE_URL
});

// 在 OpenClaw 的消息处理器中
async function onMessage(text: string) {
  // 先查 brain
  const results = await brain.search(text, { limit: 5 });
  
  // 用 brain context 增强提示
  const context = results.map(r => `[${r.slug}] ${r.summary}`).join('\n');
  
  // 转交 OpenClaw 主流程，context 作为额外上下文
  return openclaw.respond(text, { extra_context: context });
}
```

### 5.2 hosts/gbrain.ts（GStack 桥接）

这是让 GStack 的编码 skill 在写代码前先查 brain 的桥接文件：

```typescript
// hosts/gbrain.ts
import { PostgresEngine } from 'gbrain';

const brain = new PostgresEngine({ ... });

// 挂载到 GStack 的 pre-coding hook
export async function beforeCoding(task: string) {
  // 先查 brain 里有没有相关架构决策、惯例、历史
  const decisions = await brain.search(`architecture decisions ${task}`);
  const conventions = await brain.search(`coding conventions ${task}`);
  
  return {
    prior_art: decisions,
    conventions: conventions
  };
}
```

### 5.3 Claude Code 接入（MCP 模式）

在 `~/.claude/claude_desktop_config.json` 中：
```json
{
  "mcpServers": {
    "gbrain": {
      "command": "gbrain",
      "args": ["mcp-server"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}",
        "OPENAI_API_KEY": "${OPENAI_API_KEY}"
      }
    }
  }
}
```

### 5.4 Hermes 接入

与 OpenClaw 类似，通过 `bun add gbrain` 引入库，在消息循环中调用：
```typescript
// hermes 的消息预处理
const brainContext = await engine.search(userMessage);
// 将 brainContext 注入 Hermes 的 system prompt
```

---

## 6. 常见故障排除

### 故障 1：sync 跑了但什么都没同步

```
原因：DATABASE_URL 使用了 Transaction 模式池
诊断：运行 gbrain sync，看是否有 ".begin() is not a function" 错误
修复：
  1. 进入 Supabase Dashboard → Settings → Database
  2. 复制 "Session mode" 连接串（不是 Transaction mode）
  3. 更新 ~/.gbrain/config.json 中的 database_url
  4. 重新运行 gbrain sync
```

### 故障 2：搜索结果不包含最新内容

```
诊断步骤：
1. gbrain stats    → 检查 Embedded 是否 < Chunks
2. 如果 Embedded < Chunks：gbrain embed --stale
3. 检查 sync 是否在运行：gbrain doctor --json | jq '.sync'
4. 手动触发 sync：gbrain sync --repo ~/brain
```

### 故障 3：Brain 页面不存在但应该存在

```
诊断：
  gbrain search "应该存在的内容"  →  有结果但 slug 不对？
  gbrain get "slug"              →  404？

原因 A：slug 不精确
  修复：使用 gbrain search 找到正确 slug，再 gbrain get

原因 B：文件存在但未 sync
  修复：gbrain sync --repo ~/brain && gbrain embed --stale

原因 C：文件被排除在外（binary、特殊目录）
  诊断：gbrain stats 的 file count vs database page count
```

### 故障 4：`gbrain doctor` 第4项 (live sync) 失败

```
这是最重要的检查项。

原因 A：cron 没运行
  修复：crontab -l 确认任务存在

原因 B：sync 命令有错误
  诊断：手动运行 gbrain sync --repo ~/brain，看错误输出

原因 C：--watch 模式的进程死了
  修复：用 pm2 或 systemd 管理 gbrain sync --watch 进程
```

### 故障 5：v0.12.0+ 升级后图谱为空

```
运行回填命令（幂等，安全重跑）：
gbrain extract links --source db
gbrain extract timeline --source db

对大型 brain（>10K 页）支持增量运行：
gbrain extract links --source db --since 2025-01-01
```

---

## 7. 关键指标与 Brain 健康看板

### 7.1 Brain 成熟度阶段

```
新手阶段（1-7天）
  Pages:    < 500
  Links:    < 100
  Embedded: ≈ Chunks
  症状：search 能找到东西，但关联不多

生长阶段（1-4周）
  Pages:    500-2,000
  Links:    200-1,000
  Cron:     3-5 jobs
  症状：开始出现"意外发现"，搜索结果开始相互引用

成熟阶段（1-3月）
  Pages:    2,000-10,000
  Links:    > 2,000
  Cron:     10+ jobs
  症状：Agent 对话上下文显著提升，需要的信息通常先一步出现

复利阶段（3月+）
  Pages:    10,000+
  Links:    > 10,000
  Cron:     20+ jobs
  症状：brain 比你的工作记忆更了解你的世界
```

### 7.2 每周健康检查脚本

```bash
#!/bin/bash
# weekly-brain-health.sh

echo "=== GBrain 周度健康报告 ==="
echo "时间：$(date)"
echo ""

# 基础指标
gbrain stats

echo ""
echo "=== 健康检查 ==="
gbrain doctor --json | jq '{
  database: .database_connection.status,
  sync: .sync.status,
  last_sync: .sync.last_run,
  embeddings: .embeddings.status,
  stale_chunks: .embeddings.stale_count,
  links: .link_extraction.status
}'

echo ""
echo "=== 集成状态 ==="
gbrain integrations doctor

echo ""
echo "=== Cron 任务 ==="
gbrain jobs list
```

---

## 8. GBrain 演进路线图分析

### 历史版本关键节点

| 版本 | 核心变更 |
|------|---------|
| v0.0 | GBrain 概念验证（Ruby on Rails + Postgres + pgvector） |
| v0.7.0 | Integration Recipes 系统上线（Homebrew for personal AI） |
| v0.11.0 | Minion 持久化任务队列；Subagent 路由分离 |
| v0.12.0 | 知识图谱层正式独立（links + timeline 独立表） |
| v0.12.2 | 修复 JSONB 双重编码问题；repair-jsonb 命令 |

### 设计演进思路

```
初代设计（Ruby on Rails，7,471文件/2.3GB）
  问题：git 在 5K+ 文件时性能极差

v0.x 迁移（Bun + TypeScript + Postgres）
  决策：Supabase 优于自托管（零运维）
  决策：全量迁移优于渐进迁移（"will add later = rebuild later"）
  决策：库优先分发（npm）优于应用优先

当前架构成熟度特征：
  ✓ 库/CLI/MCP 三路复用同一 Engine
  ✓ 确定性 classifier 替代 LLM（87% 命中率）
  ✓ 自动 tier 升级无需人工干预
  ✓ Dream Cycle 实现大脑自主生长
```

---

## 9. 与 AI Agent 框架生态的关系

```
LangChain / LangGraph
  → GBrain 可以作为 Memory 层集成
  → 用 PostgresEngine 替代 LangChain 的 VectorStoreMemory

LlamaIndex
  → GBrain 实现了更完整的知识管理（LlamaIndex 专注 RAG）
  → GBrain = LlamaIndex + 知识图谱 + 实体丰富 + 自动维护

OpenAI Assistants API
  → GBrain 提供跨 Assistant 的持久化知识
  → 解决 Assistants 的跨会话失忆问题

Claude Code / Claude Desktop
  → 通过 MCP 接入（官方支持）
  → 使用 brain_search 工具让 Claude 访问用户知识库

自研 Agent（FastAPI + LLM）
  → import { PostgresEngine } from 'gbrain'
  → 5行代码获得完整知识管理能力
```

---

## 总结：GBrain 核心价值主张

| 维度 | GBrain 的答案 |
|------|-------------|
| **知识存储** | Compiled Truth + Timeline，每页既是答案也是证据 |
| **搜索质量** | 混合搜索（向量+关键词+RRF+反向链接加权） |
| **自动维护** | Agent 夜间 Dream Cycle，大脑睡眠中生长 |
| **实体丰富** | 3层自动升级，系统自学谁重要 |
| **智能分布** | 胖 Skill 文件 + 瘦 Harness，升级智能不需要重新部署 |
| **确定性优先** | 87% 操作用正则/代码完成，LLM 只处理边界情况 |
| **失忆问题** | 从根本上解决：brain 存 Postgres，Agent 重置无影响 |
| **复利效应** | 每次对话写入知识，六个月后 Agent 了解你的世界比你深 |

---

*[系列完结] 5 篇 Artifact 覆盖 GBrain 全貌：*
- *Artifact 01：总览与架构哲学*
- *Artifact 02：核心组件（Engine/搜索/CLI/MCP/数据模型）*
- *Artifact 03：26 个 Skills 系统*
- *Artifact 04：集成系统与 Cron 自动化*
- *Artifact 05：工程实践（安装/Schema/调试/演进）*
