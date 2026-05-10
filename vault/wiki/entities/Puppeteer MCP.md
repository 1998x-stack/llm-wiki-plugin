---
type: tool
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: [browser-automation, e2e-testing, mcp]
aliases: ["Puppeteer MCP", "Puppeteer Model Context Protocol"]
relates_to:
  - target: "[[Ralph Loop]]"
    type: used_by
  - target: "[[浏览器自动化验证]]"
    type: enables
  - target: "[[MCP]]"
    type: implements
supersedes: null
---

# Puppeteer MCP

## 概述
Puppeteer MCP 是基于 [[MCP|Model Context Protocol]] 的浏览器自动化工具集成，提供页面导航、截图、表单填充、点击交互和 DOM 验证等能力，在 [[Ralph Loop]] 系统中用于前端 User Story 的 E2E 验证。

## 关键内容

1. **核心能力**：通过 MCP 协议暴露 Puppeteer 浏览器自动化操作，包括 `puppeteer_navigate`（页面导航）、`puppeteer_screenshot`（截图捕获）、`puppeteer_fill`（表单填充）、`puppeteer_click`（元素点击）等工具函数。

2. **在 [[Ralph Loop]] 中的角色**：[[Ralph Loop]] 的核心约束要求所有前端变更必须通过[[浏览器自动化验证]]，而非主观判断"应该能用"。Agent 在实现前端 Story 后必须：先截图记录 before 状态 → 执行交互操作 → 截图记录 after 状态 → 验证 URL 跳转、DOM 元素存在、文本内容正确。

3. **验证流程**：
   ```
   puppeteer_navigate(url="http://localhost:[PORT]/[path]")
   puppeteer_screenshot(name="before")
   puppeteer_fill(selector="[selector]", value="[value]")
   puppeteer_click(selector="[submit-btn]")
   puppeteer_screenshot(name="after")
   // 验证：URL 跳转 ✓、DOM 元素存在 ✓、文本内容 ✓
   ```

4. **与 API 验证的区别**：API Story 使用 `curl` 命令行验证，前端 Story 必须使用 Puppeteer MCP。两者验证通过后才能更新 prd.json 中对应 Story 的 `passes: true` 状态。

5. **MCP 协议集成**：作为 [[MCP Prompts|MCP Server]] 运行，通过 stdio 或 Streamable HTTP 与 [[Claude Code]] 等 Agent 通信，遵循 MCP 的工具注册、参数验证和结果返回规范。

## 来源
- [[raw/articles/ai-tools/ralph-loop/CLAUDE.md]] — Ralph Coding Agent 提示词模板中的 Puppeteer MCP 验证流程
- [[raw/articles/ai-tools/ralph-loop/testing-patterns.md]] — Testing Patterns 文档（Puppeteer MCP 在 CLAUDE.md 中的声明方式、验证流程示例）

## 相关
- [[Ralph Loop]] — used_by（核心 E2E 验证工具）
- [[浏览器自动化验证]] — enables（提供底层自动化能力）
- [[MCP]] — implements（基于 MCP 协议的工具集成）
- [[Claude Code]] — uses（通过 MCP 协议调用的工具）
- [[E2E 验证模式]] — part_of（作为模式一的底层工具实现）
