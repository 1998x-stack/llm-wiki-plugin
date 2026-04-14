# PatchToolCallsMiddleware：悬空工具调用修复

**源码路径：** `libs/deepagents/deepagents/middleware/patch_tool_calls.py`

---

## 1. 问题背景

在多轮对话与工具调用流程中，可能出现：

- `AIMessage` 带有 `tool_calls`，但后续**没有**匹配的 `ToolMessage`（例如执行被中断、用户插入新消息、图执行路径异常等）。

多数聊天模型协议要求 **每个 tool_call 都有对应 tool 结果消息**；缺失时易导致后续轮次行为异常或模型困惑。

---

## 2. 中间件职责

**类名：** `PatchToolCallsMiddleware(AgentMiddleware)`

在 **`before_agent`** 钩子中扫描整条 `state["messages"]`，对每一个「有 `tool_calls` 却无对应 `ToolMessage`」的调用，**追加一条合成的 `ToolMessage`**，说明该调用已被取消。

---

## 3. 实现要点

- **遍历方式：** 对索引 `i` 处的每条消息先原样加入 `patched_messages`；若为 `AIMessage` 且含 `tool_calls`，则对每个 `tool_call` 在 **`messages[i:]`** 子序列中查找 `type == "tool"` 且 `tool_call_id` 匹配的回复。
- **未找到时：** 构造 `ToolMessage`，`content` 为固定英文说明（见下节），`name` 与 `tool_call_id` 与原始调用一致。
- **状态写回：** 返回 `{"messages": Overwrite(patched_messages)}`，使用 LangGraph 的 **`Overwrite`** 整体替换消息列表，确保补丁后的列表成为唯一真源。

该实现**代码量小**（约四十余行），但对保证 **tool 调用闭环** 很关键。

---

## 4. 完整源码引用

```1:45:libs/deepagents/deepagents/middleware/patch_tool_calls.py
"""Middleware to patch dangling tool calls in the messages history."""

from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Overwrite


class PatchToolCallsMiddleware(AgentMiddleware):
    """Middleware to patch dangling tool calls in the messages history."""

    def before_agent(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:  # noqa: ARG002
        """Before the agent runs, handle dangling tool calls from any AIMessage."""
        messages = state["messages"]
        if not messages or len(messages) == 0:
            return None

        patched_messages = []
        # Iterate over the messages and add any dangling tool calls
        for i, msg in enumerate(messages):
            patched_messages.append(msg)
            if isinstance(msg, AIMessage) and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    corresponding_tool_msg = next(
                        (msg for msg in messages[i:] if msg.type == "tool" and msg.tool_call_id == tool_call["id"]),  # ty: ignore[unresolved-attribute]
                        None,
                    )
                    if corresponding_tool_msg is None:
                        # We have a dangling tool call which needs a ToolMessage
                        tool_msg = (
                            f"Tool call {tool_call['name']} with id {tool_call['id']} was "
                            "cancelled - another message came in before it could be completed."
                        )
                        patched_messages.append(
                            ToolMessage(
                                content=tool_msg,
                                name=tool_call["name"],
                                tool_call_id=tool_call["id"],
                            )
                        )

        return {"messages": Overwrite(patched_messages)}
```

---

## 5. 设计决策说明

1. **合成消息语义：** 明确告知「被取消」而非伪造成功/失败工具输出，避免模型误以为工具已执行。
2. **插入位置：** 补丁紧跟在对应 `AIMessage` 之后（在 `patched_messages` 中的顺序），符合「先调用、后结果」的自然阅读顺序。
3. **全量 `Overwrite`：** 避免与 reducer 增量合并产生重复或顺序错乱；列表由中间件一次性重建。
4. **空消息短路：** 无消息时返回 `None`，不触发无意义更新。

---

## 6. 与其他模块的关系

- 依赖 **LangChain** 的 `AgentMiddleware`、`AgentState`、`AIMessage`、`ToolMessage`。
- 依赖 **LangGraph** 的 `Runtime`（本实现未使用 `runtime` 参数，保留签名以符合钩子约定）与 `Overwrite`。

通常与负责工具执行、人机协作、或可能中断工具链路的中间件/节点配合使用，作为 **图运行前的卫生检查（sanitizer）**。
