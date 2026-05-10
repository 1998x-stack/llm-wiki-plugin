---
type: entity
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["skill-standard", "open-source", "agent", "工具与框架"]
aliases: [Agent Skills]
relates_to:
  - Hermes Agent
  - 开放技能标准
  - SKILL.md 格式规范
  - OpenClaw
supersedes: null
---

# agentskills.io

## 概述
开放的 AI Agent [[Skills|技能]]标准规范，定义 [[Agent Skills|Skills]] 为纯文本 Markdown 文件，支持 Git 管理、社区共享和跨平台迁移。

## 关键内容
- **核心定位**：开放的 AI Agent [[Skills|技能]]标准规范，由 agentskills.io 社区维护
- **[[Skills|技能]]格式**：[[Agent Skills|Skills]] 是纯文本 Markdown 文件（[[SKILL.md 格式规范|SKILL.md]]），可 Git 管理、版本控制
- **可移植性**：[[Skills|技能]]可在不同 Agent 框架间迁移，[[OpenClaw]] skill → [[Hermes Agent|Hermes]] skill 双向兼容
- **社区生态**：通过 [[Agent Skills|Skills]] Hub 社区贡献和安装[[Skills|技能]]，`hermes skills hub search/install` 操作，[[Skills|技能]]经过 [[Agent Skills|Skills]] Hub 审核，可用 `hermes skills update` 更新到最新版
- **[[Hermes Agent|Hermes]] 集成**：[[Hermes Agent]] 遵循此开放标准，支持 [[Agent Skills|Skills]] Hub 安装和 [[OpenClaw]] 迁移
- **[[SKILL.md 格式规范|SKILL.md]] 格式**：定义标准 frontmatter（name, description, version, platforms, category, config, required_environment_variables）和正文结构（When to Use, Prerequisites, Procedure, Pitfalls, Verification）

## 来源
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — 2026 年 4 月版本
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — 2026 年 4 月版本，Hermes Agent 深度解析第四篇：Skills 系统

## 相关
- [[Hermes Agent]] — implements
- [[开放技能标准]] — implements
- [[自我进化代理]] — extends
- [[SKILL.md 格式规范]] — implements
- [[OpenClaw]] — compares_to
