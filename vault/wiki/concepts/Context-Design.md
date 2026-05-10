---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: '2026-04-25'
source_count: 3
tags: [技术, 方法论, AI, AI工程, 上下文管理]
aliases: ["上下文设计", "Context OS", "Pareto-aware Context OS"]
relates_to:
  - target: '[[Context Engineering]]'
    type: extends
    confidence: 0.9
  - target: '[[分层记忆架构]]'
    type: implements
    confidence: 0.85
  - target: '[[检索增强生成]]'
    type: incorporates
    confidence: 0.8
  - target: '[[Prompt缓存]]'
    type: incorporates
    confidence: 0.75
  - target: '[[上下文压缩]]'
    type: incorporates
    confidence: 0.85
  - target: '[[注意力预算]]'
    type: builds_on
    confidence: 0.9
  - target: '[[上下文腐烂]]'
    type: addresses
    confidence: 0.85
  - target: '[[即时上下文检索]]'
    type: implements
    confidence: 0.75
  - target: '[[RAG]]'
    type: incorporates
    confidence: 0.8
  - target: '[[Zipf定律]]'
    type: applies
    confidence: 0.9
  - target: '[[帕累托法则]]'
    type: applies
    confidence: 0.9
  - target: '[[Bradford定律]]'
    type: applies
    confidence: 0.85
  - target: '[[Matthew效应]]'
    type: addresses
    confidence: 0.8
  - target: '[[Benford定律]]'
    type: applies
    confidence: 0.75
  - target: '[[幂律分布]]'
    type: related_to
    confidence: 0.8
supersedes: null
---

# Context-Design

## 概述
Context-Design（上下文设计）是一种基于经验规律的[[上下文管理系统]]设计方法论，强调将上下文视为有限缓存而非聊天记录拼接器。该方法论由 [[Anthropic]] 将 context engineering 定义为对有限上下文的策展和管理时确立，核心思想是在固定 token 预算下最大化有用信息密度。

## 关键内容

### 1. 经验规律驱动的设计原则
Context-Design 通过四大经验规律指导[[Context Management|上下文管理]]：
- **Zipf / Pareto**：绝大多数价值来自少数热点上下文，采用热/温/冷分层，而非所有历史平权
- **Bradford / Lotka / Price**：少数核心来源覆盖大多数高价值信息，建立 source prior、canonical source pack、每源上限
- **Matthew effect**：先进入上下文的材料会放大后续推理偏向，强制多源检索、反证位、去单源垄断
- **Benford 式思路**：用分布基线找异常，监控 source share、stale fact rate、retrieval drift、无效 token 占比

### 2. 请求路由（Router-first）
第一层是路由判断，而非直接检索：
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

### 3. 五层内存架构
- **L0 Cached Prefix**：固定不变的系统提示、输出 schema、少量 few-shot、工具契约
- **L1 Working Memory**：当前任务目标、约束、实体、术语表、未解决问题、当前计划
- **L2 Episodic Memory**：按阶段压缩的"回合摘要"，只保留决策、证据、结论、pending items
- **L3 Semantic Memory**：向量检索 + 关键词检索 + 元数据过滤的长期知识层
- **L4 Raw Archive**：原始会话、原始文档、原始工具输出，默认不直接进 prompt，只在需要时回放

### 4. Memory Object 模型
上下文管理的对象应是 memory object，而非 message：
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

### 5. 混合检索链路
采用按需检索 + 混合检索 + 重排 + 去重 + 反证位：
- **query understanding → need_retrieval? → hybrid retrieve → contextualize → rerank → diversify → compress → assemble**
- 强制"前 N 条不能全来自同一文档/同一作者/同一系统"，防止 Matthew effect 式的早期锚定
- 专门保留"反证 / 边界条件 / 更新时间冲突"槽位

### 6. Prompt 位置编排
考虑到 Lost in the Middle 效应，推荐布局：
```
[Cached Prefix: system / policy / tool contract / output schema]
[Task contract: 这轮要解决什么]
[Working memory]
[Top evidence A]                     ← 最关键证据放靠前
[Compressed session summary]
[Supporting evidence B/C]
[Counter evidence / freshness note]  ← 关键约束放靠尾
[Current user ask]
[Final answer rubric]
```

### 7. 压缩策略：提炼可复用状态
压缩目标是把"历史噪音"变成"未来可[[计算]]状态"，产出四种对象：
- **durable facts**：长期有效事实
- **decisions**：已做选择和理由
- **open loops**：未完成事项
- **source anchors**：原文锚点，便于回源

### 8. 评分函数
候选 memory/chunk 评分公式：
$$
score = 0.35 \cdot relevance + 0.20 \cdot source\_quality + 0.15 \cdot freshness + 0.10 \cdot salience + 0.10 \cdot dependency + 0.10 \cdot novelty - redundancy
$$

### 9. Token 预算分配
- **Cached Prefix**：10% — 系统指令、工具契约、output schema
- **[[工作记忆|Working Memory]]**：15% — 当前任务、约束、实体
- **Recent Turns**：15% — 近期对话
- **Retrieved Evidence**：35% — 检索结果
- **Episodic Summaries**：15% — 阶段压缩摘要
- **Output Contract**：10% — 输出要求、checklist

### 10. 工具密集 Agent 的上下文管理
工具状态外置，只回注必要结果：
- 工具 schema 常驻 L0，但尽量精简
- 工具原始输出留在外部存储
- 回注到 prompt 的只有：结果摘要、关键 delta、error message、下一步所需最小证据
- **原则**：把"结果"放进上下文，不把"过程全量日志"放进上下文

### 11. 评估指标
- **Context utilization**：注入的 token 里，最后真正被引用/使用了多少
- **Answer quality @ fixed budget**：固定预算下质量是否更高
- **Stale fact rate**：过期信息混入比例
- **Source dominance**：单一来源是否垄断前几条证据
- **Position robustness**：把关键证据换位置后，答案是否明显劣化
- **Cache hit rate / latency / cost**：[[KV 缓存命中率|前缀缓存]]是否真的起作用

## 来源
- [[raw/articles/ai-engineering/prompt-context/context-design.md]] — 经验规律、分层架构、混合检索等核心设计
- [[Context Engineering]] — 基础理论和方法论
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic 官方指导

## 相关
- [[Context Engineering]] — extends
- [[分层记忆架构]] — implements
- [[检索增强生成]] — incorporates
- [[Prompt缓存]] — incorporates
- [[上下文压缩]] — incorporates
- [[注意力预算]] — builds_on
- [[上下文腐烂]] — addresses
- [[即时上下文检索]] — implements
- [[Zipf定律]] — applies
- [[帕累托法则]] — applies
- [[Bradford定律]] — applies
- [[Matthew效应]] — addresses
- [[Benford定律]] — applies