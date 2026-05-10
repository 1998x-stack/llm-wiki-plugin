# GBrain 深度调研 · Artifact 01
# 总览：系统定位、架构哲学与核心设计

> **仓库**: `github.com/garrytan/gbrain`  
> **作者**: Garry Tan（Y Combinator CEO）  
> **定位**: "Garry's Opinionated OpenClaw/Hermes Agent Brain"  
> **本质**: 给 AI Agent 提供持久化、可自我生长的知识大脑  

---

## 1. 为什么会存在 GBrain

### 问题陈述

| 痛点 | 描述 |
|------|------|
| **知识碎片化** | 笔记散落在 Obsidian、Notion、meeting notes、CRM 导出等各处 |
| **搜索失效** | 纯关键词搜索漏掉语义匹配；纯向量搜索漏掉精确名称和短语 |
| **Agent 失忆** | LLM 没有跨会话记忆，每次对话从零开始，知识无法复利 |
| **知识腐坏** | 文档写完即老化，无机制维持"当前最优理解" |
| **人工代价** | 手工整理知识图谱成本极高，无法持续 |

### GBrain 的解法

```
你的 AI Agent 很聪明，但有遗忘症。
GBrain 给它一个大脑。
```

GBrain 的核心命题：**个人知识在规模上是一个智能问题，而不是存储问题。**

---

## 2. 系统定位：三层生态中的位置

```
┌─────────────────────────────────────────────────────┐
│                  AI Agent 运行时                      │
│         OpenClaw / Hermes / Claude Code              │
│    （感知、决策、响应 — 这些是 Agent 的工作）          │
├─────────────────────────────────────────────────────┤
│                    GBrain                            │
│  知识层：存储、索引、检索、维护、丰富                  │
│  （决定性基础设施 — 确定性代码，不依赖 LLM 判断）       │
├─────────────────────────────────────────────────────┤
│               GStack（可选配套）                      │
│  编码层：ship / review / QA / investigate            │
│  70,000+ stars，30,000 开发者/天                     │
└─────────────────────────────────────────────────────┘
```

> **GStack vs GBrain 分工**  
> - GStack = 代码能力（写代码、审查、QA）  
> - GBrain = 知识能力（记忆、思考、运营）  
> - `hosts/gbrain.ts` = 桥接文件，让 GStack 的编码 skill 在写代码前先查 brain

---

## 3. 核心架构哲学

### 3.1 "胖 Skill，瘦 Harness"

```
传统做法：把智能写进应用代码
GBrain 做法：把智能写进 Skill 文件（Markdown）
```

- **Harness（运行时）**：极薄，只负责 CLI 调度、数据库 I/O、嵌入向量
- **Skill（智能）**：极胖，每个 skill 文件是一个完整工作流的编码
- **Agent 是 Package Manager**：Agent 读取 skill，执行工作流

这意味着：升级智能 = 改 Markdown 文件，不需要重新部署代码。

### 3.2 Compiled Truth + Timeline 知识模型

每一个 brain page 遵循固定结构：

```markdown
---
type: person | company | concept | original | meeting
title: ...
tags: [...]
---

## 编译真相（Compiled Truth）
当前最优理解。有新证据时重写。
这是答案。

---

## 时间轴（Timeline）
- 2025-01-10: [事件 A]
- 2025-03-22: [事件 B]

仅追加，永不删除。这是证据。
```

| 层 | 特征 | 用途 |
|----|------|------|
| Compiled Truth | 可改写，保持最新 | 快速回答 |
| Timeline | 只追加，永不删除 | 溯源、审计 |

### 3.3 确定性优先，LLM 作为后备

```
分类器使用正则 → 87% 确定性处理（第1周40%，不断提升）
LLM fallback → 剩余13%
gbrain doctor: "intent classifier: 87% deterministic, up from 40% in week 1"
```

失败驱动改进：每次 LLM fallback 被记录，并自动生成更好的正则模式。

### 3.4 自动布线知识图谱

```
每次 brain page 写入 → 自动提取实体引用 → 创建类型化链接
零 LLM 调用完成图谱布线
```

支持的关系类型：`attended` / `works_at` / `invested_in` / `founded` / `advises`

---

## 4. 生产级规模数据

