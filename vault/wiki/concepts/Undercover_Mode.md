---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [security, privacy, ai-ethics]
aliases: ["Undercover Mode", "隐藏模式", "AI Hiding"]
relates_to:
  - target: "[[Claude Code]]"
    type: implements
  - target: "[[AI Ethics]]"
    type: relates_to
supersedes: null
---

# Undercover Mode

## 概述
[[Undercover Mode]] 是 [[Claude Code]] 中的一个特殊模式，旨在当 [[Anthropic]] 员工向外部开源项目贡献代码时，确保生成的内容不包含任何 [[Anthropic]] 内部信息。

## 关键内容
1. **功能描述**：
   - 屏蔽内部模型代号（Capybara、Tengu、Fennec 等）
   - 隐藏内部 [[Slack]] 频道名称、内部[[仓库]]名称
   - 移除 "[[Claude Code]]" 字样及 [[Anthropic]] 内部术语

2. **关键设计特点**：
   - 有强制启用的选项（[[Environment Variables|环境变量]] `CLAUDE_CODE_UNDERCOVER=1`）
   - 但**没有强制关闭选项**（NO force-OFF）
   - 这是为了防止模型代号泄露的关键保护措施

3. **实现机制**：
   - 在外部构建中，整个 undercover 模块被编译时移除
   - 替换为返回 false 的空函数

4. **伦理争议**：
   - 批评者认为这违反了许多开源社区对 AI 生成内容的披露要求
   - 让 AI 生成的代码在提交时没有任何[[标注]]，仿佛是人类编写
   - [[Anthropic]] 主张他人应[[标注]] AI 生成内容的同时，自己却隐藏 AI 贡献

## 来源
- [[06_security_antidistillation.md]] — Undercover Mode 详细分析

## 相关
- [[Claude Code]] — implements
- [[AI Ethics]] — relates_to