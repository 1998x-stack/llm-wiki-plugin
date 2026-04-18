---
type: concept
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 2
tags: [技术, AI, 方法论, AI工程]
aliases: ["Long-running Agent Harness", "长时自主Agent", "多上下文窗口工作流", "初始化Agent"]
relates_to:
  - target: "[[Agent Harness模式]]"
    type: part_of
    confidence: 0.92
  - target: "[[上下文焦虑]]"
    type: related_to
    confidence: 0.9
  - target: "[[结构化笔记法]]"
    type: uses
    confidence: 0.88
  - target: "[[生成器-评估器架构]]"
    type: related_to
    confidence: 0.82
supersedes: null
---

# 长时任务 Agent 设计

## 概述

针对跨多个[[上下文窗口]]的长时自主任务（数小时至数日）的 [[Agent Harness模式|Agent Harness]] 设计模式：**[[Initializer Agent|初始化 Agent]]**（建立环境和功能列表）+ **编码 Agent**（增量推进并留清晰交接产物）两阶段架构，解决 Agent 过早宣告完成、中途失去方向等失败模式。

## 关键内容

### 核心问题：无记忆的交接

长时任务必须在多个 [[上下文窗口|Context Window]] 中进行，每个新会话从零记忆开始——类似"每班交接时上一班的记忆全部清空的工程师团队"。单纯依赖压缩（[[上下文压缩|Compaction]]）不足以解决此问题：Agent 仍会尝试一次性完成全部工作（"一枪打"），或误判任务已完成。

### 两阶段解决方案

**第一阶段：[[Initializer Agent|初始化 Agent]]**

首次会话使用专门提示，负责搭建环境：
1. 创建 `init.sh` 脚本（启动开发服务器）
2. 创建 `claude-progress.txt`（会话间状态传递文件）
3. 基于用户提示生成**完整功能需求列表**（JSON 格式，每条功能含步骤和 `passes: false` 状态）
4. 初始 git commit，展示已添加的文件

功能列表示例（200+ 条，全部初始标记为 failing）：
```json
{
  "category": "functional",
  "description": "New chat button creates a fresh conversation",
  "steps": ["Navigate to main interface", "Click 'New Chat' button", ...],
  "passes": false
}
```

**第二阶段：编码 Agent（每次会话）**

每次会话的标准化启动序列：
1. `pwd` 确认工作目录
2. 读取 git 日志和进度文件了解最近工作
3. 读取功能列表，选择下一个高优先级未完成功能
4. 运行 `init.sh`，启动开发服务器
5. 执行基础端到端测试确认应用未被破坏
6. **仅处理一个功能**（增量进度的核心）
7. 用浏览器自动化工具（Puppeteer MCP）端到端验证功能
8. 更新 `passes` 字段（仅改此字段，禁止删除/编辑测试条目）
9. git commit + 更新进度日志

### 四大失败模式及解决

| 失败模式 | 初始化 Agent 应对 | 编码 Agent 应对 |
|---------|-----------------|----------------|
| 过早宣告项目完成 | 创建功能列表（所有条目初始为 failing） | 每次读取功能列表，选择单一功能 |
| 留下有 Bug 的环境 | 创建初始 git 仓库和进度文件 | 读取进度文件和 git 日志；运行基础测试；结束时写 commit + 更新进度 |
| 过早标记功能完成 | 创建功能列表 | 仔细自我验证，通过测试后才标记 passing |
| 浪费时间弄清如何运行应用 | 编写 `init.sh` | 首先读取 `init.sh` |

### 关键实现细节

**为什么用 JSON 而非 Markdown**：实验发现模型更不容易擅自修改或覆盖 JSON 文件，而对 Markdown 文件有更强的"重写"冲动。

**"不可接受移除测试"**：需强措辞："移除或编辑测试是不可接受的行为，这会导致缺失或有 Bug 的功能。"

**浏览器自动化测试的必要性**：代码层面测试（单元测试、curl）常常无法发现端到端 Bug；必须像真实用户一样通过浏览器测试，才能发现功能是否真正工作。

**视觉局限**：Claude 的视觉和浏览器自动化工具有限制——无法通过 Puppeteer 看到原生浏览器 alert 弹窗，依赖这些弹窗的功能往往更有 Bug。

### 与多 Agent 架构的关系

两阶段设计是 [[Anthropic]] 早期长时 Harness 的探索。后续研究（见[[生成器-评估器架构]]）在此基础上增加了 Evaluator 层，发展为三 Agent（Planner + [[生成器|Generator]] + Evaluator）系统。当模型能力提升后（Opus 4.6），Sprint 分解结构可被移除，但初始化/状态传递的核心思想依然有效。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/Effective harnesses for long-running agents.md]]
- [[raw/articles/ai-engineering/anthropic-engineering/Harness design for long-running application development.md]]

## 相关

- [[Agent Harness模式]] — part_of（两阶段 Harness 是长时任务场景的具体实现）
- [[上下文焦虑]] — related_to（上下文焦虑是驱动此设计的失败模式之一）
- [[结构化笔记法]] — uses（进度文件是结构化笔记法的具体应用）
- [[生成器-评估器架构]] — related_to（三 Agent 系统是此方案的进一步演化）
- [[Sprint合约制]] — related_to（Sprint 前合约谈判是此架构的一个增强机制）
