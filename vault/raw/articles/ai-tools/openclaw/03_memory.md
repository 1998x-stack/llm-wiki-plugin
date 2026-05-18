# OpenClaw ③ MEMORY — 持久化记忆系统

> OpenClaw 的记忆系统哲学：**简单、可解释、可移植**。  
> 没有向量数据库，没有复杂的 RAG 管道——只有 Markdown 文件和 JSONL 日志。

---

## 1. 记忆系统总览

```
┌─────────────────────────────────────────────────────────┐
│                    Memory 系统                           │
│                                                          │
│  ┌───────────────────┐    ┌──────────────────────────┐  │
│  │  JSONL Transcripts │    │   Markdown Memory Files  │  │
│  │  （事实日志层）    │    │   （语义记忆层）          │  │
│  │                   │    │                          │  │
│  │  逐行审计记录：   │    │  AGENT.md  → Agent 身份  │  │
│  │  · User 消息      │    │  SOUL.md   → 个性/汇报链 │  │
│  │  · Tool 调用      │    │  memory.md → 用户偏好    │  │
│  │  · Tool 结果      │    │  context.md→ 环境上下文  │  │
│  │  · Assistant 回复 │    │  任意 .md  → 自定义知识  │  │
│  └───────────────────┘    └──────────────────────────┘  │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Bootstrap Context（启动加载）                     │  │
│  │  workspace 级别上下文，每次 Agent 启动时注入       │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘

所有文件存储在本机本地，不上云，数据主权完全归用户
```

---

## 2. JSONL Transcripts — 事实日志层

### 2.1 什么是 JSONL Transcript？

JSONL（JSON Lines）是每行一个 JSON 对象的文本格式，OpenClaw 用它记录 Agent 执行的完整审计轨迹：

```jsonl
{"role":"user","content":"帮我整理一下今天的会议记录","ts":1742000000,"session":"main"}
{"role":"assistant","content":"好的，我先读取今天的文件...","ts":1742000001,"session":"main"}
{"role":"tool_call","name":"file_list","params":{"path":"/workspace/meetings/"},"ts":1742000002}
{"role":"tool_result","name":"file_list","result":["2026-03-30.md"],"ts":1742000003}
{"role":"tool_call","name":"file_read","params":{"path":"/workspace/meetings/2026-03-30.md"},"ts":1742000004}
{"role":"tool_result","name":"file_read","result":"# 会议记录\n...","ts":1742000005}
{"role":"assistant","content":"整理完毕，以下是结构化版本：\n...","ts":1742000006,"session":"main","cost":{"input":1200,"output":340}}
```

### 2.2 JSONL 的作用

| 作用 | 说明 |
|------|------|
| **Session 历史恢复** | Agent 重启后能从断点继续 |
| **上下文注入** | Session History Loader 读取并注入对话历史 |
| **审计追踪** | 完整记录每次工具调用的参数和结果 |
| **调试可见性** | 开发者可直接用文本编辑器查看执行过程 |
| **成本追踪** | 记录每轮 Token 消耗和 API 费用 |

### 2.3 长对话压缩策略

```
对话轮次超过阈值
        │
        ▼
触发历史压缩（Context Window Guard 发起）
        │
        ▼
用廉价模型（如 claude-haiku）对旧轮次生成摘要
        │
        ▼
摘要替换原始旧轮次（保留最近 N 轮原文）
        │
        ▼
压缩后 Transcript 写回磁盘

示例：
原始：100 轮对话 → 80,000 tokens
压缩：摘要（前80轮）+ 原文（后20轮）→ 12,000 tokens
```

---

## 3. Markdown Memory Files — 语义记忆层

### 3.1 文件类型与用途

#### AGENT.md — Agent 身份定义

```markdown
# Research Agent

## Role
Senior AI Research Analyst

## Core Responsibilities
- Monitor AI papers from arXiv, Papers With Code
- Write weekly bilingual reports (EN/ZH)
- Escalate breaking discoveries to: `@supervisor`

## Behavioral Guidelines
- Always cite sources
- Flag uncertainty explicitly
- Keep reports under 2,000 words unless asked

## Output Channels
- Daily digest → email
- Weekly report → /workspace/reports/weekly/
```

#### SOUL.md — 个性与组织层级

```markdown
# Agent Soul

## Personality
- Tone: Professional but approachable
- Verbosity: Concise. Use bullet points.
- Language: Respond in the same language as the user

## Reporting Chain
- Reports to: Learning Coach Agent
- Collaborates with: Data Collection Agent
- Escalates to: Human Operator (owner@example.com)

## Activation Rules
- Active hours: 07:00-23:00 (Asia/Shanghai)
- Wake on: @mention, direct message, scheduled heartbeat
```

#### memory.md — 用户偏好记忆

