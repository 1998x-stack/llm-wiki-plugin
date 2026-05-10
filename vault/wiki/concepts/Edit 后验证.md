---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 3
tags: [AI, 方法论, AI工程]
aliases:
- Edit 后验证
- Post-Edit Validation
- 编辑后校验
relates_to:
- target: "[[Guardrails]]"
  type: implements
  confidence: 0.95
- target: "[[恢复机制]]"
  type: uses
  confidence: 0.9
- target: "[[SWE-agent]]"
  type: depends_on
  confidence: 0.85
- target: "[[环境反馈设计]]"
  type: extends
  confidence: 0.8
supersedes: null
---

# Edit 后验证

## 概述

Edit 后验证是 Agent 编辑系统中的即时校验机制，在每次代码编辑完成后立即运行语法检查、lint 或 LSP 诊断，确保新编辑未引入错误，并在发现问题时快速反馈给 agent 进行修正。

## 关键内容

### SWE-agent 的实现方式

**论文版核心思路：编辑护栏（Edit [[Guardrails]]）**
- edit 完以后立刻做检查
- 如果新编辑引入语法错误，就不应用这次编辑
- 把错误信息、原代码片段、应用后会长什么样，都反馈给 agent
- 让 agent 重新 edit，而不是把坏状态写进[[仓库]]继续往下走

**当前[[仓库]]实现（str_replace_editor）：**
- `USE_LINTER` 开关：是否启用 linter
- `flake8(file_path)`：对文件运行 flake8，仅对 .py 文件生效
- 默认 `LINT_COMMAND`：`flake8 --isolated --select=F821,F822,F831,E111,E112,E113,E999,E902 {file_path}`

**选中的错误码含义：**

| 错误码 | 类别 | 说明 |
|--------|------|------|
| F821/F822 | 未定义名 | 变量/函数未声明 |
| F831 | 重复参数 | 函数参数名重复 |
| E111/E112/E113 | 缩进 | 缩进不一致或缺失 |
| E999 | 语法错误 | [[Python]] 语法解析失败 |
| E902 | 文件 IO | 文件无法读取 |

**两种模式：**
1. **Reject 模式**（主线）：编辑未通过 lint → 不应用，告诉 agent "Your changes have NOT been applied"
2. **Warning 模式**：编辑已应用，但 linter 发现 syntax errors → 发告警但不回滚

### 增量诊断设计

[[SWE-agent]] 的 linter 不是简单地跑完就返回全部问题，而是做了 **previous errors filtering**：
- 更新旧错误的行号（因为编辑可能改变了行号）
- 过滤掉编辑窗口之外的旧 flake8 问题
- 尽量只保留和本次 edit 真正相关的新错误

这非常像 IDE 的"增量诊断"而非"全仓静态审判"。

### 为什么不做完整 LSP/全量检查

[[SWE-agent]] 当时没把 validate 做成完整 LSP/全量检查的原因：

1. **轨迹可持续优先**：目标是让 agent 在长轨迹里少走弯路，不是每步做最强静态分析
2. **全量检查对 agent 不友好**：
   - 慢：每次 edit 后跑全仓太耗时
   - 噪声大：容易把 agent 淹没
   - 历史问题混入：很难[[区分]]"这次 edit 导致的新问题"和"[[仓库]]本来就有的问题"
3. **[[Python]]-first 导向**：核心 validate 抽象更偏 [[Python]]，linter 路径明确只对 .py 生效
4. **复杂度收缩**：官方已将 [[SWE-agent]] 转向 maintenance-only，建议用 mini-[[SWE-agent]]

### 三层 Validate 设计建议

如果要做一个更强的 SWE agent，建议分三档：

**档 1：必跑（毫秒到秒级）**
- parser / syntax 检查
- indentation 检查
- import resolution basics
- 单文件 LSP diagnostics
- 只返回新引入问题

**档 2：条件触发**
- 当 edit 涉及 public API / types / build files 时
- 跑 changed-files typecheck / LSP workspace slice
- 跑相关单测或 reproduction script

**档 3：提交前**
- 最小测试集
- changed-files lint/typecheck
- 必要时 repo smoke test

### LSP 触发策略

不要每次 edit 后全量 workspace，建议：

