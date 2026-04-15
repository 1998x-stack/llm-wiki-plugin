# OpenClaw ② BRAIN — Agent Runner & ReAct 推理引擎

> Brain 是 OpenClaw 的"思考器"。它将上下文组装、LLM 调用、工具执行、流式输出整合为一个可控的 6 阶段流水线。

---

## 1. Agent Runner 的定位

Agent Runner 将 Prompt 工程视为**机械化的组装任务**，而非玄学艺术：

```
输入：InboundMessage + Session 上下文
  │
  ▼
┌─────────────────────────────────────────────────────────┐
│                    Agent Runner                          │
│                                                          │
│  1. Model Resolver     → 选择/切换 LLM 提供商            │
│  2. System Prompt Builder → 动态构建系统提示词           │
│  3. Session History Loader → 加载对话历史                │
│  4. Context Window Guard → Token 窗口监控                │
│  5. ReAct Loop         → 推理 + 工具调用循环             │
│  6. Streaming Replies  → 流式输出 + 持久化               │
└─────────────────────────────────────────────────────────┘
  │
  ▼
输出：流式文本响应 + 工具执行记录
```

---

## 2. 六大子组件详解

### 2.1 Model Resolver — 多 LLM 提供商管理

Model Resolver 负责选择当前 LLM 提供商，并处理故障转移：

```
配置的 LLM 提供商列表
  │
  ▼
主提供商（如 claude-opus-4）可用？
  ├─ 是 → 使用主提供商
  └─ 否（限流/故障）
         │
         ▼
       冷却该 API Key（放入冷却池）
         │
         ▼
       切换到备用提供商（如 gpt-4o）
         │
         ▼
       主提供商恢复后自动重新启用
```

**支持的提供商：**

| 提供商 | 模型示例 | 特性 |
|--------|----------|------|
| Anthropic | claude-opus-4, claude-sonnet-4 | 最强推理，高成本 |
| OpenAI | gpt-4o, o3 | 工具调用成熟 |
| Google | gemini-2.5-pro | 超长上下文 |
| Ollama | qwen3:8b, llama3 | 本地免费，零延迟 |
| vLLM | 任意 HF 模型 | 自托管高吞吐 |
| DeepSeek | deepseek-r1 | 高性价比推理 |

---

### 2.2 System Prompt Builder — 动态提示词构建

系统提示词由 **4 个分层组件** 动态合并：

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: OpenClaw Base Prompt                            │
│  → 核心行为准则（始终遵守）                              │
│  → 工具使用格式规范                                      │
│  → 安全边界定义                                          │
├─────────────────────────────────────────────────────────┤
│ Layer 2: Skills Prompt（紧凑索引）                        │
│  → 当前可用 Skills 的名称 + 描述 + 路径列表              │
│  → 注意：不注入 SKILL.md 全文，仅注入索引！             │
├─────────────────────────────────────────────────────────┤
│ Layer 3: Bootstrap Context Files                         │
│  → workspace 级别的环境上下文                            │
│  → AGENT.md（Agent 身份/角色定义）                       │
│  → SOUL.md（个性/汇报链路定义）                          │
├─────────────────────────────────────────────────────────┤
│ Layer 4: Per-Run Overrides                               │
│  → 本次运行注入的额外指令                                │
│  → 可来自 Heartbeat 调度、外部 API 调用                  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
              合并为最终 System Prompt → 发送 LLM
```

**AGENT.md 示例：**

```markdown
# My Research Agent

## Identity
You are a research analyst specializing in AI industry trends.

## Responsibilities
- Monitor arXiv for new papers daily
- Synthesize findings into bilingual (EN/ZH) summaries
- Report to: Learning Coach Agent

## Tools Available
- web_fetch, web_search
- file_write (output to /workspace/reports/)

## Output Format
Always produce: Executive Summary → Key Findings → Raw Notes
```

---

### 2.3 Session History Loader — 上下文历史加载

```
JSONL Transcript（磁盘）
       │
       ▼
按 Session ID 过滤条目
       │
       ▼
反序列化为 Message[] 数组
       │
       ├─ 全量加载（短对话）
       │
       └─ 压缩加载（长对话，超过阈值）
              │
              ▼
            摘要压缩（LLM 自动总结旧轮次）
              │
              ▼
            保留最近 N 轮原始记录
```

**JSONL 条目格式：**
```jsonl
{"role":"user","content":"帮我分析一下这份报告","ts":1742000000}
{"role":"assistant","content":"我来读取文件...","ts":1742000001}
{"role":"tool","name":"file_read","result":"...文件内容...","ts":1742000002}
{"role":"assistant","content":"分析完毕，结论如下：...","ts":1742000003}
```

---

### 2.4 Context Window Guard — Token 窗口保护

```
当前 Token 计数监控
       │
       ▼
Token 数 < 警戒线（如 80%）？
  ├─ 是 → 正常执行
  └─ 否
         │
         ├─ 触发 历史摘要压缩（自动 summarize 旧轮次）
         │
         ├─ 释放 compaction reserve（为模型回复预留的 Token 缓冲区）
         │
         └─ 极端情况：终止当前 Loop，提示用户重置
