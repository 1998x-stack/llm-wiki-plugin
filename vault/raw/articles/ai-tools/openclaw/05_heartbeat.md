# OpenClaw ⑤ HEARTBEAT — 调度守护进程

> Heartbeat 是让 OpenClaw 从"被动响应"变成"主动行动"的关键机制。  
> 核心模式：**Cron 触发的 Agentic Loop**

---

## 1. Heartbeat 的本质

```
传统 Chatbot 模型（被动）：
  用户发消息 → Agent 响应 → 等待下一条消息
  Agent 的行动 100% 依赖人类触发

OpenClaw Heartbeat 模型（主动）：
  定时器触发 → Agent 唤醒 → 评估任务列表 → 自主执行 → 推送结果
  Agent 可以在无人类输入的情况下持续工作 24/7
```

---

## 2. Heartbeat 架构

```
┌─────────────────────────────────────────────────────────┐
│                   Heartbeat 守护进程                     │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Cron Scheduler（时间触发器）                   │    │
│  │  支持 Cron 表达式 / 固定间隔 / 事件触发         │    │
│  └──────────────────┬──────────────────────────────┘    │
│                     │ 触发                               │
│                     ▼                                    │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Task Evaluator（任务评估器）                    │    │
│  │  Agent 读取任务列表，决定执行哪些任务           │    │
│  └──────────────────┬──────────────────────────────┘    │
│                     │ 分发                               │
│                     ▼                                    │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Inbox Monitor（收件箱监控）                     │    │
│  │  检查邮件/日历/RSS 等外部源的变化               │    │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Proactive Message Sender（主动消息推送）        │    │
│  │  将结果推送到配置的渠道（Telegram/Slack/Email）  │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Cron Scheduler 详解

### 3.1 支持的触发类型

| 类型 | 示例 | 描述 |
|------|------|------|
| **Cron 表达式** | `0 7 * * *` | 每天 07:00 触发 |
| **固定间隔** | `every: 30m` | 每 30 分钟触发 |
| **事件触发** | `on: file_changed` | 文件变化时触发 |
| **条件触发** | `when: market_open` | 满足条件时触发 |

### 3.2 Heartbeat 配置示例

```yaml
# heartbeat.yaml
heartbeats:

  # 每日早报
  morning-briefing:
    schedule: "0 7 * * 1-5"    # 工作日 07:00
    timezone: "Asia/Shanghai"
    task: |
      请生成今天的早报，包含：
      1. 昨晚的 AI 领域重要新闻（arXiv + Twitter）
      2. 今天的日历安排
      3. 待处理的重要邮件摘要
      4. 今日优先任务推荐
    output:
      channel: telegram
      format: markdown

  # 市场监控
  market-watch:
    schedule: "*/15 9-16 * * 1-5"  # 交易日每15分钟
    task: |
      检查关注的股票列表，如有异常波动（±3%）立即通知
    output:
      channel: telegram
      only_if_changed: true       # 无变化不推送

  # HackerNews 精华
  hn-digest:
    schedule: "0 9,18 * * *"    # 每天 09:00 和 18:00
    task: |
      抓取 HackerNews Top 10，过滤 AI/游戏/开源相关内容
      生成 3 句话摘要 + 链接，用中文输出
    output:
      channel: telegram

  # 网站变化监控
  competitor-monitor:
    schedule: "0 10 * * 1"     # 每周一 10:00
    task: |
      访问以下竞品网站，与上周快照对比，报告显著变化：
      - https://competitor-a.com/pricing
      - https://competitor-b.com/changelog
    output:
      channel: email
      to: "team@company.com"

  # 收件箱清理
  inbox-triage:
    schedule: "0 8,13 * * 1-5"  # 工作日 08:00 和 13:00
    task: |
      读取未处理邮件，按优先级分类：
      - 紧急（需2小时内回复）→ 标记并推送 Telegram 提醒
      - 重要（今天回复）→ 加入今日任务列表
      - 一般 → 归档到对应文件夹
    output:
      channel: telegram
```

---

## 4. 任务评估流程（Task Evaluator）

```
Heartbeat 触发
    │
    ▼
Agent 唤醒（注入 Heartbeat System Prompt）：
"你现在是自主调度模式。请评估当前任务列表，
 决定哪些任务需要立即执行。时间：2026-03-30 07:00"
    │
    ▼
Agent 读取：
- /workspace/tasks.md（待办任务列表）
- /workspace/memory.md（用户偏好）
- calendar_api（今日日程）
    │
    ▼
Agent 自主决策：
- 哪些任务今天需要做？
- 优先级排序
- 是否需要用户确认？
    │
    ├─ 可自主执行的任务 → 直接执行
    │
    └─ 需要确认的任务 → 推送询问消息给用户
```

**tasks.md 示例：**

```markdown
# 任务列表

## 每日任务
- [ ] 发送早报摘要
- [ ] 检查 AI 论文更新
- [ ] 整理收件箱

## 周期任务
- [ ] 每周一：生成竞品分析报告
- [ ] 每月初：整理上月 API 费用

## 待确认任务
- [ ] 续订服务器订阅（费用 $120/月）⚠️ 需人工确认
- [ ] 删除 /data/old-exports/ 下 30 天前的文件 ⚠️ 需人工确认

