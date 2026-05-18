---
type: concept
title: "事件驱动 Agent 架构"
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, Agent, 架构, 设计模式, LLM, 事件驱动, Agent系统]
aliases:
  - Event-driven Agent
  - Agent事件模型
  - subscribe-emit Agent
relates_to:
  - target: "[[Pi-Agent]]"
    type: implemented_by
    confidence: 0.95
  - target: "[[Agent循环]]"
    type: related_to
    confidence: 0.9
  - target: "[[Agent Harness模式]]"
    type: related_to
    confidence: 0.8
supersedes: null
---

# 事件驱动 Agent 架构

## 概述

事件驱动 [[Agent 架构与设计原则|Agent 架构]]是指：Agent 循环内所有状态变化都通过**事件发射（emit）**通知订阅者，而不依赖返回值。同一 Agent 核心可同时驱动终端 UI、Web UI、IM 机器人等完全不同的上层界面。

## 关键内容

### 核心设计决策

**所有状态变化 → 事件，而非返回值。**

```typescript
session.subscribe((event) => {
  switch (event.type) {
    // LLM 响应阶段
    case 'message_start':   /* 开始生成 */ break;
    case 'text_delta':      /* 流式文本 */ break;
    case 'thinking_delta':  /* 思维链内容 */ break;

    // 工具调用阶段
    case 'tool_call_start': /* 工具名+ID */ break;
    case 'tool_call_delta': /* 参数流（实时显示文件路径等） */ break;
    case 'tool_call_end':   /* 参数确定 */ break;
    case 'tool_result':     /* 执行完成（LLM通道 + UI通道） */ break;
    case 'tool_update':     /* onUpdate 推送的流式进度 */ break;

    // 生命周期
    case 'message_end':     /* 本轮生成完成 */ break;
    case 'session_end':     /* Agent 循环结束 */ break;
    case 'error':           /* 错误 */ break;
  }
});
```

### 双通道设计：LLM 通道 vs UI 通道

`tool_result` 事件包含两个字段：

| 字段 | 消费者 | 内容 |
|------|--------|------|
| `output` | LLM | 影响后续推理的文本（计入 token 上下文） |
| `details` | UI | 结构化数据（exitCode、截图等），不占 LLM token |

这一分离保持了 LLM 上下文精简，同时允许 UI 展示丰富的结构化信息。

### 多 UI 驱动能力

```
AgentSession（pi-agent-core）
    │
    ├── pi-tui（终端 UI）   ← 事件 → 差分渲染终端输出
    ├── pi-web-ui（Web UI） ← 事件 → 更新 React 组件
    ├── OpenClaw（IM 平台） ← 事件 → 发送 Telegram/Discord 消息
    └── 测试框架            ← 事件 → 断言验证、录制回放
```

同一套 Agent 核心代码零修改即可接入所有上层 UI。

### 为何不用 async generator？

| | 事件（subscribe/emit） | Async Generator |
|--|----------------------|----------------|
| 消费者数量 | **多订阅者**（TUI + 日志 + 测试同时接收） | 单消费者 |
| 耦合度 | 发布者不感知消费者 | 生产者-消费者紧耦合 |
| 扩展性 | 增加 UI 只需注册新监听器 | 需重构消费逻辑 |

## 会话持久化

事件流状态可序列化到磁盘，在新进程中完整恢复：

```typescript
const snapshot = session.serialize();
// 下次启动时
const restored = restoreAgentSession(snapshot, { model, tools });
await restored.prompt('继续之前未完成的重构工作');
```

## 代表实现

[[Pi-Agent]] 的 `pi-agent-core` 包是此模式的参考实现，[[OpenClaw]] 是其多渠道 IM 接入的应用案例。

## 来源

- [[raw/articles/ai-tools/pi-agent/03-pi-agent-core.md]]

## 相关

- [[Agent循环]] — 事件是 Agent 循环各阶段状态变化的通知机制
- [[Pi-Agent]] — 代表性实现
- [[OpenClaw]] — 事件模型驱动多 IM 渠道的应用案例
- [[Agent Harness模式]] — 更宏观的 Agent 工程架构模式