```markdown
# User Memory

## Preferences
- Coffee: Black, no sugar
- Writing style: Technical, avoid buzzwords
- Report format: Executive Summary first, details after
- Language: Chinese preferred for casual chat, English for technical

## Learned Facts
- Works at: TapTap Maker (XD Inc.)
- Timezone: Asia/Shanghai (UTC+8)
- Typical work hours: 09:00-21:00
- Prefers Telegram for urgent messages, email for reports

## Long-term Goals
- Build game AI evaluation framework
- Publish Manim math animation series

## Last Updated: 2026-03-30
```

#### context.md — 环境上下文

```markdown
# Workspace Context

## Environment
- OS: macOS arm64
- Workspace: /Users/xm/ai-workspace/
- Active Projects:
  - ECC（Everything Claude Code）研究文档
  - OpenClaw Skill 包开发
  - Manim 数学教育视频

## Current Sprint
- 截止：2026-04-15
- 优先级：技能包 > 评估框架 > 视频制作

## Team Contacts
- CEO: Huang Yimeng (Dash) - XD Inc.
```

---

### 3.2 Bootstrap Context 加载机制

```
Agent 启动
    │
    ▼
扫描 workspace 目录中的 .md 文件
    │
    ▼
按优先级排序：
  1. AGENT.md（最高，定义身份）
  2. SOUL.md（个性配置）
  3. memory.md（用户记忆）
  4. context.md（环境上下文）
  5. 其他自定义 .md 文件
    │
    ▼
合并为 Bootstrap Context Block → 注入 System Prompt Layer 3
```

---

## 4. 记忆读写流程

### 4.1 Agent 写入记忆

```
Agent 在 ReAct Loop 中决定需要记忆某信息
    │
    ▼
调用 memory_write 工具
    │
    ▼
工具参数：
{
  "file": "memory.md",
  "section": "Preferences",
  "content": "用户偏好黑咖啡，无糖"
}
    │
    ▼
文件系统写入（Append / Update 指定章节）
    │
    ▼
下次 Agent 启动时自动加载
```

### 4.2 Agent 读取记忆

```
情景：用户问"我平时喝什么咖啡？"
    │
    ▼
方案 A（Bootstrap 已加载）：
  → memory.md 已在 System Prompt 中，无需额外工具调用
  → 直接回答

方案 B（按需查询）：
  → LLM 调用 memory_read 工具
  → 指定 { "file": "memory.md", "query": "coffee preference" }
  → 返回匹配内容
  → 注入上下文后回答
```

---

## 5. 记忆架构设计哲学

### 5.1 为什么不用向量数据库？

| 维度 | 向量数据库（如 Milvus/Chroma） | OpenClaw Markdown |
|------|-------------------------------|-------------------|
| 可读性 | 不可直接阅读 | 人类直接可读/编辑 |
| 可移植性 | 需要专属工具导出 | 文件夹复制即可迁移 |
| 复杂度 | 需要 embedding 模型、向量索引 | 无额外依赖 |
| 版本控制 | 困难 | 直接 git commit |
| 隐私风险 | 数据可能存储于第三方 | 100% 本地 |
| 精确搜索 | 语义相似 | 结构化章节直接查 |

> **核心洞见：大多数个人 Agent 场景的记忆量远未达到需要向量检索的规模。**
> Markdown 的简单性带来了极大的工程优势。

---

### 5.2 Workspace 目录结构示例

```
/workspace/
├── AGENT.md              # Agent 身份（必须）
├── SOUL.md               # 个性配置（推荐）
├── memory.md             # 用户偏好记忆
├── context.md            # 环境上下文
├── skills/               # 本地 Skill 包
│   ├── github-reviewer/
│   │   └── SKILL.md
│   └── email-digest/
│       └── SKILL.md
├── transcripts/          # JSONL 对话日志
│   ├── main.jsonl
│   └── research-agent.jsonl
├── reports/              # Agent 产出
│   ├── weekly/
│   └── daily/
└── tmp/                  # 临时文件（自动清理）
```

---

## 6. 记忆安全与隐私

| 措施 | 说明 |
|------|------|
| **本地存储** | 所有记忆文件在用户本机，不发送云端 |
| **显式配置** | 需主动配置才会共享数据到外部服务 |
| **文件级权限** | 依赖 OS 文件权限（chmod 600 推荐）|
| **敏感数据警示** | 不建议在 memory.md 存储密码、密钥（使用系统 Keychain）|

---

## 7. 与 Claude 内置 Memory 对比

| 维度 | OpenClaw Memory | Claude.ai Memory |
|------|-----------------|------------------|
| 存储位置 | 本机 Markdown | Anthropic 云端 |
| 用户控制 | 完全自主（CRUD 任意）| 依赖平台 UI |
| 跨模型 | 可携带到任意 LLM | 仅限 Claude |
| 结构化程度 | 自由格式 Markdown | 平台管理的键值对 |
| 编程可访问 | 是（文件 API）| 否 |
| 版本历史 | 可接 git 管理 | 无 |
