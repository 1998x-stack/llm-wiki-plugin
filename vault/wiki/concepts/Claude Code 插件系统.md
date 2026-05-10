---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["AI工程"]
aliases: ["Claude Code Plugins", "插件系统", "一体化扩展包"]
relates_to:
  - target: "[[斜杠命令（Slash Commands）]]"
    type: extends
    confidence: 0.9
  - target: "[[Subagents-in-Claude-Code]]"
    type: extends
    confidence: 0.85
  - target: "[[MCP协议层]]"
    type: extends
    confidence: 0.8
  - target: "[[Claude-Code-Hook-System]]"
    type: extends
    confidence: 0.8
  - target: "[[TAOR 循环]]"
    type: implements
    confidence: 0.9
  - target: "[[nO 主循环]]"
    type: implements
    confidence: 0.9
  - target: "[[h2A 实时转向队列]]"
    type: implements
    confidence: 0.85
supersedes: null
---

# Claude Code 插件系统

## 概述
插件是 [[Claude Code]] 最高级别的扩展方式，将 slash commands、subagents、MCP servers 和 hooks 打包成可安装的一体化方案，通过一条命令即可安装，代表完整的工作流解决方案。

## 关键内容

1. **插件架构**：一个插件通常打包以下能力——slash commands、subagents、MCP servers、hooks、configuration。好处是一次安装即可使用完整工作流，团队共享更容易，[[Configuration|配置]]统一，便于版本控制和分发。

2. **插件类型**：
   - **官方**：全局范围，所有用户可用，[[Anthropic]] 维护（如 PR 审查、安全指导）
   - **社区**：公开范围，社区维护（如 [[DevOps]]、数据科学）
   - **组织**：内部范围，团队成员可用，公司维护
   - **个人**：个人范围，单个用户可用，开发者自定义工作流

3. **插件定义**：使用 `.claude-plugin/plugin.json` 清单文件定义，包含名称、描述、版本、依赖和包含的功能列表。

4. **与 [[Agent Skills|Skills]] 的区别**：[[Agent Skills|Skills]] 是单一能力包（一个 [[Agent Skills|SKILL.md]] + 可选脚本），插件是多个功能的组合体（commands + agents + MCP + hooks）。插件是 [[Agent Skills|Skills]] 的上层抽象。

## 来源
- [[07-plugins/README.md]] — Claude HowTo 插件指南

## 相关
- [[斜杠命令（Slash Commands）]] — extends
- [[Subagents-in-Claude-Code]] — extends
- [[MCP协议层]] — extends
- [[Claude-Code-Hook-System]] — extends
