---
title: "Claude Code Hook机制"
source: "https://chatgpt.com/c/69e596e6-c62c-8324-8890-f319f3bb4a94"
author:
published:
created: 2026-04-20
description: "ChatGPT conversation with 4 messages"
tags:
  - "clippings"
---
Claude code hook 背后的机制是什么，和watchdog有什么区别？

---

我先查一下 Claude Code hooks 的官方说明，再和 watchdog 的实现思路做一个机制层面的对比。

---

给出表格

---

可以，下面是对比表：

| 维度 | Claude Code Hook | watchdog |
| --- | --- | --- |
| 本质 | Agent 运行时的事件钩子 / 中间件 / 拦截器 | 文件系统事件监听库 |
| 监听对象 | Claude Code 生命周期事件，如 SessionStart、PreToolUse、PostToolUse、FileChanged | 操作系统层文件变化，如 create / modify / delete / move |
| 所在层级 | 应用层 / Agent orchestration 层 | OS / 文件系统 I/O 层 |
| 触发时机 | 会话开始、用户提交 prompt、工具调用前后、停止、目录变化等 | 文件或目录发生变化时 |
| 输入上下文 | 高语义 JSON，上下文里可包含工具名、命令参数、事件类型、会话信息 | 低层事件对象，通常只有路径、事件类型、是否目录等 |
| 是否能拦截行为 | 可以，尤其是 PreToolUse 可用于 allow / deny | 一般不行，主要是监听后再响应 |
| 是否理解“AI 正在做什么” | 能理解，知道当前 agent 正在哪个阶段、调用哪个工具 | 不能，只知道文件变了 |
| 典型用途 | 禁止危险命令、工具审计、自动测试、会话初始化、流程编排 | 热重载、自动构建、目录监控、同步任务 |
| 和文件变化的关系 | 文件变化只是众多 hook 事件之一 | 文件变化是核心功能 |
| 编程模型 | 事件匹配 + 条件过滤 + 执行 shell/HTTP/LLM handler + 返回决策 | 注册 observer / handler，收到文件事件后执行回调 |
| 语义层次 | 高语义、面向 agent 工作流 | 低语义、面向文件系统 |
| 更像什么 | policy engine / runtime middleware | fs watcher |

再给你一个更短的总结表：

| 问题 | Claude Code Hook | watchdog |
| --- | --- | --- |
| 它关心什么？ | Claude 在运行时做了什么 | 文件系统发生了什么 |
| 它能做什么？ | 拦截、审计、编排 | 监听、通知、触发后续脚本 |
| 它的核心优势 | 有上下文、可决策 | 简单、通用、底层稳定 |

一句话版：

| 工具 | 一句话理解 |
| --- | --- |
| Claude Code Hook | “Claude 在某个运行阶段触发了事件，我可以介入并决定后续行为” |
| watchdog | “某个文件变了，我收到通知后执行代码” |

要的话，我也可以继续补一个“适用场景对照表”。