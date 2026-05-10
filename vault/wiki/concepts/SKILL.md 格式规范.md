---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["skill-format", "markdown", "standard", "SKILL.md", "工具与框架"]
aliases: [SKILL.md, Skill Format Specification]
relates_to:
  - Hermes Agent
  - agentskills.io
  - 开放技能标准
  - 渐进式加载
  - 条件激活机制
supersedes: null
---

# SKILL.md 格式规范

## 概述
定义 AI Agent [[Skills|技能]]文档的标准格式，包含 frontmatter 元数据和工作流正文，是 [[agentskills.io]] 开放标准的核心载体。

## 关键内容
- **Frontmatter 关键字段**：`name`（唯一标识符，也是[[斜杠命令（Slash Commands）|斜杠命令]]名称）、`description`（Level 0 目录展示内容，是 Agent 决定是否加载[[Skills|技能]]的唯一依据）、`version`（语义化版本，Agent 自我改进时递增）、`platforms`（不匹配时[[Skills|技能]]完全隐藏）、`category`（Level 0 目录分类展示）、`config`（声明非密钥[[Configuration|配置]]项，存入 config.yaml 自动注入）
- **安全[[Configuration|配置]]**：`required_environment_variables` 声明所需[[Environment Variables|环境变量]]，[[Skills|技能]]不会因缺少它们而隐藏，首次加载时自动弹出[[Configuration|配置]]提示
- **[[条件激活机制|条件激活]]字段**：`fallback_for_toolsets`、`fallback_for_tools`、`requires_toolsets`、`requires_tools` 控制[[Skills|技能]]根据工具可用性自动显示或隐藏
- **正文结构**：When to Use（何时使用）→ Prerequisites（前提条件）→ Procedure（步骤）→ Rollback（回滚）→ Pitfalls（常见问题）→ Verification（验证）
- **目录结构**：`~/.hermes/skills/<category>/<skill-name>/SKILL.md`，可包含 `examples/` 和 `reference/` 子目录供 Level 2 加载
- **[[斜杠命令（Slash Commands）|斜杠命令]]映射**：每个已安装的[[Skills|技能]]自动成为[[斜杠命令（Slash Commands）|斜杠命令]]，如 `/deploy-to-k8s`

## 来源
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — 2026 年 4 月版本，Hermes Agent 深度解析第四篇

## 相关
- [[Hermes Agent]] — implements
- [[agentskills.io]] — implements
- [[开放技能标准]] — part_of
- [[渐进式加载]] — extends
- [[条件激活机制]] — extends
