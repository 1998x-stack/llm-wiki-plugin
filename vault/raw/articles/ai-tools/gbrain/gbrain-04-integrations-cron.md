# GBrain 深度调研 · Artifact 04
# 集成系统 (Integrations) 与 Cron 自动化体系

> 覆盖：Integration Recipes 架构 · 6大集成管道 · Cron 调度体系 · 
> Dream Cycle · Minion 任务队列 · 健康监控

---

## 1. 集成系统架构概述

### 1.1 设计哲学

```
传统集成思路：写代码 → 配置 → 部署 → 维护
GBrain 集成思路：Agent 读 Recipe → Agent 执行安装 → Recipe 即是代码
```

信号流方向：
```
信号到达（电话 / 邮件 / 推文 / 日历事件）
        │
        ▼
Collector 捕获（确定性代码，可靠）
        │
        ▼
Agent 分析（LLM，判断，实体检测）
        │
        ▼
Brain pages 创建/更新（compiled truth + timeline）
        │
        ▼
GBrain 索引（分块，嵌入，可搜索）
        │
        ▼
下次查询更智能（复利效应）
```

### 1.2 Recipe 文件格式

每个集成是一个带 YAML frontmatter 的 Markdown 文件：

```yaml
---
id: voice-to-brain              # 唯一标识
name: Voice-to-Brain            # 人类可读名称
version: 0.7.0                  # Recipe 版本
description: 电话通话创建 brain pages
category: sense                 # sense（输入）| reflex（自动响应）
requires: [credential-gateway]  # 依赖的其他 recipes
secrets:
  - name: TWILIO_ACCOUNT_SID
    description: Twilio 账号 SID
    where: https://console.twilio.com
  - name: OPENAI_API_KEY
    description: OpenAI API key（用于 Realtime 语音）
    where: https://platform.openai.com/api-keys
health_checks:
  - curl -s https://api.twilio.com/2010-04-01 > /dev/null
  - curl -s https://api.openai.com/v1/models > /dev/null
setup_time: 30 min
---

[Agent 执行的安装指令 markdown 正文...]
```

### 1.3 依赖解析（类 Homebrew）

```
gbrain init（根节点）
├── credential-gateway（凭据网关）
│   ├── voice-to-brain（需要 Twilio 凭据）
│   ├── email-to-brain（需要 Gmail 凭据）
│   └── calendar-to-brain（需要 Google Calendar 凭据）
└── x-to-brain（独立，直接使用 X API）
```

CLI 在安装前自动解析并按序安装所有依赖。

### 1.4 安全模型

```
信任来源分类：
  ✓ 包内置 Recipe（gbrain 源码中的 recipes/）
    → 完全信任，可运行 HTTP/Command 健康检查

  ⚠ 用户本地 Recipe（$GBRAIN_RECIPES_DIR 或 ./recipes/）
    → 不信任标记，限制如下：
    - 不能运行 command health checks
    - 不能运行 http health checks（防 SSRF）
    - 不能使用 deprecated string health_check 格式

  ✓ env_exists 检查 → 所有 recipe 均可使用
```

---

## 2. 六大核心集成管道

---

### 集成 1：Voice-to-Brain（语音 → 大脑）

**作用**：电话通话实时转录并自动写入 brain pages

**技术栈**：
- Twilio（电话路由）
- OpenAI Realtime API（实时语音转录）
- GBrain（存储和索引）

**数据流**：
```
来电到达 Twilio 号码
  │
  ▼
Twilio 路由到 WebRTC 端点
  │
  ▼
OpenAI Realtime API 实时转录
  │
  ▼
Agent 分析通话内容：
  - 提取人物实体
  - 提取公司提及
  - 识别决策和行动项
  │
  ▼
创建 meeting/{date}-call-{person}.md
  │
  ▼
更新相关人物/公司的 compiled truth
  │
  ▼
追加 timeline 条目
```

**生产模式（25 个模式）**：

| 模式 | 描述 |
|------|------|
| 身份分离 | 工作/个人号码分开，brain 写入不同命名空间 |
| 竞价系统 | 多条 incoming 线路时的优先级处理 |
| 对话时机 | 自动判断何时主动发起通话提醒 |
| 主动顾问 | 通话中实时提供 brain context |
| 提示压缩 | 大 brain context 的压缩策略 |
| 来电路由 | 基于来电者身份的路由规则 |
| 动态 VAD | 语音活动检测参数自适应 |
| 实时日志 | 通话中实时写入 brain，不等通话结束 |

---

### 集成 2：Email-to-Brain（邮件 → 大脑）

**作用**：Gmail 邮件自动流入 brain，结构化提取数据

**凭据要求**：
- Gmail OAuth2 凭据
- 依赖 `credential-gateway`

