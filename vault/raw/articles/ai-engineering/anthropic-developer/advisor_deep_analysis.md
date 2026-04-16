# Anthropic Advisor Tool 底层逻辑深度分析

> 版本：advisor-tool-2026-03-01 Beta  
> 分析日期：2026-04  
> 参考：[官方文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool)

---

## 一、核心设计哲学：不是"另一个模型调用"，而是"生成流内的策略审阅器"

Advisor Tool 的根本创新在于**它打破了多模型协作必须多次 HTTP 往返的惯例**。传统多 Agent 框架（LangGraph、AutoGen、CrewAI）的范式是：

```
Client ──→ Model A (generates plan) ──→ Client ──→ Model B (executes) ──→ ...
               N次网络往返
```

而 Anthropic 的 Advisor 模式是：

```
Client ──→ /v1/messages ─┬──→ Executor (Sonnet/Haiku) 流式输出
                          │       ↓ 触发 server_tool_use(name="advisor")
                          │   [服务端内部]
                          │       ↓ Advisor (Opus) 独立推理（不流式）
                          │       ↓ advisor_tool_result 注入 Executor 上下文
                          └──→ Executor 继续流式输出
                          
               整个过程 = 1次 HTTP 请求
```

**设计意图的三层含义：**

| 层次 | 含义 | 工程影响 |
|------|------|---------|
| 协议层 | 一次请求内部完成多模型协作 | 无网络往返延迟，无客户端编排复杂度 |
| 认知层 | Advisor 是"策略审阅器"而非"另一个执行者" | Advisor 不产出最终答案，只给高层建议 |
| 经济层 | 昂贵模型只做关键决策，廉价模型完成 bulk generation | 接近 Opus-solo 质量，接近 Sonnet-solo 成本 |

---

## 二、协议机制精解

### 2.1 触发流程的六个关键节点

```
[时序图]

Executor                    Server-Side                Advisor (Opus)
  │                              │                          │
  │ 生成文本...                   │                          │
  │ ──server_tool_use──────────→ │                          │
  │   {name:"advisor",input:{}}  │                          │
  │                              │ ──完整 transcript ──────→ │
  │                              │   (system+tools+history)  │ 独立推理
  │  [流暂停]                     │                          │ (extended thinking内部)
  │  [keepalive pings ~30s]      │                          │ thinking blocks 丢弃
  │                              │ ←─advisor_tool_result────│
  │                              │   (只有advice text)       │
  │ ←─advisor_tool_result──────  │                          │
  │ 继续流式生成...                │                          │
```

### 2.2 关键设计决策详解

#### A. `input: {}` 永远为空 —— 为什么？

Executor 在调用 advisor 时 **不传任何参数**，原因是：
- Advisor 看到的上下文由服务端自动构建（完整的 messages + system + tools）
- 不允许 Executor "选择性隐瞒"上下文，确保 Advisor 获得完整视角
- 防止 Executor 通过参数影响 Advisor 的决策（避免 prompt injection 链路）

这是一个**信息对称设计**：Advisor 永远比 Executor 信息更全（它看到了 Executor 的全部历史，Executor 看不到 Advisor 的 thinking）。

#### B. Thinking blocks 被丢弃

Advisor 使用 extended thinking 推理，但返回给 Executor 的 `advisor_tool_result.content.text` **只包含最终建议文本**（400-700 tokens），不含 thinking（1400-1800 tokens 含 thinking 时的总体大小）。

这不是节省 token 的小优化，而是一个**架构选择**：
- 防止 Executor 被 Advisor 的推理过程干扰（只需要"结论"）
- 保持 Executor 的自主性（它接收建议，不接收推理链）
- 和人类协作的类比：你问高级顾问的意见，他给你结论和建议，不给你他内心的全部思考过程

#### C. `advisor_redacted_result` —— 加密变体

当 Advisor 返回的是 `advisor_redacted_result`（`encrypted_content` 字段），**客户端无法读取内容**，但必须原样传回下一轮请求。服务端解密后将明文注入 Executor 的 prompt。

