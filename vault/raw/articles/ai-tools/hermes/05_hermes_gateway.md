# Hermes Agent 深度解析 · 第五篇：Gateway 消息网关 —— 14+ 平台统一接入

> **系列导读**：Hermes 的 Gateway 是把 Agent 能力暴露到任意消息平台的通信总线。本篇深入 Gateway 的架构设计、15 个平台适配器、消息路由机制、会话持久化，以及 Cron 调度系统和 ACP 编辑器集成。

---

## 一、为什么需要 Gateway？

大多数 Agent 工具是这样使用的：

```
打开终端 → 运行命令 → 等待输出 → 继续
```

你必须在电脑前，必须打开特定工具。这把 Agent 的使用场景限制在了"主动坐到电脑前"这一个模式里。

Hermes 的 Gateway 打破了这个限制：

```
在手机上发 Telegram 消息 → Agent 在云端 VM 执行 → 结果推送回手机
在上班路上用 WhatsApp 提任务 → Agent 下班前完成 → 下班后收到结果
在 Slack 群里 @Agent → Agent 执行并在群里回复
```

一个 Gateway 进程，让 Agent 活在你存在的任何地方。

---

## 二、Gateway 的架构定位

在 Hermes 的系统架构中，Gateway 是**入口层**的核心组件之一：

```
┌─────────────────────────────────────────────────────────────┐
│                        入口层                                 │
│                                                             │
│  CLI        Gateway (←─ 本篇重点)        ACP        Batch  │
│  (cli.py)   (gateway/run.py)          (acp_adapter/)       │
└──────────────────────┬──────────────────────────────────────┘
                       │ 最终都调用
                       ▼
              AIAgent.run_conversation()
```

Gateway 本身不执行 AI 推理，它负责：
1. 接收来自各平台的消息
2. 标准化为内部格式（MessageEvent）
3. 管理会话状态
4. 调用 AIAgent 处理
5. 将结果发回原平台

### Gateway vs OpenClaw 架构的根本差异

OpenClaw 把 Gateway 作为**控制平面**：一个拥有会话、路由、工具执行和状态的单一长期进程，所有东西都流过它。

Hermes 的 Gateway 更轻：它是消息路由层，核心逻辑在 AIAgent 循环里，Gateway 只负责"把消息送进去、把结果送出来"。

---

## 三、15 个平台适配器

`gateway/platforms/` 目录包含 15 个平台适配器：

### 即时消息平台

| 平台 | 特点 |
|---|---|
| **Telegram** | 最常用，支持 Bot API，消息格式丰富 |
| **Discord** | 支持频道和 DM，支持 Discord Voice Channel（语音模式） |
| **Slack** | 企业环境首选，支持 Workspace 级别 |
| **WhatsApp** | 通过 Business API 接入 |
| **Signal** | 隐私优先，端对端加密 |
| **Matrix** | 去中心化开放协议 |
| **Mattermost** | 开源 Slack 替代品，私有部署友好 |

### 传统通信渠道

| 平台 | 特点 |
|---|---|
| **Email** | 收邮件触发执行，结果发邮件返回 |
| **SMS** | 短信接入（通过 Twilio 等） |
| **BlueBubbles** | macOS iMessage 代理 |

### 国内平台

| 平台 | 特点 |
|---|---|
| **DingTalk（钉钉）** | 企业版接入 |
| **Feishu（飞书）** | 字节跳动企业协作 |
| **WeCom（企业微信）** | 腾讯企业微信 |

### 智能家居 / 通用接入

| 平台 | 特点 |
|---|---|
| **Home Assistant** | 智能家居语音/文字控制 Agent |
| **Webhook** | 通用 HTTP 接入，适合自定义集成 |

---

## 四、Gateway 核心模块详解

### `gateway/run.py` —— GatewayRunner（主进程）

约 7,500 行，是 Gateway 的心脏：

```python
# 简化概念
class GatewayRunner:
    def __init__(self, config):
        self.platforms = self._load_adapters(config)  # 加载所有配置的平台
        self.session_store = SessionStore()
        self.hooks = HookRegistry()
    
    async def _handle_message(self, event: MessageEvent):
        # 1. 授权验证
        if not self.pairing.is_authorized(event.user_id, event.platform):
            return self._reject(event)
        
        # 2. 解析会话 Key（platform + user_id 的组合）
        session_key = f"{event.platform}:{event.user_id}"
        
        # 3. 加载历史消息
        history = self.session_store.load(session_key)
        
        # 4. 创建 AIAgent（注入历史）
        agent = AIAgent(
            config=self.config,
            conversation_history=history,
            platform=event.platform,
        )
        
        # 5. 执行
        response = await agent.run_conversation(event.text)
        
        # 6. 发回响应
        await self.delivery.send(event.reply_to, response)
        
        # 7. 持久化会话
        self.session_store.save(session_key, agent.conversation_history)
```