**处理逻辑**：
```
Gmail 收到邮件
  │
  ▼
Cron 每 N 分钟扫描收件箱
  │
  ▼
过滤规则（可配置）：
  - 白名单发件人（重要联系人）
  - 黑名单域名（营销邮件）
  - 主题关键词匹配
  │
  ▼
LLM 解析邮件内容：
  - 发件人实体识别
  - 提取关键信息（融资更新、指标、请求）
  - 识别行动项
  │
  ▼
写入 brain（sources/email/ 或直接更新实体页面）
```

**数据研究 Recipes**：

从邮件中提取结构化数据到跟踪页面：
```
投资者更新 Recipe：
  从投资组合公司的更新邮件提取：
  - MRR / ARR
  - 跑道（Runway）
  - 员工数
  - 关键里程碑
  → 写入 companies/{slug}.md 的 metrics 区块
  → Timeline 追加带日期的指标快照

费用追踪 Recipe：
  从收据邮件提取金额、类别、供应商
  → 写入 finance/expenses.md

公司指标 Recipe：
  用户自定义的指标提取模板
```

---

### 集成 3：Calendar-to-Brain（日历 → 大脑）

**作用**：Google Calendar 事件自动同步为 brain 的会议预期和简报触发器

**数据流**：
```
Calendar 事件创建/更新
  │
  ▼
提取参会者列表
  │
  ▼
批量查询参会者的 brain pages
  │
  ▼
在会议前 30 分钟自动触发 briefing skill
  │
  ▼
会议结束后提示用户上传记录（与 ingest skill 联动）
```

---

### 集成 4：X-to-Brain（推特 → 大脑）

**作用**：Twitter/X 动态流入 brain

**特点**：无需 `credential-gateway`（直接使用 X API）

**监控范围**：
- 关注列表中的账号
- 已知实体（people/companies）的账号
- 特定关键词或话题

**处理策略**：
- 推文本身 → 创建 sources/tweets/{date}-{slug}.md
- 提及已知实体 → 追加 timeline 条目
- 观点/原创想法 → 触发 signal-detector 分析是否需要写入 originals

---

### 集成 5：Credential Gateway（凭据网关）

**作用**：所有需要外部 API 凭据的集成的基础依赖

**职责**：
```
统一管理所有 secrets：
  - 存储位置：~/.gbrain/secrets.json（0600 权限）
  - 验证方式：health_check 配置的命令
  - 刷新机制：OAuth token 自动刷新

为其他 recipes 提供：
  - 凭据注入（不在 recipe 文件中明文写 key）
  - 凭据验证状态
  - 过期提醒
```

---

### 集成 6：Research Recipes（数据研究配方）

**创建自定义研究 Recipe**：
```bash
gbrain research init
```

会引导创建一个自定义的从邮件/文档提取结构化数据的 recipe。

**示例**：
```yaml
---
id: portfolio-metrics
name: Portfolio Company Metrics
description: 从投资组合公司月报邮件提取指标
source: email
extract:
  - field: mrr
    prompt: "提取月度经常性收入，格式 $X,XXX,XXX"
  - field: runway
    prompt: "提取现金跑道，格式 X months"
  - field: headcount
    prompt: "提取员工总数"
destination: companies/{company_slug}
schedule: "0 9 * * 1"  # 每周一早9点
---
```

---

## 3. Cron 自动化体系

### 3.1 推荐 Cron 调度表

```
# 每15分钟 - Live Sync（核心，保持 brain 实时更新）
*/15 * * * *  gbrain sync --repo ~/brain && gbrain embed --stale

# 每日 - 自动检查更新（告知用户，不自动安装）
0 8 * * *     gbrain check-update --json

# 每晚 - Dream Cycle（记忆整合，最重要！）
0 2 * * *     gbrain doctor --json && gbrain embed --stale
              # 然后运行 maintenance + memory-consolidation skills

# 每周 - 完整健康检查
0 9 * * 1     gbrain doctor --json && gbrain embed --stale
              # 运行 weekly-report skill
```

### 3.2 Live Sync 机制

```
gbrain sync --watch --repo <path>
  │
  ├── 前台运行，每60秒轮询（可配置 --interval N）
  ├── 非文件系统 watcher，是轮询
  ├── 连续5次失败后退出（需进程管理器保活）
  └── 增量处理（SHA-256 比对，只处理变更文件）

并发安全：
  两个 sync 同时对同一 commit 运行 → 第二个 no-op
  content hash 保证幂等性
```

**Supabase 连接问题（最常见故障）**：
```
症状：sync ran but nothing happened
原因：DATABASE_URL 使用了 Transaction 模式池
      → .begin() is not a function 错误

修复：
  ✓ 使用 Session 模式池字符串（端口 6543，Session mode）
  ✓ 或使用直连字符串（端口 5432，IPv6-only）
  ✗ 不能用 Transaction 模式（端口 6543，Transaction mode）
```