这是一个**零知识中继设计**，应用场景包括：
- 企业 ZDR（Zero Data Retention）场景
- 未来可能的敏感建议隔离（不暴露给客户端 SDK）

```python
# 正确处理两种变体
for block in response.content:
    if block.type == "advisor_tool_result":
        if block.content.type == "advisor_result":
            advice_text = block.content.text  # 可读
        elif block.content.type == "advisor_redacted_result":
            encrypted = block.content.encrypted_content  # 不可读，原样传回
```

---

## 三、Token 计费架构：双层迭代模型

### 3.1 `usage.iterations[]` 的三阶段结构

```json
{
  "usage": {
    "input_tokens": 412,    // ← 仅 Executor 第一轮输入
    "output_tokens": 531,   // ← 所有 Executor 轮次输出之和
    "iterations": [
      {
        "type": "message",          // Executor 第一阶段（触发前）
        "input_tokens": 412,
        "output_tokens": 89
      },
      {
        "type": "advisor_message",  // Advisor 独立推理
        "model": "claude-opus-4-6",
        "input_tokens": 823,        // Executor全量上下文 ≈ 412 + 89 + overhead
        "output_tokens": 1612       // 含 thinking tokens
      },
      {
        "type": "message",          // Executor 第二阶段（建议后）
        "input_tokens": 1348,       // = 823 + advisor result tokens
        "cache_read_input_tokens": 412,
        "output_tokens": 442
      }
    ]
  }
}
```

### 3.2 成本优化数学

假设任务需要 2000 output tokens，单次 Advisor 调用：

| 方案 | 计费构成 | 相对成本 |
|------|---------|---------|
| Opus-solo | 2000 × Opus_out_rate | 100% |
| Advisor (Sonnet+Opus) | 1612×Opus_out + (89+442)×Sonnet_out | ~35-50% |
| Sonnet-solo | 2000 × Sonnet_out_rate | ~15-20% |

核心逻辑：**高质量来自 Advisor 的规划，低成本来自 Executor 的 bulk generation**。Opus 只花费 ~1600 tokens 做思考，Executor 花 500+ tokens 实现——而这 500 tokens 用的是 Sonnet 价格。

---

## 四、流式行为与客户端处理

### 4.1 流式事件序列

```
data: {"type":"content_block_start","index":0,"content_block":{"type":"text"...}}
data: {"type":"content_block_delta","delta":{"type":"text_delta","text":"Let me..."}}
...
data: {"type":"content_block_stop","index":0}                    # Executor 文本结束

data: {"type":"content_block_start","index":1,                   # Advisor 调用开始
       "content_block":{"type":"server_tool_use","name":"advisor","input":{}}}
data: {"type":"content_block_stop","index":1}                    # 流暂停点

# ← 此处静默，仅有 30s keepalive pings

data: {"type":"content_block_start","index":2,                   # Advisor 结果（整体到达）
       "content_block":{"type":"advisor_tool_result",...}}
data: {"type":"content_block_stop","index":2}                    # 无 delta 事件！

data: {"type":"content_block_start","index":3,"content_block":{"type":"text"...}}
data: {"type":"content_block_delta",...}                         # Executor 继续流式
...
```

**关键**：`advisor_tool_result` **不发 delta**，一次性 `content_block_start` 携带完整内容。客户端需处理这种"突然完整到达"的语义。

### 4.2 `pause_turn` 的边缘情况

如果 `server_tool_use(name="advisor")` 是最后一个 content block 时触发了 `pause_turn`，响应以 `stop_reason: "pause_turn"` 结束。此时 Advisor 推理**尚未执行**，在 resume 时服务端才真正运行 Advisor。客户端需正确保留这个悬空的 `server_tool_use` block。

---

## 五、缓存架构：双层独立缓存

```
[Executor 侧缓存]
Turn N: [...messages, advisor_tool_result(N)]
                                ↑
                    cache_control breakpoint 在此之后
Turn N+1: 命中 Executor 侧缓存，节省重复 input tokens

[Advisor 侧缓存]（需在 tool definition 中声明 caching）
Advisor Call 1: 写入完整 transcript 缓存
Advisor Call 2: 读取 Call 1 缓存 + 新增 delta 部分
Advisor Call 3: 读取 Call 2 缓存 + 新增 delta 部分
```

