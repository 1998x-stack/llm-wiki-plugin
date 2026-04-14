# FilesystemMiddleware：文件系统中间件

## 源码位置

- **主实现**：`libs/deepagents/deepagents/middleware/filesystem.py`
- **依赖协议**：`deepagents.backends.protocol`（`BackendProtocol`、`SandboxBackendProtocol` 等）
- **主图挂载**：`libs/deepagents/deepagents/graph.py` 中的 `create_deep_agent`

---

## 1. 职责概览

`FilesystemMiddleware` 为 Agent 提供一组文件与（可选）沙箱执行相关的工具，并在**每次模型调用前**通过 `wrap_model_call()`：

- 按当前解析的 backend **决定是否暴露 `execute`**（不支持则从本次请求的工具列表中过滤掉）；
- **注入**文件操作与（若适用）执行相关的系统提示；
- 对超大 **HumanMessage** 与 **ToolMessage** 做**卸载（eviction）**：将内容写入 backend，替换为短引用，缓解上下文窗口压力。

类文档字符串中的核心描述：

```519:531:libs/deepagents/deepagents/middleware/filesystem.py
class FilesystemMiddleware(AgentMiddleware[FilesystemState, ContextT, ResponseT]):
    """Middleware for providing filesystem and optional execution tools to an agent.

    This middleware adds filesystem tools to the agent: `ls`, `read_file`, `write_file`,
    `edit_file`, `glob`, and `grep`.

    Files can be stored using any backend that implements the `BackendProtocol`.

    If the backend implements `SandboxBackendProtocol`, an `execute` tool is also added
    for running shell commands.

    This middleware also automatically evicts large tool results to the file system when
    they exceed a token threshold, preventing context window saturation.
```

---

## 2. 提供的工具

| 工具名 | 作用 |
|--------|------|
| `ls` | 列出目录 |
| `read_file` | 按行分页读取文件 |
| `write_file` | 写入文件 |
| `edit_file` | 字符串查找替换编辑 |
| `glob` | 按模式匹配路径 |
| `grep` | 在目录/文件中搜索 |
| `execute` | **仅当** backend 满足 `SandboxBackendProtocol` 时，在本次 LLM 请求中保留；否则在 `wrap_model_call` 中从 `request.tools` 移除 |

`execute` 在工厂阶段仍会创建，但实际是否进入模型可见工具集由运行时 backend 能力决定（见 `wrap_model_call` 中对 `execute` 的过滤逻辑）。

---

## 3. 状态与 `_file_data_reducer`

文件内容在 Agent 状态中通过 `FilesystemState` 持有，字段 `files` 使用自定义 reducer 合并更新，并支持**删除语义**（右侧字典中值为 `None` 表示删除该路径）：

```79:112:libs/deepagents/deepagents/middleware/filesystem.py
def _file_data_reducer(left: dict[str, FileData] | None, right: dict[str, FileData | None]) -> dict[str, FileData]:
    """Merge file updates with support for deletions.

    This reducer enables file deletion by treating `None` values in the right
    dictionary as deletion markers. It's designed to work with LangGraph's
    state management where annotated reducers control how state updates merge.
    ...
    """
    if left is None:
        return {k: v for k, v in right.items() if v is not None}

    result = {**left}
    for key, value in right.items():
        if value is None:
            result.pop(key, None)
        else:
            result[key] = value
    return result
```

**设计取舍**：与 LangGraph 的 reducer 模型对齐，使「增量写文件」与「显式删除」可以用同一套 `files` 更新协议表达。

---

## 4. 大文件与读取限制相关常量

源码中与本章分析直接相关的常量（节选）：

