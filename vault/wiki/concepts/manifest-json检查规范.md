---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [示例管理, manifest, UrhoX, 项目配置, 文件复制, 游戏开发]
aliases: [manifest检查, 示例复制规范, 配置文件完整性]
relates_to: [UrhoX引擎, 游戏脚手架模式]
supersedes: null
---

# manifest-json检查规范

## 概述
[[UrhoX引擎|UrhoX]] 中复制示例目录前必须检查 `manifest.json` 文件，确保完整复制所有必需的[[Configuration|配置]]和资源文件。

## 关键内容
1. **检查流程**：复制示例目录前先检查是否存在 `manifest.json`。如果存在，按其 `includes` 字段复制所有匹配文件；如果 `copyAll: true`，复制整个目录（包括非 .lua 文件）；如果不存在，先用 `ls -la` 检查目录结构。
2. **重要文件类型**：`.fsm`（有限状态机）、`.blendspace`（混合空间）、`.json`（[[Configuration|配置]]文件）等非代码文件同样重要，遗漏会导致示例无法正常运行。
3. **适用场景**：此规范适用于所有示例目录的复制操作，确保示例的完整性和可运行性。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，示例复制规则

## 相关
- [[UrhoX引擎]] — relates_to（宿主引擎）
- [[游戏脚手架模式]] — relates_to（同为项目起手的规范）
