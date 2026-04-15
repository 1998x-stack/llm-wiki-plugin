# OpenClaw 架构总览

> **MIT 开源 · 自托管 · 模型无关 · 本地优先**  
> GitHub Stars 破 163,000+（2026 年初创下增速记录）

---

## 一、什么是 OpenClaw？

OpenClaw（前身：Clawdbot → Moltbot）是一个用 **TypeScript** 编写的开源 AI Agent 框架，核心定位是：

| 维度 | 描述 |
|------|------|
| **本质** | 本地运行的 Agent 编排网关，不是聊天机器人 |
| **数据主权** | 所有记忆/对话以 Markdown 文件存储在本机，不上云 |
| **模型无关** | 支持 Claude、GPT、Gemini、Ollama 本地模型，随时切换 |
| **渠道无关** | 接入 WhatsApp、Telegram、Slack、Discord、iMessage 等 40+ 平台 |
| **自主调度** | Heartbeat 守护进程让 Agent 无需人类触发，主动执行任务 |

---

## 二、五大核心组件

```
 ┌──────────────────────────────────────────────────────────┐
 │                    外部通讯渠道                            │
 │  WhatsApp / Telegram / Slack / Discord / Signal / ...    │
 └────────────────────────┬─────────────────────────────────┘
                          │ 消息输入（各协议）
                          ▼
 ┌──────────────────────────────────────────────────────────┐
 │   ① GATEWAY（控制平面）  ws://127.0.0.1:18789            │
 │   Channel Adapter → 会话路由 → Lane Queue               │
 └────────────────────────┬─────────────────────────────────┘
                          │ 规范化消息对象
                          ▼
 ┌──────────────────────────────────────────────────────────┐
 │   ② BRAIN（Agent Runner / 推理引擎）                      │
 │   Context Assembly → LLM 调用 → ReAct 循环               │
 └─────┬─────────────────────────────────────┬─────────────┘
       │ 读取/写入                            │ 调用
       ▼                                     ▼
 ┌─────────────┐                    ┌─────────────────────┐
 │ ③ MEMORY    │                    │  ④ SKILLS           │
 │ Markdown 文件│                   │  SKILL.md 插件包     │
 │ JSONL 日志  │                    │  ClawHub 市场        │
 └─────────────┘                    └─────────────────────┘
                          ▲
                          │ 定时触发 / 主动唤醒
 ┌──────────────────────────────────────────────────────────┐
 │   ⑤ HEARTBEAT（调度守护进程）                             │
 │   Cron 任务 · 收件箱监控 · 主动消息推送                   │
 └──────────────────────────────────────────────────────────┘
```

---

## 三、一条消息的完整生命周期

```
用户发送 WhatsApp 消息
       │
       ▼
Channel Adapter 转换为统一消息对象（含语音转文字）
       │
       ▼
Gateway 会话路由 → 确定目标 Agent + Session
       │
       ▼
Lane Queue 串行排队（防止并发竞争）
       │
       ▼
Agent Runner 组装上下文（基础提示词 + Skills 列表 + Memory + History）
       │
       ▼
调用 LLM API（Claude / GPT / Ollama...）
       │
       ├── 纯文本回复 ──→ 流式返回给用户 → 写入 JSONL
       │
       └── 工具调用请求
              │
              ▼
        执行工具（Shell / 文件 / 浏览器 / API）
              │
              ▼
        结果注入上下文 → 继续 ReAct 循环
              │
              ▼
        最终回复 → 流式返回 → 持久化
```

---

## 四、核心设计哲学

| 原则 | 实现方式 |
|------|----------|
| **Listen（倾听）** | Gateway + Channel Adapters |
| **Think（思考）** | Brain / ReAct 循环 |
| **Do（执行）** | Skills + 工具调用 |
| **Remember（记忆）** | Memory（Markdown + JSONL）|

---

## 五、与主流框架对比

| 框架 | 定位 | 配置方式 | 执行模型 | 数据隔离 |
|------|------|----------|----------|----------|
| **OpenClaw** | 持久化 Agent 系统 | Markdown 文件 | 自托管 Gateway | 本地优先 |
| **LangChain** | Pipeline 工具库 | Python 代码 | 函数调用 | 依赖提供商 |
| **AutoGPT** | 研究原型 | Python 代码 | 无持久化 | 云依赖 |
| **CrewAI** | 角色协作框架 | Python 类 | 任务中心 | 云依赖 |
| **AutoGen** | 多 Agent 对话 | Python 类 | 对话模式 | 云依赖 |

---

## 六、快速索引

| 文档 | 内容 |
|------|------|
| `01_gateway.md` | Gateway 控制平面详解 |
| `02_brain.md` | Brain/Agent Runner & ReAct 循环 |
| `03_memory.md` | Memory 系统（Markdown + JSONL）|
| `04_skills.md` | Skills 插件体系 & ClawHub |
| `05_heartbeat.md` | Heartbeat 调度守护进程 |
| `06_security.md` | 安全边界 & 部署最佳实践 |