### `gateway/session.py` —— SessionStore（会话持久化）

每个（平台 × 用户）组合维护独立的会话历史：

```
session_key: "telegram:123456789"
  → messages: [{role: user, content: "..."}, {role: assistant, content: "..."}, ...]
  → created_at: 2026-03-01T10:00:00
  → last_active: 2026-04-10T15:30:00
```

会话历史存储在 SQLite 中，支持：
- 按 session_key 精确查询
- FTS5 全文检索（跨会话搜索历史）
- 自动会话摘要（控制历史长度）

### `gateway/delivery.py` —— 出站消息投递

处理向不同平台发送消息的细节：
- 长消息分段（各平台有不同的长度限制）
- Markdown 格式转换（不同平台支持不同的 Markdown 子集）
- 媒体文件上传（图片、文件、音频）
- 失败重试

### `gateway/pairing.py` —— DM 配对授权

防止任何人都能使用你的 Agent：

```bash
# 首次使用前，在 CLI 生成配对码
hermes gateway pair

# 在 Telegram 中发送
/pair <配对码>

# 配对成功后，该 Telegram 账户被授权
```

支持多用户授权（家庭成员、团队成员），但每个用户有独立的会话隔离。

### `gateway/hooks.py` —— 生命周期 Hooks

在关键事件点插入自定义逻辑：

```python
# 示例：每次会话开始时记录日志
@on_event("session_start")
async def log_session(event: MessageEvent):
    logger.info(f"New session: {event.platform}:{event.user_id}")

# 示例：特定关键词触发特殊处理
@on_event("message_received")
async def handle_urgent(event: MessageEvent):
    if "URGENT" in event.text.upper():
        event.priority = "high"
```

内置 Hooks（`builtin_hooks/`）提供：
- 心跳检测
- 日报日志
- 周报摘要
- 错误通知

### `gateway/mirror.py` —— 跨会话消息镜像

将同一个 Agent 的多个平台对话镜像同步：

```
在 Telegram 说："我今天要完成数据库迁移"
       ↓
mirror.py 同步
       ↓
打开 CLI 时，Agent 已经知道你今天的计划
```

适用于需要跨设备无缝切换的场景。

---

## 五、Gateway 消息处理完整流程

```
┌──────────────────────────────────────────────────────────────┐
│                    消息从到达到响应的完整链路                    │
│                                                              │
│  1. 平台事件到达（如 Telegram Bot Webhook）                   │
│           ↓                                                  │
│  2. Adapter.on_message() 解析平台特定格式                     │
│           ↓                                                  │
│  3. 转换为 MessageEvent（统一内部格式）                        │
│     {platform, user_id, text, media?, reply_to, timestamp}  │
│           ↓                                                  │
│  4. GatewayRunner._handle_message()                          │
│           ↓                                                  │
│  5. pairing.is_authorized(user_id, platform)                 │
│     未授权 → 拒绝/提示配对                                    │
│           ↓                                                  │
│  6. 解析 session_key = f"{platform}:{user_id}"               │
│           ↓                                                  │
│  7. session_store.load(session_key) → 历史消息                │
│           ↓                                                  │
│  8. 创建 AIAgent（注入历史 + 平台元数据）                     │
│           ↓                                                  │
│  9. agent.run_conversation(event.text)                       │
│           ↓ （完整的工具调用循环在这里发生）                   │
│  10. delivery.send(event.reply_to, response)                 │
│           ↓                                                  │
│  11. session_store.save(session_key, updated_history)        │
│           ↓                                                  │
│  12. hooks.emit("session_end", event)                        │
└──────────────────────────────────────────────────────────────┘
```

---

## 六、Cron 调度：让 Agent 主动出击

Hermes 内置了一个 Cron 调度系统，让 Agent 不只是被动响应，而是在你指定的时间**主动执行任务**。

### 自然语言调度

```bash
# 不需要记 crontab 格式，直接用自然语言
hermes cron add "每天早上 9 点，搜集科技新闻摘要，发到我的 Telegram"
hermes cron add "每周一上午，分析上周 git 提交，生成周报发到 Slack"
hermes cron add "每月 1 日，统计上月 API 调用费用，发邮件报告"
```

Hermes 自动将自然语言转换为 cron 表达式。

### Cron 任务执行流程

```
调度器 tick（每分钟检查一次）
       ↓
从 jobs.json 加载到期任务
       ↓
每个任务：创建全新 AIAgent（无会话历史，每次独立）
       ↓
注入任务附加的 Skills 作为上下文
       ↓
运行任务提示词（你写的任务描述）
       ↓
delivery.send() 投递到配置的目标平台
       ↓
更新 jobs.json 中的 next_run 时间戳
```

**关键设计：每次 Cron 任务创建全新 AIAgent。**  
Cron 任务是隔离的，不携带历史，确保结果的确定性和可重现性。

