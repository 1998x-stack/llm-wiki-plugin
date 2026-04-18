---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["claude-code", "protocol", "tool-system", "integration", "工具与框架"]
aliases: ["MCP", "Model Context Protocol", "MCP Servers"]
relates_to:
  - target: "[[Claude Code]]"
    type: uses
  - target: "[[Agent Skills]]"
    type: compares_to
  - target: "[[Codex CLI]]"
    type: uses
  - target: "[[Agent可组合性]]"
    type: enables
  - target: "[[Context7]]"
    type: implements
  - target: "[[MCP Inspector]]"
    type: used_by
---

# MCP

## 概述
Model Context Protocol，进程级工具服务协议，AI 编码工具通过 MCP 连接独立进程暴露的工具和数据，与 [[Agent Skills]] 形成互补的扩展机制。

## 关键内容

1. **本质**：
   - 独立进程运行的服务
   - 通过 Model Context Protocol 暴露工具和数据
   - AI 客户端通过 stdio 或 SSE 与 MCP Server 通信

2. **与 [[Agent Skills]] 的区别**：
   | 维度 | [[Agent Skills]] | MCP Servers |
   |------|-------------|-------------|
   | 本质 | 目录级 Prompt 包 | 进程级工具服务 |
   | 内容 | [[SKILL.md 格式规范|SKILL.md]] + 脚本 | 独立可执行程序 |
   | 加载 | [[渐进式加载]]到上下文 | 按需调用外部进程 |
   | 适用 | 编码指导、工作流 | 工具集成、数据访问 |

3. **[[Claude Code]] 中的 MCP 类型**：
   - **本地 MCP Servers**：本地运行的工具服务
   - **Claude Connectors**：远程 MCP 服务（Slack、Figma、Asana 等 SaaS）

4. **典型用例**：
   - 数据库查询工具
   - 文件系统操作
   - API 客户端
   - 版本控制集成

## 来源
- [[01_claude_code_skill_system_overview]] — 系统架构全景
- [[raw/articles/ai-tools/codex/06_codex_mcp_layer.md]] — Codex MCP Layer 深度解析

## 相关
- [[Claude Code]] — uses
- [[Agent Skills]] — compares_to
- [[Claude Connectors]] — extends
- [[Codex CLI]] — uses
- [[Agent可组合性]] — enables
- [[Context7]] — implements
- [[MCP Inspector]] — used_by
