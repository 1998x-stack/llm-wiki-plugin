# GBrain 深度调研 · Artifact 03
# Skills 系统：26 个生产级 Skill 完整解析

> GBrain 的核心哲学：**智能在 Skill 里，不在二进制里**  
> Agent = Package Manager；Skill = 可执行工作流  
> 修改智能 = 编辑 Markdown，不需要重新部署

---

## 1. Skills 架构概述

### 1.1 Skill 是什么

```
传统观念：Skill = 函数/插件/工具调用
GBrain 观念：Skill = 一份完整工作流的 Markdown 文档

Agent 读取 Skill → 理解何时触发、如何执行、质量标准是什么
```

Skill 文件结构：
```markdown
# Skill 名称

## When to Fire（触发时机）
明确定义在什么情况下调用此 skill

## What to Check（前置检查）
执行前需要验证什么

## How to Execute（执行步骤）
详细的步骤序列，可链式调用其他 skill

## Quality Bar（质量标准）
输出结果需满足什么标准才算完成

## How to Chain（与其他 skill 的协作）
如何与其他 skills 组合使用
```

### 1.2 RESOLVER.md — Skill 调度器

位置：`skills/RESOLVER.md`

```markdown
# Skill Resolver

用户想要记住某件事 → brain-ops/SKILL.md
有新的人/公司被提及 → entity-detection/SKILL.md
需要导入文档 → ingest/SKILL.md
需要丰富某人的信息 → enrich/SKILL.md
早上起来需要简报 → briefing/SKILL.md
发现信息矛盾 → maintenance/SKILL.md
...
```

Agent 在处理任务前先读 RESOLVER，找到对应 skill，再执行。

### 1.3 Thin Harness, Fat Skills

```
gbrain (二进制)
│
├── CLI 命令层（极薄）
│   └── 解析参数 → 调用 engine
│
├── PostgresEngine（数据层）
│   └── search / get / put / sync / embed
│       这些是确定性代码，不能交给 LLM
│
└── Skills（智能层，Fat）
    └── 40+ Markdown 文件
        判断、工作流、质量标准都在这里
        可以不重新部署就修改
```

---

## 2. 核心 Skill 分类（26 个，按类别）

### 类别 A：Brain 操作 Skill（每次消息必触发）

---

#### A1. `signal-detector` — 信号检测器

**重要性**：⭐⭐⭐⭐⭐（最高优先级，每条消息都运行）

**触发条件**：每一条入站消息，无例外。

**工作流**：
```
1. 对消息内容启动廉价模型（Claude Sonnet/Haiku）
2. 双路并行检测：
   路径A：原创想法检测
   路径B：实体提及检测
3. 异步写入 brain，不阻塞主响应
```

**原创想法检测（最高价值）**：
```
捕获条件：用户的观察、论点、框架、哲学思考
关键规则：捕获用户的精确措辞，不要改写
       "The ambition-to-lifespan ratio has never been more broken"
       比 "ambition vs mortality tension" 包含更多信息

路由规则：
  用户自创的想法 → originals/{slug}.md
  用户引用的世界概念 → concepts/{slug}.md
  产品/商业想法 → ideas/{slug}.md
  个人反思 → personal/reflections/
```

**实体提及检测**：
```
对每个被提及的实体：
1. gbrain search "name" 检查是否存在
2. 不存在 + 值得关注 → 创建 stub 页面 + 触发后台丰富
3. 存在但信息少 → 触发后台丰富
4. 存在信息丰富 → 静默加载为上下文
5. 已知实体的新信息 → 追加 timeline
6. 铁律：建立从实体页面 → 来源页面的反向链接
```

---

#### A2. `brain-ops` — Brain 操作核心

**触发条件**：每次响应前的默认检查。

**核心原则**：Brain 优先，外部 API 是后备。

```
收到问题
  │
  ▼
gbrain search "{核心实体/概念}"
  │
  ├── 有结果 → 用 brain context 回答
  │   │
  │   └── 如有新信息 → 更新 page
  │
  └── 无结果 → 考虑外部 API（Brave Search / Crustdata）
               用外部数据更新 brain
               下次同样问题直接命中 brain
```

---

#### A3. `ingest` — 文档摄取

**适用场景**：导入会议记录、文章、邮件、推文等原始资料。

**执行流程**：
```
原始文档输入
  │
  ▼
1. 识别文档类型（meeting/article/email/transcript）
2. 提取所有实体提及
3. 对每个已知实体：
   - 追加 timeline 条目（发生了什么）
   - 更新 compiled truth（如信息更改了认知）
4. 创建新实体 stub（如提及未知人/公司）
5. 建立双向链接
6. 写入 brain page（源文档存档）
7. gbrain sync --no-pull --no-embed（立即可搜索）
```

**质量标准**：
- 每个事实必须有引用（来源 slug）
- 不允许无来源的 compiled truth 更新
- Timeline 条目必须带日期

---

### 类别 B：实体管理 Skill

