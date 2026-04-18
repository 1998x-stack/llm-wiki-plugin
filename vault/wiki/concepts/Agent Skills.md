---
type: concept
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 3
tags: [技术, AI, 方法论, AI工程, claude-code, plugin-system, extensibility]
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
  - target: "[[MCP协议层]]"
    type: related_to
  - target: "[[Custom Slash Commands]]"
    type: supersedes
  - target: "[[Claude Code]]"
    type: part_of
  - target: "[[OpenAI Codex]]"
    type: uses
  - target: "[[Cursor]]"
    type: uses
  - target: "[[Gemini CLI]]"
    type: uses
supersedes: null
---

# Agent Skills

## 概述

Agent Skills（代理技能）是 [[Anthropic]] 提出的开放标准：**一个含 [[SKILL.md 格式规范|SKILL.md]] 文件的目录**，通过渐进式披露机制为 Agent 提供可组合、可共享的领域专业知识。本质是把"给新员工的入职指南"包装成 Agent 可动态加载的模块化资源。

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

`[[SKILL.md 格式规范|SKILL.md]]` 必须以 YAML 前置元数据开头，含 `name` 和 `description`：

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
| **第二层** | 某 Skill 的完整 `[[SKILL.md 格式规范|SKILL.md]]` | Claude 判断该 Skill 与当前任务相关时 |
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
2. Claude 判断 PDF Skill 相关 → bash 读取 `pdf/[[SKILL.md 格式规范|SKILL.md]]` → 加载到上下文
3. 用户要填表单 → Claude 读取 `forms.md` → 加载到上下文
4. Claude 执行任务（可运行 Skill 中的 Python 脚本）

### 最佳开发实践

**从评估出发**：先识别 Agent 能力差距，再构建针对性 Skill；而非先构建再寻找用途。

**结构化扩展**：当 `[[SKILL.md 格式规范|SKILL.md]]` 变得庞杂时，将互斥或低频内容拆分到独立文件并引用。

**从 Claude 视角思考**：监控 Claude 实际使用 Skill 的轨迹；若偏离预期，要求 Claude 自我反思；特别关注 `name` 和 `description` 的措辞——这决定触发时机。

**与 Claude 迭代**：在完成任务过程中，要求 Claude 将成功方法和常见错误编码到 Skill 中。

### 安全考虑

Skills 为 Claude 提供了新能力，恶意 Skill 可能引入漏洞或指导 Claude 外泄数据：
- 只安装来自可信来源的 Skills
- 对不受信来源的 Skill，彻底审计其文件内容和代码依赖
- 注意 Skill 中引导 Claude 连接外部不受信网络的指令

### 两种技能类型

[[Anthropic]] 将 Agent Skills 分为两类，这一[[区分]]对测试策略有重要含义：

| 类型 | 定义 | 示例 | 测试关注点 |
|------|------|------|-----------|
| **能力提升（Capability Uplift）** | 帮助 Claude 完成基础模型无法完成或无法稳定完成的任务 | 文档创建技能（PDF、PPT 等） | 模型能力提升后可能变得不再必要 |
| **编码偏好（Encoded Preference）** | Claude 已能完成每个环节，但技能按团队流程编排顺序 | NDA 审核流程、周报草稿生成 | 价值取决于与实际工作流的契合度 |

**关键洞察**：能力提升类技能可能随模型进步而变得不再必要（评估能帮你判断何时发生）；编码偏好类技能更持久，但价值取决于其与实际流程的契合度。

### Skill-Creator 评估框架

[[Anthropic]] 推出的 skill-creator 增强功能将软件开发的严谨流程（测试、基准测试、迭代优化）引入技能创作，无需编写代码。

**Evals（评估脚本）**：定义测试提示词（必要时加文件），描述合格标准，skill-creator 验证技能是否符合要求。两个重要用途：
1. **捕捉质量回归**：模型和基础设施演进时，上个月有效的技能今天可能表现不同。针对新模型运行 evals 能提前发现变化信号。
2. **判断模型能力是否已超越技能**：主要针对能力提升类技能。如果基础模型在**未加载技能**的情况下就能通过 evals，说明技能的技术可能已被整合到模型默认行为中——技能未失效，只是不再必要。

**基准测试模式（Benchmark Mode）**：使用 evals 运行标准化评估，跟踪评估通过率、耗时和令牌使用量。可在模型更新后或技能迭代时运行。

**多智能体并行评估**：启动独立智能体并行运行 evals，每个在干净上下文中运行，拥有独立的令牌和计时指标，避免交叉干扰。

**对比智能体（Comparator Agents）**：用于 A/B 对比——两个技能版本，或技能 vs 无技能。它们在判断输出时不知道哪个是哪个，从而判断改动是否真正有效。

### 描述优化：精准触发

随着技能数量增长，描述精度变得至关重要：太宽导致误触发，太窄导致不触发。Skill-creator 能：
- 对照示例提示词分析当前描述
- 提出修改建议，同时减少误触发（false positives）和漏触发（false negatives）
- [[Anthropic]] 在 6 项公开文档创建技能中测试，5 项触发效果得到提升

### 展望未来：从"如何做"到"做什么"

[[SKILL.md 格式规范|SKILL.md]] 文件本质上是实施计划，告诉 Claude *如何* 做某事。随模型能力提升，仅用自然语言描述*该技能应实现什么*可能就足够了，模型自行完成其余部分。Evals 已经描述了"是什么"——最终，这一描述可能成为技能本身。

### 在 Anthropic 生态中的位置

Agent Skills 是开放标准，支持：Claude.ai、[[Claude Code]]、Claude Agent SDK、Claude Developer Platform。

与 [[MCP协议层]] 的互补关系：MCP 连接工具和服务，Skills 教导 Agent 如何使用这些工具和服务的复杂工作流。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/Equipping agents for the real world with Agent Skills.md]] — Agent Skills 原始发布
- [[raw/articles/ai-engineering/claude-blog/Improving skill-creator_ Test, measure, and refine Agent Skills.md]] — Skill-Creator 评估框架、基准测试、多智能体支持、描述优化

## 相关

- [[渐进式披露-Progressive-Disclosure]] — implements（Skills 是渐进式披露在 Agent 知识管理中的具体实现）
- [[即时上下文检索]] — implements（Skills 的按需加载机制是 JIT 检索的应用）
- [[Context-Engineering]] — part_of（Skills 是上下文工程中知识注入的模块化手段）
- [[Claude-Code]] — implemented_by（Claude Code 是 Skills 的主要运行环境）
- [[MCP协议层]] — related_to（Skills 和 MCP 是互补的能力扩展机制）