### Cron 管理命令

```bash
hermes cron list              # 列出所有定时任务
hermes cron show job_1        # 查看特定任务详情
hermes cron run job_1         # 手动立即执行
hermes cron disable job_1     # 暂停
hermes cron delete job_1      # 删除
```

---

## 七、ACP：编辑器集成层

ACP（Agent Communication Protocol）是 Hermes 与代码编辑器集成的标准协议，通过 `acp_adapter/` 实现。

### 支持的编辑器

- **VS Code**（通过扩展）
- **Zed**（原生支持）
- **JetBrains IDE 系列**（通过插件）

### ACP 提供什么

```
代码编辑器中选中代码片段
       ↓
右键 → "Ask Hermes"
       ↓
ACP 将选中代码 + 用户问题发给本地 Hermes Agent
       ↓
Agent 结合代码上下文（项目 MEMORY.md、Skills）回答
       ↓
结果显示在编辑器 sidebar
```

相比直接在 IDE 中集成 AI：ACP 使用的是你本地已配置好的 Hermes Agent，携带了你的记忆、技能、项目上下文，比从零开始的 IDE 插件更了解你的项目。

---

## 八、Gateway 配置与启动

### 完整配置流程

```bash
# 1. 交互式配置 Gateway
hermes gateway setup

# 2. 配置特定平台（以 Telegram 为例）
# 需要：BotFather 创建的 Bot Token
# 设置 Webhook URL 或 Polling 模式

# 3. 启动 Gateway
hermes gateway start

# 4. 后台运行（推荐生产环境）
hermes gateway start --daemon

# 5. 查看状态
hermes gateway status

# 6. 停止
hermes gateway stop
```

### 典型的 `config.yaml` Gateway 配置

```yaml
gateway:
  platforms:
    telegram:
      enabled: true
      token: "YOUR_BOT_TOKEN"
      mode: webhook          # 或 polling
      webhook_url: "https://your-domain.com/webhook/telegram"
    
    discord:
      enabled: true
      token: "YOUR_DISCORD_BOT_TOKEN"
      
    slack:
      enabled: false          # 暂时禁用
      
  authorization:
    mode: pairing             # 需要配对才能使用
    allowed_users:            # 或直接白名单
      - telegram:123456789
      
  session:
    max_history: 50           # 保留最近 50 条消息
    auto_summarize: true      # 自动摘要压缩历史
```

---

## 九、多平台协同使用场景

### 场景 A：移动工作流

```
早上通勤（手机 Telegram）：
"今天需要完成 API 的认证模块，先帮我分析一下现有代码结构"
       ↓ Agent 在云端分析
"收到！项目结构如下... 建议从 middleware/ 目录开始..."

到办公室（CLI）：
# 会话历史已同步，直接继续
hermes chat
"继续刚才的认证模块，先写 JWT 验证部分"
```

### 场景 B：团队 Slack Bot

```yaml
# 配置为团队 Slack Agent
gateway:
  platforms:
    slack:
      enabled: true
      workspace: "your-team"
  authorization:
    allowed_users:
      - slack:U123456  # 团队成员 A
      - slack:U789012  # 团队成员 B
```

在 Slack 频道中：
```
@HermesBot 帮我查一下上个月的 AWS 费用，跟这个月对比
       ↓
Bot: 正在查询...（运行 AWS CLI 命令）
     上月总费用：$234.56，本月截至今日：$198.23，下降 15%...
```

### 场景 C：Home Assistant 智能家居

```yaml
gateway:
  platforms:
    homeassistant:
      enabled: true
      url: "http://homeassistant.local:8123"
      token: "YOUR_HA_TOKEN"
```

```
语音助手："Hermes，把客厅灯光调到 50%，并把我明天早 9 点的会议日程告诉我"
       ↓ Agent 调用 HA API + Calendar API
"灯光已调整。明天早 9 点你有「季度复盘」会议，参与者 5 人。"
```

---

## 十、小结

Gateway 系统的设计有三个核心价值：

1. **平台无关性**：15 个适配器统一接口，Agent 逻辑与平台解耦。新增一个平台只需实现适配器，不改变 AIAgent。

2. **会话持久性**：每个（平台 × 用户）组合维护独立的历史，换平台不丢上下文（配合 mirror.py）。

3. **主动 + 被动双模式**：Gateway 处理被动响应，Cron 处理主动触发，两者共用相同的 AIAgent 执行引擎。

结合记忆系统（第三篇）和技能系统（第四篇），Gateway 让 Hermes 成为真正的**持续在线的个人 AI**：随时可达，有记忆，会学习，能主动。

---

*下一篇：[第六篇：闭环学习引擎 —— 自动技能创建、Honcho 用户建模与 RL 训练基础设施](./06_hermes_learning_loop.md)*

*基于 2026 年 4 月版本 · GitHub: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)*
