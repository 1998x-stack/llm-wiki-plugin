# OpenClaw ④ SKILLS — 插件能力体系 & ClawHub 市场

> Skills 是 OpenClaw 的"双手"——让 Agent 获得特定领域能力的可插拔模块。  
> 核心设计：**一个文件夹 + 一个 SKILL.md = 一种新能力**

---

## 1. Skills 系统总览

```
┌─────────────────────────────────────────────────────────┐
│                   Skills 生态系统                         │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │  ClawHub 市场（5,700+ 社区 Skills）             │    │
│  │  ├─ 搜索 / 自动拉取                             │    │
│  │  ├─ 版本管理                                    │    │
│  │  └─ 作者评分 / 安全审计                         │    │
│  └─────────────────────────────────────────────────┘    │
│                          │                               │
│                    自动下载 SKILL.md                     │
│                          │                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │  本地 Skills 目录（/workspace/skills/）          │    │
│  │  ├─ github-reviewer/ → SKILL.md                 │    │
│  │  ├─ email-digest/    → SKILL.md                 │    │
│  │  ├─ web-scraper/     → SKILL.md + tools.yaml    │    │
│  │  └─ ...                                         │    │
│  └─────────────────────────────────────────────────┘    │
│                          │                               │
│              System Prompt Builder 注入索引              │
│                          │                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Agent Brain（按需懒加载全文）                   │    │
│  │  用户请求 → LLM 判断需要哪个 Skill →            │    │
│  │  读取 SKILL.md 全文 → 执行能力                  │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## 2. SKILL.md 结构规范

每个 Skill 的核心是一个 `SKILL.md` 文件，包含：

```markdown
---
name: github-pr-reviewer
description: 审查 GitHub Pull Request 并提交代码审阅意见
version: 1.2.0
author: community
requires_tools: [web_fetch, shell_exec]
tags: [github, code-review, development]
---

# GitHub PR Reviewer

## 功能说明
当用户要求审查 Pull Request 时，执行以下流程：

## 执行步骤

1. **获取 PR 信息**
   - 使用 `web_fetch` 工具拉取 PR 差异（diff）
   - URL 格式：`https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}`
   - 需要 GitHub Token（从环境变量读取）

2. **分析代码**
   - 检查：正确性、安全漏洞、代码风格、性能
   - 必须标记：阻塞性问题 vs. 建议性改进

3. **输出格式**
   ```
   ## PR 审阅报告
   
   ### 执行摘要
   [1-2句总结]
   
   ### 阻塞性问题（必须修复）
   - [ ] ...
   
   ### 改进建议（可选）
   - [ ] ...
   
   ### 总体评价
   [Approve / Request Changes / Comment]
   ```

4. **提交审阅**（仅当用户明确要求时）
   - 调用 GitHub API 提交 Review
   - 状态：`APPROVE` / `REQUEST_CHANGES` / `COMMENT`

## 注意事项
- 始终保持建设性，批评具体行为而非人
- 对安全漏洞单独置顶警告
- 不要审阅生成的代码（如 package-lock.json）

## 示例触发语
- "帮我看一下这个 PR：[URL]"
- "Review PR #42 in my-org/my-repo"
- "这个 Pull Request 有什么问题？"
```

---

## 3. Skills 注入机制详解

### 3.1 两阶段注入策略

```
阶段一：索引注入（每次 Agent 启动时）
────────────────────────────────────────
扫描 /workspace/skills/ 目录
    │
    ▼
生成紧凑索引（Skills Prompt）：

Available Skills:
- github-pr-reviewer: 审查 GitHub PR，提交代码审阅
  Path: /workspace/skills/github-pr-reviewer/SKILL.md
- email-digest: 整理邮件摘要，按优先级排序
  Path: /workspace/skills/email-digest/SKILL.md
- web-scraper: 爬取网页内容，支持 JS 渲染页面
  Path: /workspace/skills/web-scraper/SKILL.md
...（仅 name + description + path）

    │
    ▼
注入 System Prompt Layer 2

Token 消耗：每个 Skill 约 20-30 tokens（仅索引）
vs. 全文注入：每个 Skill 约 500-2000 tokens
节约比例：95%+
```

```
阶段二：按需懒加载（用户请求触发时）
────────────────────────────────────────
用户："帮我 Review 这个 PR"
    │
    ▼
LLM 识别需要 github-pr-reviewer Skill
    │
    ▼
调用 file_read 工具读取完整 SKILL.md
    │
    ▼
SKILL.md 全文注入当前 context
    │
    ▼
LLM 按照 SKILL.md 指令执行任务
```

---

## 4. Skill 类型分类

### 4.1 纯指令型 Skill（最简单）

只有 SKILL.md，定义自然语言操作流程：

```
/skills/competitive-analysis/
└── SKILL.md    # 纯 Markdown 指令，无额外配置
```

适用：数据分析、报告生成、内容写作等

---

### 4.2 工具配置型 Skill

包含工具配置文件：

```
/skills/web-scraper/
├── SKILL.md         # 操作指令
└── tools.yaml       # 工具配置（Puppeteer/FireCrawl 参数）
```

**tools.yaml 示例：**
```yaml
tools:
  - name: web_scrape
    engine: puppeteer          # 或 firecrawl
    js_rendering: true
    wait_for: 2000             # 等待 JS 渲染（ms）
    extract_selectors:
      - "article.content"
      - "div.main-text"
    output_format: markdown