```58:76:libs/deepagents/deepagents/middleware/filesystem.py
EMPTY_CONTENT_WARNING = "System reminder: File exists but has empty contents"
GLOB_TIMEOUT = 20.0  # seconds
LINE_NUMBER_WIDTH = 6
DEFAULT_READ_OFFSET = 0
DEFAULT_READ_LIMIT = 100
# Template for truncation message in read_file
# {file_path} will be filled in at runtime
READ_FILE_TRUNCATION_MSG = (
    "\n\n[Output was truncated due to size limits. "
    "The file content is very large. "
    "Consider reformatting the file to make it easier to navigate. "
    "For example, if this is JSON, use execute(command='jq . {file_path}') to pretty-print it with line breaks. "
    "For other formats, you can use appropriate formatting tools to split long lines.]"
)

# Approximate number of characters per token for truncation calculations.
# Using 4 chars per token as a conservative approximation (actual ratio varies by content)
# This errs on the high side to avoid premature eviction of content that might fit
NUM_CHARS_PER_TOKEN = 4
```

| 常量 | 含义 |
|------|------|
| `DEFAULT_READ_LIMIT` | 默认最多读取 **100** 行（可分页） |
| `NUM_CHARS_PER_TOKEN` | 按 **每 token 约 4 字符** 估算长度，用于截断与卸载阈值计算（偏保守，减少误伤） |
| `READ_FILE_TRUNCATION_MSG` | 超长输出时追加的说明模板，`{file_path}` 运行时填充 |
| `GLOB_TIMEOUT` | `glob` 操作超时 **20** 秒 |
| `LINE_NUMBER_WIDTH` | 带行号输出时行号列宽 **6** |
| `EMPTY_CONTENT_WARNING` | 文件存在但内容为空的系统提醒文案 |

`read_file` 内部会结合行数上限与基于 `NUM_CHARS_PER_TOKEN` 的字符上限做截断，避免单次工具返回撑爆上下文。

---

## 5. 工具结果卸载（eviction）与默认阈值

构造参数（节选）：

```572:612:libs/deepagents/deepagents/middleware/filesystem.py
    def __init__(
        self,
        *,
        backend: BACKEND_TYPES | None = None,
        system_prompt: str | None = None,
        custom_tool_descriptions: dict[str, str] | None = None,
        tool_token_limit_before_evict: int | None = 20000,
        human_message_token_limit_before_evict: int | None = 50000,
        max_execute_timeout: int = 3600,
    ) -> None:
```

- **`tool_token_limit_before_evict`**（默认 20000）：工具返回内容超过估算 token 阈值时，写入 backend，消息体替换为简短描述与路径引用。
- **`human_message_token_limit_before_evict`**（默认 50000）：对用户 HumanMessage 的类似卸载，避免单条用户输入占满窗口。

部分工具名会排除在卸载逻辑之外（常量 `TOOLS_EXCLUDED_FROM_EVICTION`），避免破坏必须内联展示的结果。

**设计意图**：在「仍把引用留在对话里」的前提下，把大块 payload 迁到 backend，由 `read_file` 等工具按需拉回，从架构上把**存储**与**对话 token**解耦。

---

## 6. 系统提示与 `execute`

中间件会注入文件操作指引；若 backend 支持执行且本次请求保留 `execute`，会追加执行工具说明（`EXECUTION_SYSTEM_PROMPT` 等）。工具描述中亦明确 `execute` 与 `SandboxBackendProtocol` 的关系，避免模型在不可用环境下盲目调用。

---

## 7. 与其他模块的关系

- **`deepagents.backends`**：`BackendProtocol` 定义读写列表等能力；`SandboxBackendProtocol` 扩展执行能力。
- **`create_deep_agent`**：默认将 `FilesystemMiddleware(backend=...)` 放入主 Agent 的中间件栈；子代理在 `graph.py` 中也会挂载同名中间件以继承文件能力。
- **`deepagents.backends.utils`**：路径校验、行号格式化、grep 结果格式化、`truncate_if_too_long` 等工具函数供本中间件复用。

---

## 8. 小结

- **工具面**：六大文件工具 + 条件性 `execute`。
- **管线面**：`wrap_model_call` 统一处理工具过滤、提示注入、消息/结果卸载。
- **状态面**：`files` + `_file_data_reducer` 支持合并与删除。
- **常量面**：分页读取、字符/token 估算、glob 超时、空文件提醒等共同构成「大仓库/大文件」场景下的可操作性与安全边界。