Garry Tan 的真实部署数据（12天内构建）：

| 指标 | 数值 |
|------|------|
| Brain pages | 17,888 页 |
| People 实体 | 4,383 人 |
| Company 实体 | 723 家 |
| 运行中 Cron jobs | 21 个 |
| 参考架构规模 | 14,700+ 文件，40+ skills，20+ cron |
| 构建时间 | 12 天 |

---

## 5. 技术栈

| 层 | 技术选型 | 理由 |
|----|---------|------|
| **运行时** | Bun (TypeScript) | 速度快，原生 TypeScript，比 Node 快3-4x |
| **数据库** | Postgres + pgvector | 混合搜索（关键词 + 向量）在同一 DB |
| **托管** | Supabase Pro ($25/月) | 零运维，8GB 存储，内置 pgvector |
| **向量模型** | OpenAI text-embedding-3-large | 高质量嵌入 |
| **LLM** | Claude Haiku (Anthropic) | 多查询扩展 + LLM 分块，价格低 |
| **向量索引** | HNSW (cosine) | 近似最近邻，速度/精度平衡 |
| **关键词索引** | tsvector + ts_rank | Postgres 原生全文搜索 |
| **融合算法** | RRF (Reciprocal Rank Fusion) | 混合搜索结果合并 |
| **分发方式** | npm package (bun add gbrain) | 库优先，CLI 和 MCP 是瘦包装 |

---

## 6. 安装路径矩阵

```
┌──────────────────┬────────────────────────────────────────┐
│ 安装方式          │ 命令                                    │
├──────────────────┼────────────────────────────────────────┤
│ OpenClaw（推荐）  │ 粘贴一段自然语言指令，Agent 自动完成安装  │
│ ClawHub          │ clawhub install gbrain                 │
│ 全局 CLI         │ bun add -g gbrain                      │
│ 项目库           │ bun add gbrain                          │
│ 从源码           │ git clone + bun install + bun link     │
└──────────────────┴────────────────────────────────────────┘
```

初始化统一入口：
```bash
gbrain init --supabase   # 向导式，自动或手动配置 Supabase
gbrain init --url <url>  # 连接任意带 pgvector 的 Postgres
```

---

## 7. Brain-Agent 核心循环（宏观视角）

```
信号到达（消息 / 会议 / 邮件 / 推文 / 链接）
        │
        ▼
检测实体（人、公司、概念、原创想法）
        │  → 异步子 Agent，不阻塞主流程
        ▼
READ：先查 brain（gbrain search / gbrain get / gbrain query）
        │
        ▼
用 brain context 响应（每个答案都因上下文而更好）
        │
        ▼
WRITE：更新 brain pages（新信息 → compiled truth + timeline）
        │
        ▼
SYNC：gbrain indexes changes（新内容进入向量索引）
        │
        ▼
（下次信号到达 — Agent 比上次更聪明）
```

**两条不变式**：
1. 每次 READ 改善当前响应
2. 每次 WRITE 改善未来 READ

六个月后的效果：Agent 对你的世界了解程度超过你工作记忆的上限，因为它从不忘记，从不停止索引。

---

## 8. GBrain vs 竞品定位

| 维度 | GBrain | Mem.ai | Obsidian+插件 | Notion AI | 传统 RAG |
|------|--------|--------|--------------|-----------|---------|
| **存储层** | Postgres+pgvector | 私有 | 本地文件 | 云端 | 可变 |
| **搜索质量** | 混合（向量+关键词+RRF） | 向量为主 | 插件依赖 | 语义搜索 | 可变 |
| **Agent 集成** | 原生（MCP + CLI） | 有限 | 无 | 有限 | 手动 |
| **知识模型** | Compiled Truth+Timeline | 简单记录 | 无结构约束 | 无 | 无 |
| **自动维护** | 是（Agent 夜间运行） | 部分 | 无 | 无 | 无 |
| **知识图谱** | 自动布线类型化链接 | 无 | 手动 | 无 | 无 |
| **实体丰富** | 3层自动升级 | 无 | 无 | 无 | 无 |
| **开源** | 是 | 否 | 是 | 否 | 取决于实现 |

---

*下一篇：[Artifact 02 - GBrain 核心组件深度解析]*
