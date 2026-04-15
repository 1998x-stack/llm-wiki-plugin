---
type: concept
title: Context Engineering
status: active
confidence: 0.92
created: 2026-04-15
updated: 2026-04-15
last_accessed: '2026-04-16'
source_count: 2
tags:
- 技术
- 方法论
- AI
aliases:
- 上下文工程
- 有限注意力预算调度
- Context OS
relates_to:
- target: '[[分层记忆架构]]'
  type: uses
  confidence: 0.95
- target: '[[LLM-Statelessness]]'
  type: extends
  confidence: 0.88
- target: '[[检索增强生成]]'
  type: uses
  confidence: 0.9
- target: '[[Prompt缓存]]'
  type: uses
  confidence: 0.85
- target: '[[上下文腐烂]]'
  type: related_to
  confidence: 0.95
- target: '[[即时上下文检索]]'
  type: related_to
  confidence: 0.9
supersedes: null
---

# Context Engineering

## 概述

Context Engineering（上下文工程）是指对 LLM 的有限上下文窗口进行策展与管理的系统化方法。Anthropic 将其定义为：在固定 token 预算下最大化有用信息密度，而非简单地将聊天历史拼接填满窗口。核心隐喻是把上下文当作**有限缓存**（Cache）和**工作集**（Working Set），而非日志记录器。

## 关键内容

### 四条经验规律驱动的设计原则

| 规律 | 上下文工程含义 | 工程手段 |
|------|--------------|---------|
| **Zipf / Pareto** | 绝大多数价值来自少数热点上下文 | 热/温/冷分层，优先权加权 |
| **Bradford / Lotka** | 少数核心来源覆盖大多数高价值信息 | source prior、每源上限（per-source cap） |
| **Matthew Effect** | 早进入上下文的材料放大后续推理偏向 | 强制多源检索、反证位（counter-evidence lane） |
| **Benford 式思路** | 用分布基线发现异常 | 监控 source share、stale fact rate、retrieval drift |

### 请求路由（Router-first）

第一层不是检索，而是**路由判断**：

```
if kb_size < 200k and low_churn and low_tooling:
    mode = "full_context_cached"
elif task_is_knowledge_intensive:
    mode = "retrieval_augmented"
elif session_is_long_running:
    mode = "hierarchical_memory"
else:
    mode = "hybrid_agent"
```

Anthropic 建议：知识库小于约 200k tokens 且相对稳定时，直接放入 prompt 往往是最简单方案。

### 检索链路：按需混合检索

**query understanding → need_retrieval? → hybrid retrieve → contextualize → rerank → diversify → compress → assemble**

关键环节：
1. **need_retrieval?** — 先判断能否靠 working memory 回答
2. **hybrid retrieve** — 同时跑 dense + BM25 + metadata filter + graph hop
3. **contextualize chunk** — 给每个 chunk 补最小必要上下文（标题、章节、时间）
4. **rerank + diversify** — 考虑 source quality / freshness / novelty / redundancy penalty / per-source cap
5. **counter-evidence lane** — 保留 1 个"反证/边界条件"槽位，防止 Matthew effect 锚定

### Prompt 位置编排

_Lost in the Middle_ 研究表明关键信息埋在中段时模型利用效果显著下降。推荐布局：

```
[Cached Prefix: system / policy / tool contract / output schema]
[Task contract: 这轮要解决什么]
[Working memory]
[Top evidence A]             ← 最关键证据放靠前
[Compressed session summary]
[Supporting evidence B/C]
[Counter evidence / freshness note]  ← 关键约束放靠尾
[Current user ask]
[Final answer rubric]
```

对真正不能丢的约束，**允许重复一次**比埋在中间更稳。

### 压缩目标：可复用状态，而非摘要

压缩应产出四种结构化对象，而非自由文本摘要：

- **durable facts** — 长期有效事实
- **decisions** — 已做选择和理由
- **open loops** — 未完成事项
- **source anchors** — 原文锚点，便于回源

压缩触发条件：任务阶段切换 / 关键决策 / 工具返回超长结果 / token 预算逼近阈值。

⚠️ 禁止压缩的内容：数字/合同/代码逻辑（会失真）、事实与推断混写（无法审计）。

### Memory Object 模型

上下文管理的对象不应是 message，而应是 **memory object**：

