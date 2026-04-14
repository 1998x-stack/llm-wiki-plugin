# SummarizationMiddleware：上下文压缩与对话卸载

**源码路径：** `libs/deepagents/deepagents/middleware/summarization.py`

---

## 1. 模块定位

本模块为 Deep Agents 提供**对话摘要与上下文压缩**能力：在 token 用量逼近上限时自动压缩历史，或将完整历史卸载到后端存储；同时可选暴露 `compact_conversation` 工具，供智能体或人在回路按需触发压缩。实现上在 **LangChain** 的 `SummarizationMiddleware`（`LCSummarizationMiddleware`）之上扩展了 **后端卸载**、**与工具层协同** 等逻辑。

---

## 2. 两个中间件类

### 2.1 `SummarizationMiddleware`（内部类 `_DeepAgentsSummarizationMiddleware`）

- **作用：** 在 `wrap_model_call` / `awrap_model_call` 中，于调用主模型前检查是否应摘要；若应摘要，则先卸载旧消息、再调用 LLM 生成摘要，并用 `ExtendedModelResponse` + `Command` 更新私有状态 `_summarization_event`。
- **公开名：** `SummarizationMiddleware = _DeepAgentsSummarizationMiddleware`，外部应导入 `SummarizationMiddleware`。

### 2.2 `SummarizationToolMiddleware`

- **作用：** 注册 `compact_conversation` 工具；**不会自动压缩**，仅在工具被调用时执行压缩。
- **组合关系：** 构造函数接收一个 `SummarizationMiddleware` 实例，复用其模型、后端、阈值与摘要引擎。
- **与自动摘要共享状态：** 工具路径与自动摘要均写入同一 `_summarization_event`，二者可正确衔接。
- **资格门槛：** `_is_eligible_for_compaction` 要求对话用量达到**自动摘要触发阈值的大约 50%** 才允许手动压缩，避免过早清空上下文。

---

## 3. 工厂函数

| 函数 | 说明 |
|------|------|
| `create_summarization_middleware(model, backend)` | `model` **必须是**已解析的 `BaseChatModel`；根据 `compute_summarization_defaults(model)` 设置 `trigger`、`keep`、`truncate_args_settings` 等。 |
| `create_summarization_tool_middleware(model, backend)` | `model` 可为字符串或 `BaseChatModel`；字符串会先经 `deepagents._models.resolve_model` 解析，再创建 `SummarizationMiddleware` 并包一层 `SummarizationToolMiddleware`。 |

---

## 4. 触发与保留：`trigger` / `keep`

当模型 **profile** 中存在 `max_input_tokens` 时，`compute_summarization_defaults` 采用**比例**策略（与文档示例一致）：

- **`trigger=("fraction", 0.85)`**：用量达到上下文窗口约 **85%** 时触发摘要。
- **`keep=("fraction", 0.10)`**：压缩后保留约窗口 **10%** 对应的近期消息（具体切分由 LangChain 侧 `_determine_cutoff_index` 等逻辑完成）。

若无可靠 profile，则回退为更保守的 **token / 条数** 默认值（例如 `trigger=("tokens", 170000)`、`keep=("messages", 6)`），避免误判上下文上限。

---

## 5. 处理流程概要

1. **重建有效消息列表：** 若状态中已有 `_summarization_event`，通过 `_apply_event_to_messages` 得到「摘要 HumanMessage + 截断点之后的消息」。
2. **（可选）工具参数截断：** `TruncateArgsSettings` 可在完整摘要前，对较早 `AIMessage` 中 `write_file` / `edit_file` 等大参数做裁剪，降低 token。
3. **判断是否摘要：** 委托内部 `_lc_helper`（LangChain）的 `_should_summarize`；token 计数默认使用 `count_tokens_approximately`。
4. **卸载历史：** 将待摘要段通过 `_offload_to_backend` 写入后端；路径默认为 `{history_path_prefix}/{thread_id}.md`，默认前缀 `/conversation_history`。
5. **生成摘要：** `_create_summary` / `_acreate_summary` 调用 LangChain 侧逻辑。
6. **更新请求与状态：** 用 `_build_new_messages_with_path` 构造带路径说明的 `HumanMessage`（`additional_kwargs` 中 `lc_source="summarization"`），与保留段拼接后调用 `handler`；并通过 `Command(update={"_summarization_event": new_event})` 写入事件。

**设计要点：** 与旧版「直接改 LangGraph messages 状态」不同，当前实现主要在 **middleware 状态** 中记录 `_summarization_event`，在每次模型请求时重算**有效**消息列表，从而与 LangGraph 状态模型对齐。

---

## 6. 后端文件：运行日志式追加

- 每个线程对应一个文件：`/conversation_history/{thread_id}.md`（`thread_id` 来自 `get_config()["configurable"]["thread_id"]`，缺失时生成 `session_xxxxxxxx`）。
- 每次摘要事件追加一节：`## Summarized at {ISO8601 UTC}\n\n` + `get_buffer_string(filtered_messages)`。
- 链式摘要时，会过滤掉此前摘要产生的 `HumanMessage`（`lc_source == "summarization"`），避免重复卸载同一段摘要文本。
- 读写使用 `download_files` / `adownload_files` 取**原始**内容，再 `write` / `edit` 或 `awrite` / `aedit` 追加（因 `read` 可能返回带行号等面向 LLM 的格式）。

---

## 7. `ContextOverflowError` 处理

在 **未** 达到预设摘要阈值时，中间件仍会先尝试用当前（可能已截断参数的）消息调用模型。若调用抛出 `ContextOverflowError`，则**捕获后转入摘要路径**，用「摘要 + 保留近期消息」重试。这样在计数略滞后或边界情况下仍能恢复。

---

## 8. Token 计数与 LangChain 基类

- 默认 `token_counter=count_tokens_approximately`（`langchain_core.messages.utils`）。
- 核心摘要阈值、切分、摘要生成等委托给：

```python
from langchain.agents.middleware.summarization import (
    SummarizationMiddleware as LCSummarizationMiddleware,
    # ...
)
```

---

## 9. 系统提示注入（工具中间件）

`SummarizationToolMiddleware.wrap_model_call` / `awrap_model_call` 通过 `append_to_system_message` 追加 `SUMMARIZATION_SYSTEM_PROMPT`，告知模型可使用 `compact_conversation` 及适用场景（新任务、已完成提炼等）。**仅改提示，不自动执行工具。**

---

## 10. 与其他模块的关系

- **`deepagents._models.resolve_model`**：`create_summarization_tool_middleware` 在传入字符串模型时使用。
- **`deepagents.middleware._utils.append_to_system_message`**：拼接系统提示。
- **`deepagents.backends.protocol`**：`backend` 可为实例或可调用工厂，与 `ToolRuntime` / `Runtime` 解析一致。
- **`langgraph.types.Command` / `ExtendedModelResponse`**：在模型调用包装层回写 `_summarization_event`。

---

## 11. 小结

| 维度 | 内容 |
|------|------|
| 自动压缩 | `SummarizationMiddleware`，比例触发 85% / 保留 10%（有 profile 时） |
| 按需压缩 | `SummarizationToolMiddleware` → `compact_conversation` |
| 历史持久化 | 后端 Markdown 按线程追加节 |
| 健壮性 | `ContextOverflowError` 回退摘要；可选大工具参数预截断 |
| 基座 | LangChain `SummarizationMiddleware` + Deep Agents 后端与状态扩展 |