---

#### B1. `entity-detection` — 实体检测

**详细检测规则**：

| 实体类型 | 存储位置 | Tier 判定 |
|---------|---------|---------|
| 人物 | `people/{slug}.md` | 1次→T3, 3次→T2, 会议→T1 |
| 公司 | `companies/{slug}.md` | 1次→T3, 3次→T2, 交易→T1 |
| 概念/框架 | `concepts/{slug}.md` | 每次提及 |
| 媒体作品 | `sources/{slug}.md` | 每次提及 |

**反向链接规则**（铁律，不得违反）：
```markdown
<!-- 在实体页 people/jane-chen.md 的 Timeline 中 -->
- **2025-04-10** | Referenced in [board-prep-2025-03](meetings/board-prep-2025-03.md) 
                   -- 讨论了定价策略分歧
```

---

#### B2. `enrich` — 实体丰富

**三层自动升级系统**：
```
Tier 3 (Stub)
  slug + 基本提及信息
  触发条件：首次提及
  自动升级：跨3个不同来源提及后 → Tier 2

Tier 2 (Web + Social 丰富)
  + LinkedIn/Twitter 信息
  + 公司背景
  + 近期公开动态
  数据来源：Crustdata / Happenstance / Exa APIs
  自动升级：有会议记录 OR 8次以上提及 → Tier 1

Tier 1 (完整 Pipeline)
  + 完整履历
  + 投资历史（人物）/ 融资历史（公司）
  + 相关网络（合伙人、共同投资人等）
  + 重写 compiled truth 整合所有信息
```

**数据来源优先级**：
```
1. 用户的直接陈述（最高权威）
2. Brain 现有页面中的引用
3. 外部 API（Crustdata/Happenstance/Exa）
```

---

### 类别 C：维护 Skill

---

#### C1. `maintenance` — Brain 维护

**运行时机**：夜间 Dream Cycle（每晚自动运行）

**检查项目**：
```
1. 矛盾检测
   扫描 compiled truth，找出相互矛盾的事实
   → 标记为待解决，创建 conflict/{slug}.md

2. 陈旧信息
   超过 N 天未更新的高 Tier 实体
   → 触发 Tier 1 重新丰富

3. 孤儿页面
   没有任何入站链接的页面
   → 检查是否遗漏了关联

4. 死链接
   指向不存在 slug 的链接
   → 修复或删除

5. 标签不一致
   同一概念使用不同标签
   → 标准化标签

6. 引用修复
   没有引用来源的 compiled truth 陈述
   → 添加引用或降级为观点
```

---

#### C2. `memory-consolidation` — 记忆整合

**夜间 Dream Cycle 核心任务**：
```
扫描当天新增的所有 timeline 条目
  │
  ▼
聚类相关条目
  │
  ▼
重写受影响实体的 compiled truth
  │
  ▼
如有足够新证据 → 触发升级（T3→T2, T2→T1）
  │
  ▼
提取新出现的实体
  │
  ▼
生成引用格式修正
  │
  ▼
运行 gbrain extract links 更新知识图谱
```

---

### 类别 D：报告 Skill

---

#### D1. `briefing` — 简报生成

**触发命令**：
```
"Prep me for my meeting with Jordan in 30 minutes"
"Give me a morning briefing"
"What do I need to know before the board meeting?"
```

**简报内容**：

*会议前简报*：
```markdown
## Jordan 简报 @ 2025-04-22 14:00

### 关键背景
[从 people/jordan-xxx.md 提取 compiled truth]

### 共同历史
[从 brain 中搜索所有我们共同参与的会议]

### 近期动态
[Timeline 最新条目]

### 待跟进事项
[之前会议中标记为 open threads 的内容]

### 相关公司/人脉
[Jordan 的知识图谱邻居]
```

*晨间简报*：
```markdown
## 晨间简报 @ 2025-04-22

### 今日日程
[从 Calendar integration 拉取]

### 每位参会者背景速览
[batch 查询所有参会者的 brain pages]

### 活跃交易状态
[companies 中 status=active-deal 的实体]

### 待处理线索
[timeline 中 status=open 的条目]
```

---

#### D2. `weekly-report` — 周报生成

自动汇总：
- 新增 brain pages 数量及分类
- 新实体（人/公司/概念）
- 重大 compiled truth 更新
- Cron 运行状态
- Brain 健康指标趋势

---

### 类别 E：迁移 Skill

#### E1. `migrate` — 知识迁移

**支持的来源格式**：

| 来源 | 处理策略 |
|------|---------|
| **Obsidian** | 转换 `[[wikilink]]` 格式，保留标签 |
| **Notion** | 导出 markdown，处理数据库关联 |
| **Logseq** | 处理 block 引用和缩进结构 |
| **Roam Research** | 转换双括号链接 |
| **纯 Markdown** | 直接导入，检测类型 |
| **CSV** | 批量导入结构化实体数据 |
| **JSON** | 解析自定义数据结构 |

