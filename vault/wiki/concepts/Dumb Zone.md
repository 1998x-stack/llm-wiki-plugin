---
type: concept
title: Dumb Zone
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["context-management", "agent-pattern", "ralph-loop", "Agent系统"]
aliases: ["Dumb Zone", "愚蠢区", "上下文退化区"]
relates_to:
  - target: "[[上下文策略]]"
    type: part_of
    confidence: 0.9
  - target: "[[上下文腐烂]]"
    type: relates_to
    confidence: 0.85
  - target: "[[上下文窗口]]"
    type: relates_to
    confidence: 0.85
  - target: "[[Ralph Loop]]"
    type: relates_to
    confidence: 0.8
supersedes: null
---

# Dumb Zone

## 概述
Dumb Zone 是 L[[LM Agent]] 上下文使用量超过安全阈值后进入的性能退化区域，此时模型推理质量显著下降但仍继续输出，导致 Agent 做出错误决策却不自知。[[Ralph Loop]] 的核心设计原则是在进入 Dumb Zone 之前主动退出并重启新实例。

## 关键内容

1. **定义与成因**：随着工具调用链不断向上下文追加内容（每次 read_file ~1.5-2k tokens、每次测试输出 ~3k tokens），上下文使用量持续增长。当超过某个阈值（通常为[[上下文窗口]]的 60-70%）时，模型进入 Dumb Zone——此时模型的[[注意力机制（Attention Mechanism）|注意力机制]]被大量历史信息稀释，推理能力退化，但模型本身不会报错或停止输出。

2. **各模型的 Dumb Zone 阈值**：
   | 模型 | Context | Dumb Zone 估计 |
   |------|---------|---------------|
   | [[Claude_Code|Claude]] 3.5 Sonnet | 200k tokens | >120k tokens |
   | [[Claude_Code|Claude]] 3 Opus | 200k tokens | >120k tokens |
   | GPT-4o | 128k tokens | >80k tokens |
   | [[Gemini CLI|Gemini]] 1.5 Pro | 1M tokens | >700k tokens |

3. **与 [[上下文腐烂]] 的关系**：Dumb Zone 是[[上下文腐烂]]在 Agent 工作流中的具体表现。[[上下文腐烂]]描述的是模型从上下文中准确召回信息的能力随 token 增加而非均匀下降；Dumb Zone 则是这种下降到影响 Agent 决策质量的临界区域。

4. **[[Ralph Loop]] 的应对策略**：不在 Dumb Zone 中强行完成任务，而是主动退出（输出 `<promise>COMPLETE</promise>`），由外循环启动一个拥有干净上下文的新 Agent 实例继续工作。这比在退化上下文中继续操作更可靠。

5. **为什么大窗口不能解决 Dumb Zone**：即使 [[Gemini CLI|Gemini]] 1.5 Pro 有 1M tokens 的[[上下文窗口]]，Dumb Zone 仍然存在（>700k tokens）。[[上下文策略]] 推荐即使在大窗口模型下也保持小粒度迭代（每迭代 1 Story），因为小粒度意味着更清晰的 [[Git Commit|git commit]] 和更低的失败恢复成本。

## 来源
- [[raw/articles/ai-tools/ralph-loop/context-strategies.md]] — Context Strategies 文档中的 Dumb Zone 定义与模型对比表

## 相关
- [[上下文策略]] — part_of（Dumb Zone 是上下文策略旨在避免的目标区域）
- [[上下文腐烂]] — relates_to（Dumb Zone 是上下文腐烂的临界表现）
- [[上下文窗口]] — relates_to（Dumb Zone 由上下文窗口使用比例定义）
- [[Ralph Loop]] — relates_to（Ralph 的核心设计是避免进入 Dumb Zone）
- [[Clean State Protocol]] — relates_to（干净状态协议确保迭代在 Dumb Zone 之前结束）
