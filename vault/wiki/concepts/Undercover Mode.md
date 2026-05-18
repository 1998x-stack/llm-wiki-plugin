---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [security, anti-distillation, ai-systems, AI工程]
aliases: ["Undercover Mode", "卧底模式"]
relates_to: 
  - target: "[[Claude Code]]"
    type: implemented_in
    confidence: 0.8
  - target: "[[Anthropic]]"
    type: developed_by
    confidence: 0.7
  - target: "[[Source Map 泄露事件]]"
    type: ironic_failure
    confidence: 0.9
supersedes: null
---

# Undercover Mode

## 概述
Undercover Mode（卧底模式）是 [[Anthropic]] 为 [[Claude Code]] 设计的内部信息泄露防护系统，旨在防止 AI 在 [[Git Commit|git commit]] 等操作中暴露内部代号和其他敏感信息。

## 关键内容

1. **设计目的**：
   - 防止 AI 在提交代码时暴露内部代号、秘密常量或其他敏感信息
   - 阻止内部模型代号和系统提示词泄露到公共[[仓库]]
   - 防止在日志、注释或其他元数据中泄露内部系统细节

2. **应用场景**：
   - 代码提交检查
   - 日志过滤
   - 输出审查
   - 生成内容过滤

3. **讽刺的失效**：
   - [[Anthropic]] 花费大量工程精力阻止 AI 在 [[Git Commit|git commit]] 里暴露内部代号
   - 但却通过 npm 包中的 [[Source Map]] 文件将整个源码连同内部代号和提示词完全泄露出去
   - 这成为 [[Source Map 泄露事件]]中最具有讽刺意味的部分

## 来源
- [[01_overview_architecture]] — 系统介绍及失效分析

## 相关
- [[Claude Code]] — implemented_in
- [[Source Map 泄露事件]] — ironic_failure
- [[Anthropic]] — developed_by