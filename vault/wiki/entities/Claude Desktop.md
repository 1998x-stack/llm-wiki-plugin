---
type: project
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [Anthropic, 桌面应用, MCP, AI工程]
aliases: ["Claude Desktop", "Claude 桌面"]
relates_to:
  - "[[MCP]] — uses"
  - "[[Desktop Extensions]] — part_of"
  - "[[Anthropic]] — part_of"
  - "[[扩展市场]] — relates_to"
supersedes: null
---

# Claude Desktop

## 概述
[[Claude_Code|Claude]] Desktop 是 [[Anthropic]] 推出的桌面端 AI 应用，支持通过 MCP 协议集成外部工具，并通过 [[Desktop Extensions]] 实现一键安装扩展。

## 关键内容

1. **核心定位**：作为 [[Anthropic]] 的桌面端产品，[[Claude_Code|Claude]] Desktop 是用户与 [[Claude_Code|Claude]] AI 交互的主要入口之一，支持通过 [[MCP]] 协议连接各种外部[[服务]]和数据源。

2. **[[Desktop Extensions]] 支持**：引入了一键安装 [[MCP 服务器]]的功能，将原本需要手动[[Configuration|配置]]的技术操作简化为点击安装。用户可在[[扩展市场]]中浏览、安装扩展，安装时查看[[Permissions|权限]]请求并[[Configuration|配置]]必要凭证（如 API 密钥）。

3. **[[安全沙箱]]**：每个扩展在独立进程中运行，[[Permissions|权限]]声明清晰可见，敏感[[Configuration|配置]]存储在系统密钥链中，确保安全性不牺牲可用性。

4. **[[Configuration|配置]]管理**：传统方式需要手动编辑 `config.json` 文件[[Configuration|配置]] [[MCP 服务器]]，[[Desktop Extensions]] 将此过程完全自动化，依赖管理、[[Configuration|配置]]管理全部对用户透明。

5. **生态意义**：通过降低工具集成门槛，[[Claude_Code|Claude]] Desktop 从技术用户扩展到普通用户，为 MCP 生态系统的繁荣奠定基础。

## 来源
- [[21_desktop_extensions.md]] — Anthropic Engineering Blog 原文

## 相关
- [[MCP]] — uses
- [[Desktop Extensions]] — has_feature
- [[Anthropic]] — developed_by
- [[扩展市场]] — integrates_with