| 触发时机 | 范围 | 目标延迟 |
|---------|------|---------|
| `on_edit(file)` | 单文件增量诊断 | 0.2–2 秒 |
| `on_cross_file_signal` | 相关依赖图扩展 | 2–10 秒 |
| `on_submit` | changed-files / targeted workspace diagnostics | 10–30 秒 |

### Observation 返回格式

不要直接把 LSP 原始 JSON 全塞给模型，应压成 agent-friendly 格式：
- `file`：文件名
- `range`：行号范围
- `severity`：严重程度
- `message`：错误信息
- `是否新引入`：标记是否本次 edit 导致
- `是否阻断提交`：是否阻止继续

这符合 [[SWE-agent]] 强调的 **specific + concise** 设计逻辑。

### Ablation Study 证据

[[SWE-agent]] 论文 Table 3 专门对 editor interface 做了 ablation，验证了 edit 后 validate 的有效性：

| [[Configuration|配置]] | [[SWE-bench]] Lite Resolved Rate | 说明 |
|------|----------------------------|------|
| **w/ linting** | **18.0%** | 带 linting 的 edit（最佳） |
| **edit action** | **15.0%** | 有专门 edit 动作但不带 linting |
| **No edit** | **10.3%** | 没有专门 edit 工具，靠 shell 方式改文件 |

**两层结论：**
1. **有专门 edit 工具本身就重要**：从 No edit (10.3) 到 edit action (15.0)，把编辑变成紧凑、受约束的专门动作，本身就能显著提升效果（+4.7 点）。
2. **edit 后做 validate / linting 进一步显著有益**：从 15.0 到 18.0（+3.0 点），说明仅仅"能编辑"还不够，把坏编辑拦下来、把语法/缩进类错误尽早暴露出来，会明显减少错误传播。

**准确表述**：论文这里验证的主要是 linting / syntax-level guardrail，不是完整的 LSP/全仓语义检查。它证明的是"edit 后做轻量、即时的有效性校验有帮助"，而非"必须上完整 LSP 才有效"。

### Claude Code 分层验证方案

在 [[Claude Code]] 平台中，edit 后验证被设计为**四层架构**（详见 [[Claude Code 分层验证]]）：

| 层级 | 职责 | 机制 |
|------|------|------|
| **Tool Description** | "会用"：教会 [[Claude_Code|Claude]] 如何正确调用 validate 工具 | 参数语义 + 使用示例 |
| **[[CLAUDE.md]]** | "想这么做"：定义项目验证策略和偏好 | 每个会话加载的持久指令 |
| **[[Hooks]] / settings.json** | "真的会做"：PostToolUse 自动触发 lint/test | additionalContext + decision:block |
| **LSP** | "即时反馈"：edit 后自动报告 type errors/warnings | 内建 code intelligence |

**核心原则**：必须发生的放 hooks，希望 [[Claude_Code|Claude]] 优先做的放 [[CLAUDE.md]]，自定义工具用法放 tool description + examples，快速语义反馈交给 LSP。

### 单文件 vs 多文件编辑

- **单次工具调用**：针对一个 path，作用对象是一个文件
- **整个 agent run**：可以连续修改多个文件、创建新文件、回退编辑
- 当前编辑器支持 `view/create/str_replace/insert/undo_edit`
- 多文件修改通过多次工具调用实现，不是原子性的 batch multi-file edit

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/10-swe-agent 每次 edit后，如何设计lintlsp 等validate？.md]] — SWE-agent edit 后 validate 设计详解
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/11-SWE-agent 是否对 edit 是否 validate 做了 ablation study？有.md]] — Edit validate ablation study 结果（Table 3）
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/12-claude code中，edit后做 validate  linting，需要在tool des.md]] — Claude Code 分层验证设计

## 相关

- [[Guardrails]] — implements（Edit 后验证是 Guardrails 的具体实现之一）
- [[恢复机制]] — uses（验证失败后触发恢复流程）
- [[SWE-agent]] — depends_on（基于 SWE-agent 的编辑系统设计）
- [[环境反馈设计]] — extends（验证结果作为环境反馈的一种形式）
- [[Claude Code 分层验证]] — caused（Edit 后验证理念在 Claude Code 中的分层实现）
