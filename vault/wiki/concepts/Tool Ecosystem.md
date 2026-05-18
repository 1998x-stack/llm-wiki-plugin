---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, claude-code, tool-system, AI工程]
aliases: ["工具生态系统", "Tool System"]
relates_to: []
supersedes: null
---

# Tool Ecosystem

## 概述
[[Claude Code]]的工具生态系统设计理念：使用4个通用基元替代100个脆弱的专用插件集成，Bash作为终极[[Bash通用适配器|通用适配器]]。

## 关键内容

1. **设计哲学**：
   - **Primitives > Integrations**：用4个通用基元替代100个脆弱的专用插件集成
   - **Bash是终极[[Bash通用适配器|通用适配器]]**：任何CLI工具都可通过它调用

2. **工具调用数据流**：
   - LLM输出JSON Tool Call（tool_name + tool_input）
   - 经过[[Tool Hook Mechanism|PreToolUse Hook]]检查
   - 在[[Claude Code 沙箱机制|沙箱]]执行环境中运行（带[[Permissions|权限]]白名单检查）
   - 结果以纯文本返回
   - 通过[[Tool Hook Mechanism|PostToolUse Hook]]进行质量检查
   - 最终追加到消息历史

3. **统一接口**：所有工具遵循**JSON in → 纯文本 out**的统一接口

## 来源
- [[03 · 工具生态系统（Tool Ecosystem）]] — 源文件

## 相关
- [[BashTool]] — 关联工具
- [[Tool System]] — 相关概念