---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["AI工程"]
aliases: ["Memory System", "CLAUDE.md 记忆", "跨会话记忆"]
relates_to:
  - target: "[[斜杠命令（Slash Commands）]]"
    type: uses
    confidence: 0.8
  - target: "[[上下文窗口]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# Claude Code 记忆系统

## 概述
Memory 系统让 [[Claude Code]] 在不同会话之间保留上下文。用户可将团队规范、项目规则、个人偏好和目录级约束写进 `CLAUDE.md`，Claude 在合适场景下自动加载。

## 关键内容

1. **记忆范围分层**：
   - **受管策略记忆**：[[Claude Code]] 内置策略
   - **项目记忆**（`./CLAUDE.md`）：项目级规范
   - **用户记忆**（`~/.claude/CLAUDE.md`）：用户级偏好
   - **本地项目记忆**：目录级约束

2. **记忆命令**：
   - `/init`：初始化项目级 `CLAUDE.md`
   - `/memory`：打开并编辑记忆文件，在不同范围间切换
   - `#` 前缀：快速把规则写入记忆（如 `# 这个项目始终使用 TypeScript 严格模式`）

3. **自动加载机制**：Claude 会根据当前工作目录和任务上下文，自动判断加载哪些记忆文件，避免一次性把所有记忆塞进上下文。

4. **与 [[Agent Skills|Skills]] 的区别**：记忆是静态的规则和偏好，[[Agent Skills|Skills]] 是可复用的能力包（含脚本、模板、参考文件）。记忆告诉 Claude"怎么做"，[[Agent Skills|Skills]] 告诉 Claude"能做什么"。

## 来源
- [[02-memory/README.md]] — Claude HowTo Memory 指南

## 相关
- [[斜杠命令（Slash Commands）]] — uses
- [[上下文窗口]] — relates_to
