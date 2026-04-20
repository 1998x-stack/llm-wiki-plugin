---
type: concept
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["MCP", "文件格式", "打包"]
aliases: ["DXT", "Desktop Extension 格式", ".dxt"]
relates_to:
  - "[[Desktop Extensions]] — used_by"
  - "[[MCP]] — relates_to"
supersedes: null
---

# DXT 文件格式

## 概述
DXT（Desktop Extension）是 Claude Desktop 扩展的打包文件格式，包含 manifest.json、MCP 服务器代码、资源和文档的标准化结构。

## 关键内容

1. **文件结构**：一个 `.dxt` 文件是压缩包，包含四个核心部分：`manifest.json`（扩展元数据和依赖声明）、`server/`（MCP 服务器代码，如 `index.js`）、`assets/`（图标和截图）、`README.md`（用户文档）。

2. **manifest.json 关键字段**：包含 `name`、`version`、`description` 等基本信息；`server` 对象指定运行类型（如 `node`）和入口文件；`permissions` 数组声明所需权限（如 `internet`、`filesystem:read`）；`configuration` 定义用户需提供的配置项（如 API 密钥），支持 `secret` 类型安全存储。

3. **打包与分发**：开发者使用 `claude-desktop pack` 命令打包，可提交到 Anthropic 审核后发布到扩展市场，也可直接分发 `.dxt` 文件。

4. **与 Chrome Extension 的类比**：DXT 格式对 MCP 生态的影响类似于 Chrome Extension Store 对浏览器扩展生态的影响——标准化打包和一键安装是生态繁荣的关键基础设施。

## 来源
- [[21_desktop_extensions.md]] — Anthropic Engineering Blog 原文

## 相关
- [[Desktop Extensions]] — used_by
- [[MCP]] — relates_to
- [[扩展市场]] — relates_to
