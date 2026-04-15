---
type: concept
title: Claude Code Hook System
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: '2026-04-15'
source_count: 1
tags:
- AI
- 工具，方法论
aliases:
- Claude Code Hooks
- Hook Lifecycle
- Claude Plugin Hooks
relates_to:
- target: '[[Claude-Mem]]'
  type: uses
  confidence: 1.0
- target: '[[Claude-Code]]'
  type: part_of
  confidence: 0.95
supersedes: null
---

# Claude Code Hook System

## 概述
Claude Code Hook System 是 Claude Code 编程助手提供的一种扩展机制，允许开发者通过编写脚本拦截和响应 AI 会话的生命周期事件。该系统包含一组预定义的钩子（Hooks），覆盖从会话初始化、用户输入、工具调用到会话结束的全过程。通过这一系统，第三方插件（如 [[Claude-Mem]]）能够实现深度集成，捕获原始交互数据、修改上下文或执行后台任务，从而扩展 Claude Code 的原生能力。

## 关键内容
### 钩子生命周期
Claude Code 的钩子系统定义了五个关键阶段的触发点，每个阶段对应特定的 JS/TS 脚本：
1. **Context Hook (`context-hook`)**：在会话启动时触发。用于读取外部数据（如历史记忆）并注入到初始上下文中，为 AI 提供前置知识。
2. **New Hook (`new-hook`)**：当用户发起新的对话或提示词时触发。负责创建会话记录、保存用户意图（经脱敏处理后）。
3. **Save Hook (`save-hook`)**：在每次工具调用（Tool Call）完成后触发。这是最频繁的钩子，用于捕获工具名称、输入参数及响应结果，是构建行为记忆的关键入口。
4. **Summary Hook (`summary-hook`)**：在用户停止问答或会话告一段落时触发。用于分析转录日志（transcript.jsonl），生成高层级的会话摘要（如完成的任务、学到的经验）。
5. **Cleanup Hook (`cleanup-hook`)**：在会话彻底结束时触发。负责更新会话状态（如标记为 completed），执行资源清理，但不删除历史数据以保留记忆。

### 通信模式：即发即忘（Fire-and-Forget）
由于 Hook 脚本运行在主进程中且受严格的超时限制（默认 120 秒），复杂的处理逻辑（如 AI 压缩）不能同步执行。因此，高效的 Hook 实现通常采用异步通信模式：
- **非阻塞调用**：Hook 脚本通过 HTTP POST 请求将数据发送给后台 Worker 服务。
- **快速返回**：发出请求后立即返回控制权给主进程，不等待处理结果。
- **后台处理**：Worker 服务接收请求后，在独立进程中完成耗时的 AI 推理和数据库写入操作。

### 应用场景
除了记忆系统外，Hook 系统还可用于：
- **合规性检查**：在代码写入前自动扫描敏感信息或违规模式。
- **自定义工作流**：根据特定工具调用触发外部 CI/CD 流水线。
- **遥测与分析**：收集匿名化的使用数据以优化模型表现。

该系统的灵活性使得 Claude Code 不仅仅是一个聊天机器人，而是一个可编程的、具备扩展性的开发平台。

## 来源
- [[raw/articles/claude-mem/blog_01_overview.md]]

## 相关
- [[Claude-Mem]]
- [[Claude-Code]]