```

---

### 4.3 API 集成型 Skill

包含 API 认证和调用配置：

```
/skills/gmail-digest/
├── SKILL.md
├── tools.yaml
└── auth.yaml        # 认证方式（从系统 Keychain 读取）
```

**auth.yaml 示例：**
```yaml
credentials:
  - name: GMAIL_OAUTH_TOKEN
    source: keychain           # 从系统 Keychain 安全读取
    required: true
  - name: GMAIL_CLIENT_ID
    source: env                # 从环境变量读取
```

---

### 4.4 MCP 集成型 Skill

通过 MCP（Model Context Protocol）接入外部服务：

```
/skills/github-mcp/
├── SKILL.md
└── mcp.yaml         # MCP 服务器配置
```

**mcp.yaml 示例：**
```yaml
mcp_servers:
  - name: github
    url: https://github.mcp.example.com/sse
    description: GitHub repository operations
    auth:
      type: bearer
      token_from: keychain:GITHUB_PAT
```

---

## 5. ClawHub — Skills 市场

### 5.1 ClawHub 概览

<table>
<tr><th>指标</th><th>数据（2026年3月）</th></tr>
<tr><td>社区 Skills 总数</td><td>5,700+</td></tr>
<tr><td>分类数</td><td>50+</td></tr>
<tr><td>日活跃安装量</td><td>数万次</td></tr>
<tr><td>安全审计覆盖率</td><td>进行中（Cisco 研究警示见安全章节）</td></tr>
</table>

### 5.2 热门 Skill 分类

| 类别 | 示例 Skills |
|------|-------------|
| **开发工具** | github-pr-reviewer, jira-updater, ci-monitor |
| **内容生产** | blog-writer, social-media-poster, newsletter-generator |
| **数据分析** | hacker-news-digest, market-analyzer, spreadsheet-processor |
| **效率自动化** | email-classifier, calendar-optimizer, meeting-notes |
| **生活助手** | recipe-planner, travel-researcher, finance-tracker |
| **AI 增强** | image-generator, voice-transcriber, translation-engine |
| **专业领域** | legal-draft-assistant, medical-note-formatter, code-reviewer |

### 5.3 自动安装机制

```
用户："帮我设置一个每日 Hacker News 摘要"
    │
    ▼
Agent 识别需要 hacker-news-digest Skill
    │
    ▼
ClawHub 搜索（Agent 自动调用）：
  GET https://clawhub.io/api/search?q=hacker-news-digest
    │
    ▼
返回匹配 Skill 列表 + 描述
    │
    ▼
用户确认安装 → Agent 拉取 SKILL.md 到本地
    │
    ▼
立即可用，无需重启 Gateway
```

---

## 6. 编写高质量 SKILL.md 的最佳实践

### 6.1 触发语设计

```markdown
## 示例触发语
- "分析这个月的销售数据"       ← 明确场景
- "做一份竞品分析报告"         ← 任务驱动
- "summarize today's news"     ← 英文场景
- "帮我看一下这个 PR：[URL]"  ← 含参数提示

❌ 避免过于宽泛的触发语（如"分析"、"帮我做"）
✅ 要有具体的场景和输出物描述
```

### 6.2 步骤清晰度

```markdown
❌ 差的写法：
"分析数据并给出结论"

✅ 好的写法：
1. 使用 file_read 读取 /workspace/data/ 下的 CSV
2. 统计关键指标：均值、方差、异常值（±2σ）
3. 生成趋势图（调用 code_exec 工具，输出 PNG）
4. 撰写报告，格式：执行摘要 → 详细分析 → 行动建议
5. 报告保存至 /workspace/reports/YYYY-MM-DD-analysis.md
```

### 6.3 错误处理指导

```markdown
## 错误处理
- 文件不存在：提示用户检查路径，询问是否创建示例文件
- API 超时：等待 5 秒后重试一次，失败则报告错误
- 权限拒绝：提示用户检查 API Key 配置
- 数据为空：返回"未找到数据"，不要捏造结果
```

---

## 7. Skills 安全注意事项

⚠️ **来自 Cisco 研究（2026 年）的警告：**
> 26% 的社区 Skills 存在至少一个安全漏洞

**安全使用规范：**

| 规范 | 说明 |
|------|------|
| **审计 SKILL.md 内容** | 安装前阅读完整指令，检查是否有可疑的工具调用 |
| **沙箱化 shell_exec** | 限制 Shell 权限，不要以 root 运行 |
| **验证 API 调用目标** | 检查 SKILL.md 中所有外部 URL 的合法性 |
| **Pin 版本** | 锁定已审计的 Skill 版本，避免自动升级引入恶意更改 |
| **不可逆操作确认** | 发邮件、删除文件、支付等操作必须人工确认 |

---

## 8. 与 Claude Skills（Anthropic）对比

| 维度 | OpenClaw Skills | Claude Skills（Anthropic）|
|------|-----------------|--------------------------|
| **本质** | 完整 Agent 能力插件 | LLM 单一能力扩展 |
| **自主性** | 主动执行，无需触发 | 被动响应，需用户触发 |
| **数据隐私** | 完全本地 | 云端处理 |
| **可定制性** | 完全自定义（Markdown）| 受平台约束 |
| **市场规模** | 5,700+ 社区 Skills | 平台管理 |
| **编程门槛** | 写 Markdown 即可 | 需了解 API 规范 |
