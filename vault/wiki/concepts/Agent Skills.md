---
type: concept
status: active
confidence: 0.92
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [技术, AI, 方法论]
aliases: ["Agent Skills", "SKILL.md", "技能系统", "Agent技能", "Skills"]
relates_to:
  - target: "[[渐进式披露-Progressive-Disclosure]]"
    type: implements
    confidence: 0.95
  - target: "[[即时上下文检索]]"
    type: implements
    confidence: 0.88
  - target: "[[Context-Engineering]]"
    type: part_of
    confidence: 0.85
  - target: "[[Claude-Code]]"
    type: implemented_by
    confidence: 0.9
supersedes: null
---

# Agent Skills

## 概述

Agent Skills（代理技能）是 Anthropic 提出的开放标准：**一个含 SKILL.md 文件的目录**，通过渐进式披露机制为 Agent 提供可组合、可共享的领域专业知识。本质是把"给新员工的入职指南"包装成 Agent 可动态加载的模块化资源。

## 关键内容

### 核心结构

一个 Skill 就是一个目录，核心是 `SKILL.md` 文件：

```
skill-name/
├── SKILL.md          ← 必须，含 YAML 前置元数据和技能内容
├── reference.md      ← 可选，更多细节文件（按需加载）
├── forms.md          ← 可选，特定场景细节（按需加载）
└── scripts/          ← 可选，可执行代码（工具脚本）
```

`SKILL.md` 必须以 YAML 前置元数据开头，含 `name` 和 `description`：

```yaml
---
name: PDF Skill
description: 操作和处理 PDF 文件，包括读取、填写表单、提取内容
---
# 详细操作说明...
```

### 三层渐进式披露

Agent Skills 的设计核心是[[渐进式披露-Progressive-Disclosure]]原则，分三层加载：

| 层次 | 内容 | 何时加载 |
|------|------|---------|
| **第一层** | 所有 Skill 的 `name` 和 `description` | 启动时自动注入系统提示 |
| **第二层** | 某 Skill 的完整 `SKILL.md` | Claude 判断该 Skill 与当前任务相关时 |
| **第三层（及以上）** | 额外引用文件（如 forms.md、reference.md） | Claude 根据具体子任务按需读取 |

**关键洞见**：Skills 可捆绑的上下文量实际上**无上限**——Agent 有文件系统和代码执行工具，无需一次性将整个 Skill 加载入上下文。

### 技能包含代码

Skills 可包含预写的 Python/Bash 脚本供 Claude 运行，而无需将脚本内容和数据对象加载入上下文：
- 代码执行是确定性的，结果一致可重复
- 大型 PDF、数据文件等可被脚本处理，不直接进入 LLM 上下文
- 代码可作为文档（引用阅读）或工具（执行使用）

### 上下文窗口动态

触发 Skill 时的上下文变化序列：
1. 初始上下文 = 核心系统提示 + 所有 Skill 的 name/description + 用户消息
2. Claude 判断 PDF Skill 相关 → bash 读取 `pdf/SKILL.md` → 加载到上下文
3. 用户要填表单 → Claude 读取 `forms.md` → 加载到上下文
4. Claude 执行任务（可运行 Skill 中的 Python 脚本）

### 最佳开发实践

**从评估出发**：先识别 Agent 能力差距，再构建针对性 Skill；而非先构建再寻找用途。

**结构化扩展**：当 `SKILL.md` 变得庞杂时，将互斥或低频内容拆分到独立文件并引用。

**从 Claude 视角思考**：监控 Claude 实际使用 Skill 的轨迹；若偏离预期，要求 Claude 自我反思；特别关注 `name` 和 `description` 的措辞——这决定触发时机。

**与 Claude 迭代**：在完成任务过程中，要求 Claude 将成功方法和常见错误编码到 Skill 中。

### 安全考虑

Skills 为 Claude 提供了新能力，恶意 Skill 可能引入漏洞或指导 Claude 外泄数据：
- 只安装来自可信来源的 Skills
- 对不受信来源的 Skill，彻底审计其文件内容和代码依赖
- 注意 Skill 中引导 Claude 连接外部不受信网络的指令

### 在 Anthropic 生态中的位置

Agent Skills 是开放标准，支持：Claude.ai、Claude Code、Claude Agent SDK、Claude Developer Platform。

与 [[MCP协议层]] 的互补关系：MCP 连接工具和服务，Skills 教导 Agent 如何使用这些工具和服务的复杂工作流。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/Equipping agents for the real world with Agent Skills.md]]

## 相关

- [[渐进式披露-Progressive-Disclosure]] — implements（Skills 是渐进式披露在 Agent 知识管理中的具体实现）
- [[即时上下文检索]] — implements（Skills 的按需加载机制是 JIT 检索的应用）
- [[Context-Engineering]] — part_of（Skills 是上下文工程中知识注入的模块化手段）
- [[Claude-Code]] — implemented_by（Claude Code 是 Skills 的主要运行环境）
- [[MCP协议层]] — related_to（Skills 和 MCP 是互补的能力扩展机制）
