---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [skills, agent-tools, claude-code, automation, AI工程]
aliases: ["Claude Code 技能系统", "Claude Skills", "Agent Skills"]
relates_to: []
supersedes: null
---

# Claude Code Skills

## 概述
[[Claude Code]][[Skills|技能]]是一种强大的扩展机制，允许开发者通过简单的Markdown文件和相关脚本、资源来扩展[[Claude Code]]的功能。[[Agent Skills|技能系统]]提供了灵活、易创建且易于分发的自动化功能。

## 关键内容

1. **[[Skills|技能]]的定义与结构**：
   - [[Skills|技能]]不仅仅是Markdown文件，而是包含脚本、资产、数据等的完整文件夹
   - [[Claude_Code|Claude]]可以发现、探索和操作这些文件
   - 拥有多种[[Configuration|配置]]选项，包括动态钩子注册

2. **[[Skills|技能]]的主要类型**：
   - **库与API参考**：解释如何正确使用库、CLI或SDK
   - **产品验证**：描述如何测试或验证代码是否正常工作
   - **数据获取与分析**：连接到数据和监控堆栈
   - **业务流程与团队自动化**：将重复性工作流自动化为单个命令
   - **代码脚手架与模板**：为特定函数生成框架样板
   - **代码质量与审查**：在组织内强制执行代码质量并帮助审查代码
   - **CI/CD与部署**：帮助获取、推送和部署代码
   - **运行手册**：处理症状分析并生成结构化报告
   - **基础设施操作**：执行例行维护和操作程序

3. **制作[[Skills|技能]]的最佳实践**：
   - **构建常见陷阱部分**：最高信号的内容是[[Gotchas]]部分
   - **使用文件系统和渐进式披露**：[[Skills|技能]]是文件夹而非仅Markdown文件
   - **避免过度引导[[Claude_Code|Claude]]**：给[[Claude_Code|Claude]]信息但给予适应情况的灵活性
   - **考虑[[Settings|设置]]过程**：一些[[Skills|技能]]可能需要用户上下文
   - **描述字段面向模型**：描述应该说明何时触发此[[Skills|技能]]
   - **内存与数据存储**：[[Skills|技能]]可以在内部存储形式的数据作为内存
   - **存储脚本与生成代码**：给[[Claude_Code|Claude]]提供脚本使其能够组合功能

## 来源
- [[Lessons from Building Claude Code_ How We Use Skills]] — 完整的文章内容
- [[Thariq (@trq212)]] — 作者

## 相关
- [[Agent-Native-Architecture]] — relates_to
- [[Context-Engineering]] — relates_to
- [[Action-Parity]] — relates_to
- [[Context-Parity]] — relates_to