---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [AI工具, 无障碍, Claude插件, WCAG]
aliases: ["accesslint/claude-marketplace", "AccessLint插件"]
relates_to:
  - target: "[[bencium UX Designer]]"
    type: relates_to
    confidence: 0.8
  - target: "[[WCAG]]"
    type: implements
    confidence: 0.9
  - target: "[[无障碍设计]]"
    type: implements
    confidence: 0.9
supersedes: null
---

# AccessLint

## 概述
AccessLint是一个专注于无障碍合规的[[Claude_Code|Claude]] Marketplace插件，提供自动化[[WCAG|WCAG 2.1]] AA标准检查和[[代码重构]]功能。

## 关键内容

1. **功能组件**：
   - `contrast-checker`：颜色对比度检查，自动检测CSS/[[Tailwind CSS v4|Tailwind]]中的颜色对比度问题
   - `link-purpose`：链接文字可理解性检查，修复"点击这里"等无障碍不友好的链接文字
   - `refactor`：系统性[[重构]]代码以提升无障碍性，包括语义HTML、ARIA角色、键盘事件处理等
   - `use-of-color`：颜色使用规范审查

2. **技术架构**：捆绑专门的[[MCP Prompts|MCP Server]]进行精确的颜色对比度[[计算]]，提供calculate_contrast_ratio、find_accessible_alternative等功能

3. **专用Agent**：`accesslint:reviewer`执行完整的[[WCAG|WCAG 2.1]] Level A和AA一致性审查

4. **工作流程**：从开发时的ACCESSIBILITY.md规范，到实现后的即时检查，再到发布前的全面审查

## 来源
- [[06_bencium_ux_designer_and_accesslint.md]] — AccessLint部分

## 相关
- [[bencium UX Designer]] — relates_to
- [[WCAG]] — relates_to
- [[无障碍设计]] — relates_to
- [[Claude Code]] — relates_to