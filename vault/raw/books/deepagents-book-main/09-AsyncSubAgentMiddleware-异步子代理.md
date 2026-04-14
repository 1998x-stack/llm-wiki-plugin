# AsyncSubAgentMiddleware：异步子代理（远程）

## 源码位置

- **主实现**：`libs/deepagents/deepagents/middleware/async_subagents.py`
- **主图挂载**：`libs/deepagents/deepagents/graph.py`（当 `subagents` 中含 `graph_id` 的规格时归入异步列表并追加本中间件）

---

## 1. 设计背景

异步子代理通过 **LangGraph SDK** 与符合 **[Agent Protocol](https://github.com/langchain-ai/agent-protocol)** 的远端服务交互：主代理**启动任务后立即拿到 task id**，不必阻塞等待子图跑完；后续通过轮询、发消息、取消等工具与远端 run/thread 同步。

模块头部说明：

```1:10:libs/deepagents/deepagents/middleware/async_subagents.py
"""Middleware for async subagents running on remote Agent Protocol servers.

Async subagents use the LangGraph SDK to launch background runs on remote
[Agent Protocol](https://github.com/langchain-ai/agent-protocol) servers.
Unlike synchronous subagents (which block until completion), async subagents
return a task ID immediately, allowing the main agent to monitor progress and
send updates while the subagent works.

Compatible with LangGraph Platform (managed) and self-hosted servers.
"""
```

`create_deep_agent` 中的注释亦指出：当前路径支持通过 **LangSmith 部署**等方式托管的远端 Agent。

---

## 2. `AsyncSubAgent` 规格

```34:68:libs/deepagents/deepagents/middleware/async_subagents.py
class AsyncSubAgent(TypedDict):
    """Specification for an async subagent running on an remote Agent Protocol server.
    ...
    """

    name: str
    """Unique identifier for the async subagent."""

    description: str
    """What this subagent does.

    The main agent uses this to decide when to delegate.
    """

    graph_id: str
    """The graph name or assistant ID on the remote server."""

    url: NotRequired[str]
    """URL of the Agent Protocol server.

    Defaults to the LangGraph SDK's default endpoint. Omit to use ASGI
    transport for local servers.
    """

    headers: NotRequired[dict[str, str]]
    """Additional headers to include in requests to the remote server."""
```

- **`graph_id`**：远端上的图名或 assistant id（必填）。
- **`url` / `headers`**：自选；认证可通过环境变量（如 `LANGGRAPH_API_KEY` 等，见类文档）或自定义头。

---

## 3. `AsyncSubAgentMiddleware` 与生命周期工具

中间件构建五类工具（内部名如下），覆盖异步任务全生命周期：

| 工具名 | 作用 |
|--------|------|
| `start_async_task` | 创建 thread + run，**立即**返回 `task_id`（此处等于远端 `thread_id`），并在状态中记录 `AsyncTask` |
| `check_async_task` | 按 `task_id` 查询 run 状态；成功时拉取 thread values 取最后一条消息作为 `result` |
| `update_async_task` | 在同一 thread 上新建 run，带上后续用户消息；`multitask_strategy="interrupt"` 打断当前 run |
| `cancel_async_task` | 取消指定 run |
| `list_async_tasks` | 列出已跟踪任务；对非终态任务会尝试拉取**实时**状态更新缓存 |

工具列表由 `_build_async_subagent_tools` 组装：

```837:859:libs/deepagents/deepagents/middleware/async_subagents.py
def _build_async_subagent_tools(
    agents: list[AsyncSubAgent],
) -> list[StructuredTool]:
    """Build the async subagent tools from agent specs.
    ...
    """
    agent_map: dict[str, AsyncSubAgent] = {a["name"]: a for a in agents}
    clients = _ClientCache(agent_map)
    agents_desc = "\n".join(f"- {a['name']}: {a['description']}" for a in agents)
    launch_desc = ASYNC_TASK_TOOL_DESCRIPTION.format(available_agents=agents_desc)

    return [
        _build_start_tool(agent_map, clients, launch_desc),
        _build_check_tool(clients),
        _build_update_tool(agent_map, clients),
        _build_cancel_tool(clients),
        _build_list_tasks_tool(clients),
    ]
```

---

## 4. 状态：`async_tasks` 与 reducer

```113:126:libs/deepagents/deepagents/middleware/async_subagents.py
def _tasks_reducer(
    existing: dict[str, AsyncTask] | None,
    update: dict[str, AsyncTask],
) -> dict[str, AsyncTask]:
    """Merge task updates into the existing tasks dict."""
    merged = dict(existing or {})
    merged.update(update)
    return merged


class AsyncSubAgentState(AgentState):
    """State extension for async subagent task tracking."""

    async_tasks: Annotated[NotRequired[dict[str, AsyncTask]], _tasks_reducer]
```

`AsyncSubAgentMiddleware.state_schema = AsyncSubAgentState`，使 task id 与元数据在**多轮对话与上下文压缩**后仍可被工具查找（类文档明确提到 survive context compaction）。

---

## 5. 系统提示与使用约束

默认 `ASYNC_TASK_SYSTEM_PROMPT` 强调：

- 启动后**立刻把 task_id 给用户**，**不要**自动连续轮询；
- 仅在用户要状态/结果时调用 `check_async_task`，且**禁止循环 poll**；
- 历史里的状态可能已过期，需用工具取**当前**状态；
- **完整展示 task_id**，不要截断。

`wrap_model_call()` 将上述说明与「可用异步子代理类型」列表追加到主系统消息，与同步 `SubAgentMiddleware` 模式一致。

---

## 6. 客户端与认证

`_ClientCache` 按 `(url, headers)` 缓存 sync/async 的 LangGraph 客户端。`_resolve_headers` 默认在未指定时加入 `x-auth-scheme: langsmith`，便于托管平台场景。

**注意**：同步路径 `get_sync` 在 `url is None` 时会报错，提示 ASGI 传输需要异步调用 —— 集成时需按运行环境选择 sync/async 工具实现（本模块已为各工具提供 `func` 与 `coroutine`）。

---

## 7. 与同步子代理、主图的关系

```371:374:libs/deepagents/deepagents/graph.py
    if async_subagents:
        # Async here means that we run these subagents in a non-blocking manner.
        # Currently this supports agents deployed via LangSmith deployments.
        deepagent_middleware.append(AsyncSubAgentMiddleware(async_subagents=async_subagents))
```

- **同步子代理**：`SubAgent` / `CompiledSubAgent` → `task` 工具，阻塞直到子 Runnable 完成。
- **异步子代理**：带 `graph_id` 的 spec → `AsyncSubAgentMiddleware`，**非阻塞**，适合长任务与远端专用部署。

---

## 8. 典型使用场景小结

- 长耗时分析、批处理、流水线任务，避免占满主 Agent 的 turn。
- 子能力运行在 **LangGraph Platform / 自托管 Agent Protocol** 上，与主应用解耦。
- 需要**并行**启动多个远端任务，稍后统一 `list_async_task` / `check_async_task` 收结果。

---

## 9. 小结

- **规格**：`AsyncSubAgent` 以 `name`、`description`、`graph_id` 为核心，可选 `url`/`headers`。
- **中间件**：注册五个生命周期工具 + 系统提示，状态字段 `async_tasks` 持久化任务表。
- **集成模型**：LangGraph SDK + Agent Protocol；与同步 `task` 子代理互补，面向远端与非阻塞编排。
