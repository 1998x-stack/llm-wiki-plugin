# Hermes Agent 深度解析 · 第三篇：分层记忆系统

> **系列导读**：记忆是 Hermes 区别于无状态 Agent 的核心能力之一。本篇系统讲解 Hermes 的四层记忆体系：语义记忆（MEMORY.md）、用户模型（USER.md）、情节记忆（FTS5 跨会话召回）、辩证用户建模（Honcho），以及"冻结快照"这一关键设计决策。

---

## 一、为什么需要记忆系统？

想象两种助手：

**助手 A（无状态）：**
- 每次告诉它："我用 macOS，喜欢简洁的回答，项目在 ~/code/api"
- 每次重新建立上下文
- 下次仍需重复

**助手 B（有记忆）：**
- 第一次告诉它，它记下来
- 之后直接问："帮我看看 API 的性能问题"
- 它自动知道在哪、你的习惯、环境配置

Hermes 是助手 B。但它不只是简单地"记几条笔记"，而是构建了一个**四层分级记忆体系**，每一层解决不同的记忆问题。

---

## 二、四层记忆体系全景

```
┌─────────────────────────────────────────────────────────────┐
│                   Hermes 记忆体系                             │
│                                                             │
│  Layer 1: MEMORY.md          语义记忆（环境/项目/学到的）      │
│           ~2,200 chars       始终注入 System Prompt           │
│                                                             │
│  Layer 2: USER.md            用户模型（偏好/风格/身份）        │
│           ~1,375 chars       始终注入 System Prompt           │
│                                                             │
│  Layer 3: SQLite FTS5        情节记忆（历史对话全文检索）      │
│           无上限              按需召回（工具调用触发）          │
│                                                             │
│  Layer 4: Honcho             辩证用户建模（深度用户认知）      │
│           honcho-ai 包        跨会话动态更新                   │
└─────────────────────────────────────────────────────────────┘
```

每一层的访问方式和 Token 成本不同，共同构成从"快速事实"到"深度理解"的记忆梯度。

---

## 三、Layer 1：MEMORY.md —— Agent 的语义记忆

### 定位

MEMORY.md 是 Agent 的**个人笔记本**，存储关于工作环境的客观事实：

- 运行环境（OS、已安装工具、Docker 设置）
- 项目约定（代码风格、构建命令、CI 配置）
- 学到的工具技巧（某 SSH 端口特殊、某命令需要 sudo）
- 已完成的重要任务记录（数据库迁移日期等）
- 反复纠正的错误（"不要用 sudo 执行 Docker 命令，用户已在 docker 组"）

### 存储规格

| 属性 | 值 |
|---|---|
| 文件路径 | `~/.hermes/memories/MEMORY.md` |
| 字符上限 | 2,200 chars（约 800 tokens） |
| 典型条目数 | 8-15 条 |
| 注入方式 | 会话开始时冻结快照，注入 System Prompt |

### System Prompt 中的呈现格式

```
══════════════════════════════════════════════
MEMORY (your personal notes) [67% — 1,474/2,200 chars]
══════════════════════════════════════════════
User runs macOS 14 Sonoma, Homebrew, Docker Desktop and Podman. Shell: zsh+oh-my-zsh. Editor: VS Code with Vim keybindings.
§
Project ~/code/api uses Go 1.22, sqlc for DB queries, chi router. Run tests with 'make test'. CI via GitHub Actions.
§
Staging server (10.0.1.50) needs SSH port 2222, not 22. Key at ~/.ssh/staging_ed25519.
§
User prefers concise responses without lengthy explanations. Show code first, explain after if needed.
```

**格式细节：**
- 标题行：显示用量百分比和字符数，让 Agent 知道剩余空间
- 条目分隔符：`§`（节符，避免与内容冲突）
- 条目支持多行

### 记忆操作：`memory` 工具

Agent 通过 `memory` 工具管理 MEMORY.md，支持三种操作：

**添加新条目**
```json
{
  "action": "add",
  "target": "memory",
  "content": "Project uses Poetry for dependency management, not pip directly."
}
```