## 一次性任务
- [ ] 整理 OpenClaw 技术文档草稿 → 截止 2026-04-01
```

---

## 5. Inbox Monitor 详解

Heartbeat 可以监控多种外部"收件箱"：

### 5.1 支持的监控源

| 类型 | 监控方式 | 触发条件 |
|------|----------|----------|
| **邮件（Gmail/IMAP）** | OAuth API 轮询 | 新邮件到达 |
| **日历（Google Calendar）** | API 轮询 | 会议即将开始（30分钟前）|
| **RSS Feed** | HTTP 请求 | 新文章发布 |
| **网页变化** | 快照对比 | 内容发生变化 |
| **GitHub** | Webhooks / API | 新 PR / Issue / 评论 |
| **Slack 渠道** | Slack API | @提及 / 关键词 |
| **文件系统** | inotify / FSEvents | 文件创建/修改 |

### 5.2 邮件监控示例

```yaml
inbox_monitors:
  gmail:
    check_interval: 5m
    filters:
      - from: "*@important-client.com"
        priority: urgent
        action: notify_immediately
      - subject_contains: "[Invoice]"
        priority: high
        action: extract_and_log
      - older_than: 7d
        is_unread: false
        action: archive
    output:
      urgent → telegram (immediate push)
      high   → tasks.md (add to today's list)
      normal → weekly_digest.md (batch)
```

---

## 6. 主动消息推送（Proactive Sender）

```
Heartbeat 执行完成
    │
    ▼
生成输出内容（Markdown 格式）
    │
    ▼
输出路由决策：
  ├─ 用户当前在线（最近 30 分钟有活动）→ 直接推送
  ├─ 用户不在线 + 优先级 urgent → 立即推送
  ├─ 用户不在线 + 优先级 normal → 排入早报队列
  └─ 无变化 / 无重要内容 → 静默跳过
    │
    ▼
选择推送渠道：
  - Telegram Bot → 即时消息
  - Email → 富文本报告
  - Slack → 团队频道
  - WhatsApp → 移动端提醒
    │
    ▼
格式适配（渠道特定分片/格式）→ 发送
```

**Telegram 推送示例输出：**

```
🌅 早报 2026-03-30 07:00

📰 AI 快讯（3条）
• Claude 4 Opus 发布，推理能力大幅提升
• OpenClaw GitHub Stars 突破 163k
• DeepSeek R2 论文泄露

📅 今日日程
• 10:00 - 产品评审会（1h）
• 15:00 - 与 Dash 1:1

📬 待处理邮件（2封）
• [紧急] 来自投资方的 Term Sheet 确认邮件
• [一般] 服务器账单通知

✅ 今日推荐任务
1. 回复投资方邮件
2. 完成 OpenClaw 技术文档 Draft v1
3. Review PR #127（截止明天）

---
⚡ 由 OpenClaw Heartbeat 自动生成
```

---

## 7. 成本控制与安全护栏

### 7.1 API 费用风险

⚠️ **警告：配置不当的 Heartbeat 可能导致 API 费用爆炸**

```
危险场景示例：
- schedule: "*/1 * * * *"  ← 每分钟执行
- task: 复杂的多工具任务（每次消耗 5,000 tokens）
- 一天 1440 次 × 5,000 tokens = 7,200,000 tokens
- Claude Opus 4 成本：~$108/天 💸
```

**费用控制配置：**

```yaml
heartbeat_limits:
  max_cost_per_day: 5.00       # 每日最大费用 $5
  max_tokens_per_run: 10000    # 单次最大 Token
  cost_alert_threshold: 3.00  # 超过 $3 发出警告
  emergency_stop: 10.00       # 超过 $10 自动停止
  preferred_model: "claude-haiku-4-5"  # Heartbeat 用廉价模型
```

### 7.2 不可逆操作护栏

```yaml
human_approval_required:
  - action_type: send_email
    description: "发送邮件给外部联系人"
  - action_type: file_delete
    description: "删除任何文件"
  - action_type: payment
    description: "任何涉及费用的操作"
  - action_type: api_post
    description: "向外部 API 发送 POST 请求"

timeout_for_approval: 30m    # 30分钟内未确认则跳过
```

---

## 8. 典型 Heartbeat 使用场景

| 场景 | 调度 | 效果 |
|------|------|------|
| **AI 日报** | 每天 07:00 | 自动抓取 arXiv + HN，生成中文摘要推送 Telegram |
| **竞品监控** | 每周一 | 爬取竞品网站，与上周对比，邮件发送报告 |
| **收件箱管理** | 每 5 分钟 | 自动分类邮件，紧急邮件立即 Telegram 提醒 |
| **日历助手** | 会议前 30 分钟 | 准备会议背景资料，生成议程摘要 |
| **财务监控** | 交易日每 15 分钟 | 监控股票/加密货币异常波动 |
| **网站监控** | 每小时 | 检测关键网站是否宕机 |
| **代码监控** | GitHub Webhook | 新 PR 自动触发代码审查 |
| **学习助手** | 每天 22:00 | 整理今日学习内容，生成知识卡片 |

---

## 9. Heartbeat vs. 传统定时任务

| 维度 | 传统 Cron Job | OpenClaw Heartbeat |
|------|---------------|---------------------|
| **任务定义** | Shell 脚本 / Python 代码 | 自然语言 Markdown |
| **灵活性** | 固定逻辑 | AI 自主决策 |
| **错误处理** | 需要编码 | AI 自动重试/适应 |
| **输出格式** | 固定 | 根据内容自适应 |
| **可维护性** | 需要开发者 | 任何人都能修改 |
| **上下文感知** | 无 | 有（记忆 + 日历 + 偏好）|
| **跨服务编排** | 需要集成代码 | 通过 Skills 自动 |