**迁移流程**：
```
源格式检测
  │
  ▼
格式转换（保留元数据）
  │
  ▼
MECE 目录结构重组
  │
  ▼
链接格式统一化
  │
  ▼
初始实体提取
  │
  ▼
gbrain import --no-embed（快速导入）
  │
  ▼
gbrain embed --stale（后台向量化）
```

---

### 类别 F：身份 & 配置 Skill

---

#### F1. `identity-setup` — Agent 身份配置

gbrain init 时生成 4 个核心文件：

```
SOUL.md     — Agent 身份定义
              "你是谁，你代表谁，你的风格是什么"

USER.md     — 用户档案
              "这个 brain 属于谁，他们的背景、目标、偏好"

ACCESS_POLICY.md — 访问策略
              "谁可以查询这个 brain，哪些信息是私密的"

HEARTBEAT.md — 操作节奏
              "Cron 调度节奏，每日/每周/每月的例行任务"
```

---

#### F2. `subagent-routing` — 子 Agent 路由（v0.11.0+）

```
调度后台工作时 → 读取 subagent-routing.md
  │
  ├── 读取 ~/.gbrain/preferences.json#minion_mode
  │
  ├── minion_mode = "native" → 使用 OpenClaw 原生子 Agent
  │
  └── minion_mode = "minion" → 使用 Minion jobs（持久化任务队列）
```

---

### 类别 G：Cron 相关 Skill

#### G1. `cron-via-minions` — Cron 任务 via Minions

v0.11.0 起，所有定时任务通过 Minion 而非直接 agentTurn 执行。

**Minion 任务队列特性**：
```
✓ 任务存活：跨 gateway 重启不丢失
✓ 流式进度：实时查看任务执行进度
✓ 暂停/恢复：支持中途干预
✓ 转向控制：可以在运行中修改任务方向
✓ gbrain jobs：可视化所有任务状态
```

---

## 3. RESOLVER.md 完整路由示例

```markdown
# GBrain Skill Resolver

## 消息类路由
- 任何入站消息 → signal-detector + brain-ops（并行）
- "记住..." / "别忘了..." → brain-ops#write
- "搜索..." / "查找..." → brain-ops#search
- "准备一下和...的会议" → briefing
- "今天的简报" → briefing#morning

## 实体类路由
- 提到未知人物 → entity-detection → enrich
- 提到未知公司 → entity-detection → enrich
- 提到概念/框架 → entity-detection → concepts
- 发现矛盾信息 → maintenance#conflict

## 文档类路由
- 粘贴会议记录 → ingest#meeting
- 粘贴文章链接 → ingest#article
- 粘贴邮件 → ingest#email
- 上传通话记录 → ingest#transcript（voice-to-brain）

## 迁移类路由
- "导入我的 Obsidian 库" → migrate#obsidian
- "从 Notion 迁移" → migrate#notion

## 维护类路由
- 夜间 Dream Cycle → maintenance + memory-consolidation + report#weekly
- 发现孤儿页面 → maintenance#orphans
- 发现死链接 → maintenance#dead-links

## 代码类路由
- 任何代码任务 → 先检查 brain，再路由到 GStack
  hosts/gbrain.ts 处理这个桥接
```

---

## 4. 最重要的 3 个 Skill（安装后立即掌握）

按照 INSTALL_FOR_AGENTS.md 的建议：

```
优先级 1: signal-detector
  原因：fire on EVERY message。没有它，大脑不会增长。
  效果：每次对话都在悄悄往大脑里写知识。

优先级 2: brain-ops
  原因：每次响应前先查 brain。没有它，知识存而不用。
  效果：回答变得更有深度，因为有历史上下文。

优先级 3: brain-agent-loop
  原因：理解整体 Read-Detect-Write 循环。
  效果：让以上两个 skill 形成飞轮，而不是孤立运行。
```

---

## 5. Skill 开发指南

### 5.1 编写新 Skill 的原则

```
1. 触发条件要精确
   不好：when the user needs something
   好：when the user says "prep me for meeting with X"

2. 步骤要可验证
   每步都应该有明确的成功标准

3. 调用 gbrain 命令而非描述意图
   不好：search the brain for relevant info
   好：gbrain search "{entity}" | gbrain get {slug}

4. 质量栏要可测量
   不好：output should be good
   好：every fact must have a citation in format [source](path)

5. 链式调用要显式
   说明哪些情况下应该调用其他哪些 skills
```

### 5.2 Skill 测试框架

```bash
# 验证 skill 触发正确
gbrain test-skill signal-detector --input "I met Sarah today, she works at OpenAI"
# 期望：在 people/ 下创建 sarah 的 stub 页面

# 验证 brain-ops 正常
gbrain test-skill brain-ops --query "who is Sarah?"
# 期望：返回 sarah 的 brain page（如存在）
```

---

*下一篇：[Artifact 04 - GBrain 集成系统与 Cron 体系]*