**替换现有条目**（子字符串匹配，无需完整内容）
```json
{
  "action": "replace",
  "target": "memory",
  "old_text": "SSH port 2222",
  "content": "Staging server (10.0.1.50) needs SSH port 2222. Key at ~/.ssh/staging_ed25519. Dev server uses port 22."
}
```

**删除过期条目**
```json
{
  "action": "remove",
  "target": "memory",
  "old_text": "Completed migration to PostgreSQL on 2026-01-15"
}
```

**为什么用子字符串匹配？**  
完整条目可能经过多次修改，原始内容不再准确。子字符串匹配只需提供唯一标识片段，更鲁棒。如果子字符串匹配到多条，会返回错误要求更精确。

### 自动触发 vs 手动触发

Agent **自动**在以下情况保存记忆（不需要你提醒）：
- 发现新的环境事实
- 学到项目约定或工具用法
- 被用户纠正某个做法
- 完成重要的里程碑任务

你也可以**显式要求**：
- "记住我的 API 密钥每月轮换"
- "把这个项目的构建流程记下来"

---

## 四、Layer 2：USER.md —— 用户模型档案

### 定位

USER.md 存储关于**你**的信息，而非关于环境的信息：

- 身份：姓名、职位、时区
- 沟通偏好：详细 vs 简洁、喜欢代码先行还是解释先行
- 技术水平：初学者 / 中级 / 专家
- 工作习惯：喜欢分步骤 vs 直接给结论
- 禁忌：不喜欢的表达方式、需要避免的假设

### 存储规格

| 属性 | 值 |
|---|---|
| 文件路径 | `~/.hermes/memories/USER.md` |
| 字符上限 | 1,375 chars（约 500 tokens） |
| 典型条目数 | 5-10 条 |
| 注入方式 | 与 MEMORY.md 相同，冻结快照 |

### System Prompt 中的呈现格式

```
══════════════════════════════════════════════
USER PROFILE [45% — 619/1,375 chars]
══════════════════════════════════════════════
Name: XM. Senior AI Engineer at TapTap Maker (XD Inc.). Timezone: Asia/Shanghai.
§
Prefers Chinese-language documentation and markdown artifacts as primary deliverables.
§
Expert-level Python and ML background. Skip basic explanations of standard library or common patterns.
§
Prefers exhaustive, production-ready implementations over demos. Always include type annotations.
§
Communication style: direct, technical. No filler phrases.
```

### MEMORY.md vs USER.md：怎么区分？

| 问自己 | 存哪里 |
|---|---|
| 这是关于**运行环境**的事实吗？ | MEMORY.md |
| 这是关于**我这个人**的信息吗？ | USER.md |
| "项目用 Poetry 管理依赖" | MEMORY.md ✅ |
| "用户讨厌啰嗦的解释" | USER.md ✅ |
| "用户的 Go 水平是专家级" | USER.md ✅ |
| "服务器在 10.0.1.50" | MEMORY.md ✅ |

---

## 五、冻结快照模式（Frozen Snapshot Pattern）

这是 Hermes 记忆系统最重要的设计决策，也是最容易被误解的地方。

### 行为描述

```
会话开始
   ↓
从磁盘加载 MEMORY.md + USER.md
   ↓
渲染为文本，注入 System Prompt（此后不再改变）
   ↓
会话进行中
   ↓
Agent 调用 memory 工具添加/修改记忆
   ↓
立即写入磁盘 ✅
但不更新 System Prompt ❌（本次会话内不可见）
   ↓
会话结束
   ↓
下次会话开始时，新记忆才进入 System Prompt
```

### 为什么这样设计？

**答案：保护 LLM 的 KV Cache（前缀缓存）。**

LLM 的计算成本与输入 Token 数量成正比。如果 System Prompt 每次工具调用后都改变，前缀缓存就会失效，每次都需要重新处理整个 System Prompt。

对于长期运行的 Agent（数小时、数天），这个优化的累积效果极为可观：

```
不优化：每次 API 调用处理完整 System Prompt（约 3,000 tokens）
优化后：前缀缓存命中，System Prompt 只处理一次
节省：数千次调用 × 3,000 tokens/次 = 数百万 tokens
```