### 3.3 Dream Cycle（夜间记忆整合）

这是让 brain **自我增长**的核心机制：

```
每晚 2:00 AM 执行
        │
        ▼
STEP 1: gbrain doctor --json
  → 确认系统健康，记录指标趋势
        │
        ▼
STEP 2: gbrain embed --stale
  → 处理白天新增但未向量化的 chunks
        │
        ▼
STEP 3: maintenance skill
  → 扫描矛盾、孤儿、死链接
  → 修复引用格式
  → 标准化标签
        │
        ▼
STEP 4: memory-consolidation skill
  → 聚类当天新增 timeline 条目
  → 重写受影响实体的 compiled truth
  → 触发实体 tier 升级
        │
        ▼
STEP 5: entity enrichment（Tier 升级触发）
  → 调用外部 API 丰富新升至 T2/T1 的实体
        │
        ▼
STEP 6: gbrain extract links --source db
  → 更新知识图谱（提取新页面中的链接）
        │
        ▼
STEP 7: 生成 overnight report
  → 写入 reports/overnight-{date}.md
  → 早上用户醒来时 brain 比昨晚更聪明
```

### 3.4 Minion 任务队列（v0.11.0+）

所有 Cron 任务从 v0.11.0 起通过 Minion 执行：

```
传统 Cron：调用 agentTurn → 如果 gateway 重启，任务丢失
Minion Cron：任务写入持久化队列 → 重启后自动恢复
```

**Minion 生命周期**：
```
QUEUED → RUNNING → STREAMING → DONE
                 ↘ PAUSED（人工干预）
                 ↘ STEERED（修改任务方向）
                 ↘ FAILED（重试）
```

**查看任务状态**：
```bash
gbrain jobs list
# NAME                    STATUS    PROGRESS   STARTED
# dream-cycle-2025-04-22  RUNNING   4/7 steps  02:01
# enrich-sarah-chen       DONE      7/7 steps  01:45
# weekly-report           QUEUED    -          -
```

---

## 4. 集成健康监控

### 4.1 `gbrain integrations doctor` 输出

```bash
$ gbrain integrations doctor

voice-to-brain:
  ✓ Twilio reachable
  ✓ OpenAI key valid
  ✓ ngrok tunnel up

email-to-brain:
  ✓ Gmail auth valid
  ✗ No emails in 48h (check cron)    ← 警告

calendar-to-brain:
  ✓ Google Calendar auth valid
  ✓ Last sync: 12 min ago

x-to-brain:
  ✓ X API reachable
  ✓ Last tweet processed: 3 min ago

credential-gateway:
  ✓ All secrets present
  ✓ No tokens expired

OVERALL: 1 warning (email-to-brain: no recent emails)
```

### 4.2 集成状态追踪

```bash
gbrain integrations list
# ID                STATUS    LAST_RUN         RECIPE_VERSION
# voice-to-brain    active    2025-04-22 14:23  0.7.0
# email-to-brain    warning   2025-04-20 09:01  0.5.2
# calendar-to-brain active    2025-04-22 14:15  0.3.1
# x-to-brain        active    2025-04-22 14:20  0.4.0
```

---

## 5. 版本迁移注意事项

### v0.11.0 迁移

```
自动迁移：
  - AGENTS.md 自动注入 subagent-routing.md 的指针
  - Cron handler 为内置命令的条目自动重写

手动迁移：
  - host-specific handlers（如 ea-inbox-sweep）需要按
    docs/guides/plugin-handlers.md 手动注册
```

### v0.12.0 迁移

```
如果 brain 创建于 v0.12.0 之前，必须运行：
gbrain extract links --source db
gbrain extract timeline --source db
→ 回填新的图谱层
```

### v0.12.2 迁移

```
Postgres/Supabase-backed brain 且早于 v0.12.2：
gbrain post-upgrade  # 自动运行 repair-jsonb 修复 double-encoding 问题
```

---

## 6. "大脑即基础设施操作系统"愿景

GBrain 的长期设计意图（来自 `HOMEBREW_FOR_PERSONAL_AI.md`）：

```
GBrain 成为个人基础设施操作系统
生命中每一个信号都自动流经大脑

Integrations = Senses（感官输入）
             + Reflexes（对模式的自动响应）

用户订阅创建者（Garry Tan）的实际操作系统
然后根据自己的情况定制

用户感受：
"我的大脑是活的。它在关注我在乎的一切，
每天都在变得更聪明。我不需要写任何代码。
当 Agent 问我时，我只是说了'是'。"
```

---

*下一篇：[Artifact 05 - GBrain 工程实践指南：安装、推荐 Schema、调试与演进]*
