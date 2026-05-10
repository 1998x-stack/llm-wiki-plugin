---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, claude-code, tool-system, security]
aliases: ["安全过滤层", "Security Filter Layer"]
relates_to: []
supersedes: null
---

# Security Filter Layer

## 概述
[[Claude Code]]中用于防止命令注入的安全过滤机制，采用确定性检测而非LLM判断，确保所有潜在恶意命令被准确拦截。

## 关键内容

1. **注入检测模式**：
   - 检测`命令替换符号
   - 检测$(命令替换符号
   - 检测${变量替换攻击
   - 检测$(算术扩展符号

2. **确定性拦截**：
   - 安全过滤层不依赖LLM判断
   - 采用预定义模式列表进行确定性检测
   - 发现注入模式时直接抛出SecurityError异常

3. **实现原理**：
   - 系统维护INJECTION_PATTERNS列表
   - 对输入命令逐项检查是否包含潜在注入模式
   - 检测到时立即阻止执行并报告具体模式

## 来源
- [[03 · 工具生态系统（Tool Ecosystem）]] — 安全过滤部分

## 相关
- [[Tool Ecosystem]] — 所属系统
- [[BashTool]] — 应用场景