```json
{
  "id": "mem_xxx",
  "type": "fact|decision|preference|plan|episode",
  "text": "用户更关心 latency 而不是 peak accuracy",
  "source": "chat:turn_18",
  "freshness": "2026-04-14",
  "salience": 0.82,
  "reuse_count": 6,
  "confidence": 0.91,
  "anchors": ["turn18", "doc:spec#p4"]
}
```

### Token 预算分配（参考值）

| 层 | 比例 | 内容 |
|---|---|---|
| Cached Prefix | 10% | 系统指令、工具契约、output schema |
| Working Memory | 15% | 当前任务、约束、实体 |
| Recent Turns | 15% | 近期对话 |
| Retrieved Evidence | 35% | 检索结果 |
| Episodic Summaries | 15% | 阶段压缩摘要 |
| Output Contract | 10% | 输出要求、checklist |

Coding agent 场景：减少 Retrieved Evidence，增加 Working Memory + Tool Delta。
Enterprise QA 场景：Retrieved Evidence 提升至 ~45%。

### 候选 Memory 评分函数

$$
score = 0.35 \cdot relevance + 0.20 \cdot source\_quality + 0.15 \cdot freshness + 0.10 \cdot salience + 0.10 \cdot dependency + 0.10 \cdot novelty - redundancy
$$

按 token budget 做 knapsack 式选择，而非 top-k 直接截断。

### 评估指标（Pareto 风格）

- **Context utilization** — 注入 token 中真正被引用的比例
- **Answer quality @ fixed budget** — 固定预算下质量变化
- **Stale fact rate** — 过期信息混入比例
- **Source dominance** — 单一来源是否垄断前几条证据
- **Position robustness** — 换位置后答案是否明显劣化
- **Cache hit rate / latency / cost** — 前缀缓存效果

### 核心结论

> 大模型上下文管理不要围绕"聊天历史"设计，而要围绕"**价值密度**"设计；不要把上下文当日志，而要当**缓存、工作集、可审计记忆**。

设计公式：**分层记忆（hot/warm/cold） + 按需检索 + 混合检索与重排 + 结构化压缩 + 位置编排 + 工具状态外置 + 预算与评估闭环。**

### Anthropic 工程视角的补充（2026）

Anthropic Applied AI 团队对上下文工程的核心定位：**在任意时刻找到最小化的高[[信噪比]] token 集合，最大化目标行为的概率。**

**[[上下文腐烂]]（[[上下文腐烂|Context Rot]]）**：[[ChromaDB|Chroma]] Research 基准研究发现，随上下文 token 增加，模型从上下文中准确召回信息的能力持续下降。这不是硬性崖式截止，而是性能梯度——是上下文工程存在的核心动机。

**[[注意力预算]]（[[注意力预算|Attention Budget]]）**：[[Transformer架构|Transformer]] n² 注意力机制导致每个新 token 都消耗有限的[[注意力预算|注意力资源]]，上下文增长时每对 token 关系可获得的参数容量被稀释。

**长时任务的三种技术**（Anthropic 实践）：
1. **Compaction**：对话历史摘要压缩 → 适合需要流式回话的复杂推理
2. **[[结构化笔记法]]**（[[结构化笔记法|Agentic Memory]]）：Agent 将关键状态写入上下文外的持久存储 → 适合有明确里程碑的迭代开发
3. **多 Agent 架构**：子 Agent 处理深度工作并返回精简摘要 → 适合需要并行探索的复杂研究

**[[即时上下文检索]]（[[即时上下文检索|Just-in-Time Context]]）**：Agent 不预加载所有数据，而是持有轻量标识符（文件路径、URL、查询），运行时工具按需动态加载。Claude Code 的 glob/grep/Bash 模式是典型实现。

## 来源

- [[raw/articles/ai-engineering/prompt-context/context-design.md]]
- [[raw/articles/ai-engineering/anthropic-engineering/Effective context engineering for AI agents.md]]
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic
- [Lost in the Middle (Liu et al. 2023)](https://arxiv.org/abs/2307.03172)
- [Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) — MemGPT

## 相关

- [[分层记忆架构]]
- [[LLM-Statelessness]]
- [[检索增强生成]]
- [[Prompt缓存]]
- [[Agent Harness模式]]
- [[Claude-Code上下文工程全景]]
- [[上下文腐烂]] — 上下文工程的核心动机
- [[注意力预算]] — 核心约束条件
- [[即时上下文检索]] — 按需加载策略
- [[结构化笔记法]] — 长时任务持久记忆技术
- [[检索增强生成]] — 外部知识注入的主要技术路径
- [[情境化检索]] — 解决 RAG 上下文破坏的增强方案