### 实际使用中的注意点

- **工具响应始终显示实时状态**：虽然 System Prompt 不变，但 `memory` 工具的返回值会告诉 Agent 当前实际的记忆内容
- **Agent 知道这个机制**：System Prompt 中会告知"记忆更改下次会话生效"
- **不影响正确性**：本次会话中 Agent 通过工具响应知道最新记忆，只是 LLM 的"背景知识"到下次才更新

---

## 六、Layer 3：FTS5 跨会话召回 —— 情节记忆

### 定位

MEMORY.md 和 USER.md 的容量是刻意有限的（~1,300 tokens 合计）。**历史的详细内容**存储在 SQLite 数据库里，通过全文检索按需召回。

### 工作原理

```
Agent 遇到需要历史信息的任务
   ↓
调用历史搜索工具（非默认，按需触发）
   ↓
SQLite FTS5 全文检索所有历史会话
   ↓
返回相关片段
   ↓
辅助 LLM（auxiliary_client.py）对结果摘要
   ↓
精炼后的相关记忆注入当前上下文
```

### SQLite 会话存储结构

```sql
-- 简化的 Schema 概念
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    created_at DATETIME,
    platform TEXT,           -- cli / telegram / discord 等
    session_key TEXT,        -- 会话标识
    messages TEXT,           -- JSON 序列化的消息列表
    summary TEXT             -- LLM 生成的会话摘要
);

-- FTS5 全文索引
CREATE VIRTUAL TABLE sessions_fts USING fts5(
    content,                 -- 消息内容
    content="sessions",
    content_rowid="rowid"
);
```

### 为什么不把所有历史放进 System Prompt？

| 方案 | 问题 |
|---|---|
| 全部历史进 Prompt | Token 爆炸，成本不可控，信噪比低 |
| 固定数量最近消息 | 丢失更早的相关上下文 |
| FTS5 按需召回（Hermes 方案） | 只在需要时加载，精确相关，成本可控 |

FTS5 按需召回是**情节记忆**的最佳工程实现：大脑不会把所有记忆时刻保持激活，而是在需要时检索。

---

## 七、Layer 4：Honcho —— 辩证用户建模

### 定位

Honcho 是 Plastic Labs 开发的 AI 原生记忆和用户建模系统，Hermes 通过 `honcho-ai` 包集成它。

Honcho 做的事情比 USER.md 更深：

| USER.md | Honcho |
|---|---|
| 存储用户告诉 Agent 的事实 | 推断用户没有明确说出的偏好 |
| 静态添加 / 替换 | 辩证推理，动态更新 |
| 简单键值式事实 | 认知模型（Cognitive Model） |
| "用户喜欢简洁回答" | "用户在技术话题上偏好详细，在任务分配上偏好简洁" |

### 辩证推理（Dialectic Reasoning）机制

辩证推理的核心思想来自哲学：通过正题（Thesis）、反题（Antithesis）、合题（Synthesis）的循环，持续精炼认知。

在 Hermes 中的实现：

```
观察 1："用户要求简洁"（正题）
         ↓
观察 2："用户对代码解释要求很详细"（反题）
         ↓
推断："用户对文字说明要简洁，对技术代码要详细"（合题）
         ↓
更新用户模型，下次响应策略调整
```

### 访问 Honcho

```bash
hermes honcho        # 查看 Honcho 状态
hermes honcho reset  # 重置用户模型
```

---

## 八、容量管理与最佳实践

### 当记忆满了怎么办？

```json
{
  "success": false,
  "error": "Memory at 2,100/2,200 chars. Adding this entry (250 chars) would exceed the limit. Replace or remove existing entries first.",
  "current_entries": ["..."],
  "usage": "2,100/2,200"
}
```

Agent 的正确响应步骤：
1. 读取当前所有条目（错误响应中已包含）
2. 找出可以合并或删除的条目
3. 使用 `replace` 合并相关条目
4. 再次 `add` 新条目

### 好的记忆条目 vs 坏的记忆条目

**✅ 好的：信息密集，可操作**

