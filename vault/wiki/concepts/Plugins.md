---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, distribution, packaging, AI工程]
aliases: ["Plugin System", "Plugin Ecosystem"]
relates_to:
  - target: "[[Claude Code]]"
    type: extends
  - target: "[[Agent Skills]]"
    type: bundles
  - target: "[[Agents]]"
    type: bundles
  - target: "[[Hooks]]"
    type: bundles
  - target: "[[MCP]]"
    type: bundles
supersedes: null
---

# Plugins

## 概述
[[Claude Code]]中将多个[[Skills]]、[[Agents]]、[[Hooks]]、[[MCP|MCP Servers]]打包分发的容器，是一个发布单元，支持Marketplace一键安装。

## 关键内容

1. **组成结构**：
   ```
   my-plugin/
   ├── .claude-plugin
   │   └── plugin.json          # Plugin 元数据（name, version, description）
   ├── skills/
   │   ├── skill-a/
   │   │   └── SKILL.md
   │   └── skill-b/
   │       └── SKILL.md
   ├── agents/
   │   └── my-agent/
   │       └── AGENT.md
   └── mcp/
       └── my-server/           # 捆绑的 MCP Server
   ```

2. **功能特点**：
   - 捆绑Skills、Agents、Hooks、MCP Server
   - 一条命令安装
   - 支持Plugin Marketplace进行分发
   - 使用命名空间避免冲突

3. **命名冲突规则**：
   - Plugin Skills使用`plugin-name:skill-name`命名空间
   - 永远不与用户[[Skills]]冲突

4. **Marketplace命令**：
   - /plugin marketplace add
   - /plugin install
   - /plugin menu
   - /plugin uninstall
   - /reload-plugins

## 来源
- [[raw/articles/ai-tools/claude-skills/01_claude_code_skill_system_overview.md]] — 全文

## 相关
- [[Claude Code]] — extends
- [[Agent Skills]] — bundles
- [[Agents]] — bundles
- [[Hooks]] — bundles
- [[MCP]] — bundles