**Advisor 侧缓存的盈亏平衡点：3次调用**  
原因：首次 cache write 有额外成本，第2次开始节省。3次以下，cache write 开销 > 节省。

**与 `clear_thinking` 的冲突**：  
若开启 extended thinking 且未显式设置 `keep: "all"`，默认 `keep: {type: "thinking_turns", value: 1}` 会导致每轮 Advisor 看到的 transcript 结构变化（thinking blocks 被裁剪），破坏 cache prefix 稳定性。

```python
# 正确配置：保留所有 thinking 以维持 Advisor 缓存稳定性
response = client.beta.messages.create(
    ...
    thinking={"type": "enabled", "budget_tokens": 8000},
    context_management={"clear_thinking": {"keep": "all"}},  # 关键！
)
```

---

## 六、与主流多智能体模式的对比分析

| 维度 | Advisor Tool | LangGraph Multi-Agent | Self-Consistency | CoT Prompting |
|------|-------------|----------------------|-----------------|---------------|
| 网络往返 | 1次 | N次 | N次 | 1次 |
| 模型异构 | ✅ 原生支持 | ✅ 需手动路由 | ❌ 通常同模型 | ❌ 单模型 |
| Advisor 可见上下文 | 完整 transcript | 需手动传递 | - | - |
| Executor 自主性 | 保留（建议≠命令）| 依设计而定 | - | 无 |
| 成本控制粒度 | `max_uses` + client-side | 完全自定义 | 固定倍数 | 无 |
| 流式支持 | ✅（Advisor 暂停流） | 需自行实现 | ❌ | ✅ |
| Thinking 可见性 | Advisor thinking 丢弃 | 可配置 | - | - |

**核心差异本质**：Advisor Tool 是"服务端编排"，其他方案是"客户端编排"。服务端编排的优势在于：
1. 延迟最优（无额外 RTT）
2. 上下文完整性保证（服务端确保 Advisor 获得完整信息）
3. 协议可信性（`input: {}` 无法被 Executor 篡改）

---

## 七、本地复刻的三个设计原则

根据上述分析，任何本地实现（LangGraph + 异构模型）必须保留：

### 原则 1：服务端语义等价性
Advisor 必须收到完整的 messages 历史（包括所有 tool_results），不能只收到摘要或 Executor 的"主动传递"。

### 原则 2：结构化状态传递
Advisor 的建议必须作为 `ToolMessage`（而非普通文本）注入对话历史，因为 Executor 在推理时会区分 tool_result 和用户输入的语义权重。

### 原则 3：Executor 保持主控
Advisor 给建议，Executor 决定采纳程度。不要让 Advisor 直接写出最终答案，这会破坏成本优化的核心逻辑。

---

## 八、适用场景与反适用场景

### 强适用
- **长链代码生成**：exploratory reads → advisor call → write → test → advisor call
- **多步研究 Pipeline**：搜索多源 → advisor 综合建议 → 撰写
- **Computer Use**：截图分析 → advisor 规划下一步 → 执行

### 弱适用 / 反适用
- **单轮 Q&A**：没有"规划"的必要，纯浪费 Advisor tokens
- **实时低延迟场景**：Advisor 推理暂停流，P99 延迟不可接受
- **纯机械重复任务**：数据格式转换等，规划价值为零

---

## 九、已知限制与未来方向

| 限制 | 当前状态 | 推测方向 |
|------|---------|---------|
| `clear_tool_uses` 与 advisor 不兼容 | 官方声明修复中 | 下个版本支持 |
| 无对话级 cap | 需客户端手动计数 | 可能增加 conversation-level `max_uses` |
| Advisor 不能用工具 | 当前限制 | 可能开放只读工具（搜索）|
| 仅支持 Haiku/Sonnet+Opus 配对 | 当前限制 | 可能扩展到第三方模型 |
| 流式暂停无进度反馈 | keepalive pings | 可能增加 advisor_thinking_delta |

---

*本文基于官方文档及协议层分析，部分内部实现为推断，以官方文档为准。*