```

**Token 预算配置：**

```yaml
context_window:
  max_tokens: 200000          # 模型最大上下文
  compaction_reserve: 4096    # 为回复预留的 Token
  history_compression_threshold: 0.75  # 超过 75% 触发压缩
  summarization_model: claude-haiku-4-5  # 用廉价模型做摘要
```

---

### 2.5 ReAct Loop — 核心推理循环

ReAct = **Re**asoning + **Act**ing，是 Agent 区别于 Chatbot 的核心模式：

```
─────────────────────────────────────────────────────
                    ReAct 完整流程
─────────────────────────────────────────────────────

context = [system_prompt, history, user_message]

LOOP:
    ┌─────────────────────────────────┐
    │  REASON                         │
    │  LLM 生成下一步思考             │
    │  (支持 <thinking> 内部推理)     │
    └─────────────┬───────────────────┘
                  │
         ┌────────┴────────┐
         │                 │
         ▼                 ▼
    纯文本回复          工具调用请求
         │            { tool: "web_fetch",
         │              params: { url: "..." } }
         │                 │
         │                 ▼
         │           ACT: 执行工具
         │                 │
         │                 ▼
         │           OBSERVE: 获取结果
         │                 │
         │                 ▼
         │           结果注入 context
         │                 │
         │                 └──► 继续 LOOP
         │
         ▼
    流式输出文本
    写入 JSONL
    返回 Gateway
    结束 LOOP
```

**伪代码实现：**

```typescript
async function reactLoop(context: Context): Promise<string> {
  while (true) {
    const response = await llm.call(context);

    // 流式输出中间结果
    stream.write(response.delta);

    if (response.type === "text") {
      // 纯文本终止
      await persist(context, response);
      return response.text;
    }

    if (response.type === "tool_call") {
      // 执行工具
      const result = await toolExecutor.run(
        response.tool_name,
        response.tool_params
      );
      // 将工具结果注入上下文
      context.addMessage({
        role: "tool",
        name: response.tool_name,
        content: result,
      });
      // 继续循环
    }
  }
}
```

---

### 2.6 内置工具集（Tool Executor）

| 工具类型 | 具体工具 | 描述 |
|----------|----------|------|
| **文件系统** | `file_read`, `file_write`, `file_list` | 本地文件操作 |
| **Shell** | `shell_exec` | 执行 Bash 命令（受沙箱限制）|
| **浏览器** | `browser_navigate`, `browser_click` | CDP 控制 Chrome |
| **网络** | `web_fetch`, `web_search` | HTTP 请求 + 搜索 |
| **Agent** | `sessions_spawn` | 创建子 Agent |
| **记忆** | `memory_read`, `memory_write` | Markdown 记忆操作 |

**Semantic Snapshot（浏览器优化）：**

```
传统方式：截图 → base64 → 传入视觉 LLM → 高 Token 成本
OpenClaw 方式：解析 Accessibility Tree → 结构化文本 → 传入 LLM

Token 成本节约：高达 90%
准确率：显著提升（结构化 > 像素识别）
```

---

## 3. 多 Agent 子进程编排

OpenClaw 支持主 Agent 孵化子 Agent（Subagent）：

```yaml
# 主 Agent 调用工具 sessions_spawn
sessions_spawn:
  label: "research-task"
  model: "ollama/qwen3:8b"     # 用本地廉价模型执行
  task: "Research top 5 Rust web frameworks and summarize"
  runTimeoutSeconds: 300
```

**混合云/本地编排策略：**

```
主 Agent（Claude Opus 4，云端）
  → 决策、推理、用户交互
  → 成本：~$15/M input tokens

子 Agent × N（Ollama/本地模型）
  → 执行型任务：搜索、汇总、文件处理
  → 成本：$0（仅电费）

规则：任务执行 > 30s → 委托给子 Agent
结果：push-based 回传，无需轮询
```

**并发上限（Apple M3 Pro 36GB 示例）：**
```
OLLAMA_MAX_LOADED_MODELS=3
可并行子 Agent 数：2-3 个
```

---

## 4. 流式输出机制

```
LLM 生成 Token
    │
    ▼ (Server-Sent Events / WebSocket 流)
Gateway 接收流
    │
    ▼
实时转发到目标渠道（WhatsApp/Telegram/...）
    │
    ├─ 渠道支持流式 → 逐 Token 输出
    └─ 渠道不支持流式 → 缓冲后一次发送

用户可实时看到：
  ✓ 工具被调用的通知
  ✓ 工具执行结果
  ✓ 模型在工具结果上的推理过程
  ✓ 最终回复文本
```

---

## 5. 关键设计决策

| 决策 | 原因 |
|------|------|
| 提示词分层组装 | 可维护、可版本控制、可独立替换每一层 |
| Skills 仅注入索引 | 控制 Token 消耗，按需懒加载全文 |
| Context Window Guard | 防止 Token 爆炸导致模型行为不可预测 |
| 工具调用串行执行 | 与 Lane Queue 配合，防止状态竞争 |
| Semantic Snapshot | 90% Token 节约，比视觉截图更准确 |
| 子 Agent 委托 | 前沿模型做决策，本地模型做执行，成本最优 |
