---
type: concept
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["agent-pattern", "signaling", "state-verification", "Agent系统"]
aliases: ["Completion Signal", "完成信号", "COMPLETE 信号", "<promise>COMPLETE</promise>"]
relates_to:
  - target: "[[Ralph Loop]]"
    type: used_by
  - target: "[[Agent 迭代循环]]"
    type: part_of
  - target: "[[双重验证]]"
    type: requires
  - target: "[[PRD 驱动开发]]"
    type: relates_to
supersedes: null
---

# 完成信号机制（Completion Signal Mechanism）

## 概述
完成信号机制是 [[Agent 迭代循环]]中用于标记单次迭代结束的标准化通信协议，通过 `<promise>COMPLETE</promise>` XML 标签实现外循环对 Agent 实例完成状态的可靠检测。

## 关键内容

1. **信号格式**：`<promise>COMPLETE</promise>`
   - **XML 标签格式**：不容易出现在普通文本或代码输出中，避免误触发
   - **明确语义**：`promise` 表示 Agent 主动承诺任务完成，而非被动结束
   - **grep 可检测**：`grep -q "<promise>COMPLETE</promise>"` 简单可靠
   - **可扩展**：也可用 `<promise>BLOCKED</promise>` 等变体传递状态

2. **为什么选择这个格式**：
   - 普通文本标记（如 `DONE`、`FINISHED`）容易在代码输出中误触发
   - XML 标签提供了结构化的边界，grep 检测精确
   - `promise` 语义强调 Agent 的主动承诺，[[区分]]于异常退出

3. **与 [[双重验证]] 的关系**：仅检测信号字符串是不够的——Agent 可能输出完成信号但实际工作未完成。必须配合[[双重验证（Dual Verification）|双重验证]]：
   - **Step 1**：检测文本信号 `grep -q "<promise>COMPLETE</promise>"`
   - **Step 2**：验证 prd.json 实际状态（防止 Agent 撒谎）
   - 只有两者同时确认才真正退出循环

4. **在 [[Agent 迭代循环]] 中的位置**：完成信号是每次迭代的最后一个动作，在代码实现、验证、[[Git Commit|Git 提交]]、progress.txt 更新之后输出。无论 Story 是否还有未完成，每次迭代都必须输出此信号。

5. **信号变体**：
   - `<promise>COMPLETE</promise>` — 正常完成
   - `<promise>BLOCKED</promise>` — 被阻塞，需要人工介入
   - 可扩展为更多状态信号

6. **与 [[PRD 驱动开发]] 的关系**：完成信号触发外循环检查 prd.json 的完成度。信号只是"声明"，prd.json 才是"事实"——两者的一致性由[[双重验证（Dual Verification）|双重验证]]保证。

## 来源
- [[raw/articles/ai-tools/ralph-loop/how-the-loop-works.md]] — Ralph Loop 核心原理深度解析

## 相关
- [[Ralph Loop]] — used_by（Ralph Loop 外循环检测此信号决定是否继续）
- [[Agent 迭代循环]] — part_of（每次迭代的最后一个动作）
- [[双重验证]] — requires（信号必须与 prd.json 状态交叉验证）
- [[PRD 驱动开发]] — relates_to（信号触发外循环检查 PRD 完成度）
