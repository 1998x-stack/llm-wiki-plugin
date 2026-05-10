---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: ["claude-code", "protocol", "tool-system", "integration", "工具与框架"]
aliases: ["MCP", "Model Context Protocol", "MCP Servers", "Model Context Protocol"]
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
  - target: "[[HTTP 传输协议]]"
    type: uses
    confidence: 0.8
  - target: "[[Stdio 传输协议]]"
    type: uses
    confidence: 0.8
  - target: "[[SSE 传输协议]]"
    type: uses
    confidence: 0.8
  - target: "[[WebSocket 传输协议]]"
    type: uses
    confidence: 0.7
  - target: "[[OAuth 2.0 认证]]"
    type: supports
    confidence: 0.75
  - target: "[[MCPorter]]"
    type: extends
    confidence: 0.6
---

# MCP

## 概述
[[Model Context Protocol]]，进程级工具[[服务]]协议，AI 编码工具通过 MCP 连接独立进程暴露的工具和数据，与 [[Agent Skills]] 形成互补的扩展机制。支持多种传输协议如 [[HTTP 传输协议]]、[[Stdio 传输协议]]、[[SSE 传输协议]] 等，可通过 [[OAuth 2.0 认证]] 进行安全认证，并利用 [[MCPorter]] 实现工具组合编排。

## 关键内容

1. **本质**：
   - 独立进程运行的[[服务]]
   - 通过 [[Model Context Protocol]] 暴露工具和数据
   - AI 客户端通过 stdio 或 SSE 与 [[MCP Prompts|MCP Server]] 通信

2. **三种传输模式**：
   - `stdio`：本地进程，原生隔离，不经过网络
   - `SSE`：远程 HTTP 流式，实时推送
   - `HTTP`：远程 HTTP 非流式，简单请求-响应

3. **[[Configuration|配置]]结构**：
   - 用户级 MCP：`~/.claude.json`（不在 ~/.claude/ 目录内）
   - 项目级 MCP：`./.mcp.json`（提交到 Git，团队共享）
   - 规则：项目级 MCP 补充（不覆盖）用户级 MCP

4. **Tool Search 机制**：
   - 会话启动时仅加载工具名称（极低 Token 消耗）
   - [[Claude_Code|Claude]] 遇到需要外部工具的任务时搜索匹配的 MCP 工具名
   - [[渐进式披露（Progressive Disclosure）|按需加载]]完整工具 Schema（进入上下文）
   - 效果：即使[[Configuration|配置]]了大量 [[MCP 服务器]]，上下文开销仍然最小

5. **输出 Token 保护**：
   - 警告阈值：10,000 tokens（显示警告）
   - 默认上限：25,000 tokens（截断）
   - 调整：export MAX_MCP_OUTPUT_TOKENS=50000
   - 最佳实践：让 [[MCP 服务器]]分页/过滤响应，而非增加上限

6. **社区生态（2026 年 3 月）**：
   - server-github：Issues、PR、[[仓库]]搜索（15 个工具）
   - mcp-server-brave-search：网页搜索（400ms 均值）
   - @playwright/mcp：浏览器自动化（150MB/实例）
   - 数据库系列：SQL 查询、Schema 探索
   - server-slack：消息、频道、搜索
   - 生态规模：200+ 社区[[服务]]器；[[GitHub]] [[服务]]器被 **92%** 启用 MCP 的用户最先安装

7. **与 [[Agent Skills]] 的区别**：
   | 维度 | [[Agent Skills]] | [[MCP Prompts|MCP Server]]s |
   |------|-------------|-------------|
   | 本质 | 目录级 Prompt 包 | 进程级工具[[服务]] |
   | 内容 | [[SKILL.md 格式规范|SKILL.md]] + 脚本 | 独立可执行程序 |
   | 加载 | [[渐进式加载]]到上下文 | 按需调用外部进程 |
   | 适用 | 编码指导、工作流 | 工具集成、数据访问 |

8. **[[Claude Code]] 中的 MCP 类型**：
   - **[[本地 MCP Servers]]**：本地运行的工具[[服务]]
   - **[[Claude Connectors]]**：远程 MCP [[服务]]（[[Slack]]、Figma、Asana 等 SaaS）

9. **典型用例**：
   - 数据库查询工具
   - 文件系统操作
   - API 客户端
   - 版本控制集成

5. **工具描述质量**：MCP 工具的性能不仅取决于底层实现，更依赖于工具描述的质量。糟糕的工具描述会导致错误的工具选择、参数格式错误、Agent 绕过有用工具。Anthropic 实践表明，经过 AI 辅助优化的工具描述可使后续 Agent 任务完成时间减少 40%。[[工具测试 Agent]] 是专门用于测试和改进 MCP 工具描述的有效方法。

6. **防错设计在 MCP 中的应用**：MCP 工具定义应采用防错设计手段，如使用具体类型而非宽泛字符串、提供枚举值而非自由文本、要求绝对路径而非相对路径，使常见错误在结构上不可能发生。

7. **[[代码执行]] MCP 服务器**：
   - 通过 MCP 提供安全的代码执行能力，使 Agent 从"描述解决方案"跃迁为"直接执行验证"
   - 工具定义示例：`execute_python`，在安全 Python 3.11 环境中执行代码，支持 numpy、pandas、matplotlib 等预安装库
   - 安全架构：在隔离容器（Docker/gVisor）中执行，文件系统访问受限，网络访问可控，执行超时（30 秒），内存限制
   - 效率提升：将问题解决往返次数从 3-5 轮减少到 1-2 轮，将"语言准确性"转化为"逻辑准确性"
   - 最佳实践：始终在[[安全沙箱]]中执行，合理设置超时和内存限制，审查涉及外部系统的代码

## 来源
- [[05_to_08_combined]] — 07 · MCP（Model Context Protocol）
- [[01_claude_code_skill_system_overview]] — 系统架构全景
- [[raw/articles/ai-tools/codex/06_codex_mcp_layer.md]] — Codex MCP Layer 深度解析
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/00_INDEX.md]] — Desktop Extensions、代码执行 MCP、高级工具使用
- [[10_writing_tools_for_agents]] — MCP 工具描述质量优化及测试 Agent 实践
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/20_code_execution_mcp]] — 通过 MCP 的代码执行：构建更高效的 Agent

## 相关
- [[Claude Code]] — uses
- [[Agent Skills]] — compares_to
- [[Claude Connectors]] — extends
- [[Codex CLI]] — uses
- [[Agent可组合性]] — enables
- [[Context7]] — implements
- [[MCP Inspector]] — used_by
- [[SSE 传输协议]] — uses
- [[Tool Ecosystem]] — relates_to
- [[Model Context Protocol]] — relates_to