```
# 把多个相关事实打包进一条
User runs macOS 14 Sonoma, Homebrew, Docker Desktop+Podman. 
Shell: zsh+oh-my-zsh. Editor: VS Code+Vim keybindings. Python: 3.12 via pyenv.

# 具体、有动作指导意义的约定
~/code/api: Go 1.22 + sqlc + chi router. Tests: 'make test'. Lint: 'make lint'. 
Deploy: 'make deploy-staging' / 'make deploy-prod'.

# 有时间戳的关键里程碑
Migrated DB from MySQL 5.7 to PostgreSQL 16 on 2026-03-01. 
Old dumps at ~/backups/mysql/. Connection string in .env.
```

**❌ 差的：模糊、冗余、可重新搜索到的信息**

```
# 太模糊
User has a project.

# 太冗长（适合放到 Context File，不适合记忆）
On January 5th, 2026, the user asked me to look at their project 
which is located at ~/code/api. I discovered it uses Go version 1.22 
and has several microservices...

# 可以随时 web search 到的事实
Python 3.12 supports f-string nesting. (不需要记，能搜到)
```

### 容量分配策略

```
MEMORY.md (2,200 chars)
├── 运行环境 (约 400 chars)
│   └── OS、工具链、Shell 配置
├── 主要项目 (约 800 chars)
│   └── 最多 3-4 个活跃项目的关键信息
├── 学到的经验教训 (约 500 chars)
│   └── 纠错记录、特殊配置、已知坑
└── 已完成里程碑 (约 500 chars)
    └── 重要任务的完成记录

USER.md (1,375 chars)
├── 身份信息 (约 200 chars)
│   └── 姓名、角色、时区
├── 沟通偏好 (约 500 chars)
│   └── 风格、格式、语言要求
├── 技术偏好 (约olean 400 chars)
│   └── 擅长领域、喜欢的工具/语言
└── 禁忌事项 (约 275 chars)
    └── 不喜欢的做法、需要避免的假设
```

---

## 九、安全扫描机制

Hermes 在写入记忆前会扫描内容，防止：

- **凭证泄露**：拦截看起来像 API Key、密码、Token 的内容
- **指令注入**：拦截试图通过记忆影响未来会话行为的指令
- **过大的条目**：拒绝单条超过合理大小的内容

---

## 十、记忆体系的完整数据流

```
┌──────────────────────────────────────────────────────────────┐
│                     会话开始时                                 │
│                                                              │
│   磁盘读取 MEMORY.md ──→ 冻结快照 ──→ 注入 System Prompt      │
│   磁盘读取 USER.md   ──→ 冻结快照 ──→ 注入 System Prompt      │
│   Skills Level 0    ──→           ──→ 注入 System Prompt      │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                     会话进行中                                 │
│                                                              │
│   任务需要历史 ──→ FTS5 搜索 ──→ LLM 摘要 ──→ 注入上下文      │
│   Agent 学到新东西 ──→ memory 工具 ──→ 立即写磁盘              │
│   所有消息 ──→ SQLite sessions 表（实时追加）                  │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                     会话结束后                                 │
│                                                              │
│   生成会话摘要 ──→ 存入 SQLite（供未来 FTS5 搜索）              │
│   Honcho 更新用户模型（跨会话辩证推理）                        │
└──────────────────────────────────────────────────────────────┘
```

---

## 十一、小结

Hermes 的记忆系统是精心分层的工程设计，而非简单的"存几条笔记"：

| 层次 | 解决的问题 | Token 成本 |
|---|---|---|
| MEMORY.md | 环境事实快速获取 | 固定（~800 tokens） |
| USER.md | 用户偏好自动应用 | 固定（~500 tokens） |
| FTS5 跨会话召回 | 历史经验按需检索 | 按需（仅在需要时消耗） |
| Honcho | 深度用户认知 | 后台异步 |

四层合力，构成了 Hermes 的记忆大脑——既轻量（总固定成本仅 1,300 tokens），又深度（历史无限，随用随取）。

---

*下一篇：[第四篇：Skills 系统 —— 程序性记忆与 agentskills.io 开放标准](./04_hermes_skills.md)*

*基于 2026 年 4 月版本 · GitHub: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)*
