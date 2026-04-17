---
type: concept
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 4
tags: [AI, Agent, 架构, 协议, 沙箱, Agent系统]
aliases: [BackendProtocol, SandboxBackendProtocol, DeepAgents backend]
relates_to:
  - target: "[[DeepAgents]]"
    type: part_of
    confidence: 0.95
  - target: "[[Agent Harness模式]]"
    type: implements
    confidence: 0.9
  - target: "[[DeepAgents中间件体系]]"
    type: related_to
    note: FilesystemMiddleware 依赖 BackendProtocol
    confidence: 0.9
supersedes: null
---

# DeepAgents 后端协议

## 概述

[[DeepAgents]] 的存储与执行抽象层（`libs/deepagents/deepagents/backends/`）。`BackendProtocol` 定义统一的文件类 API，`SandboxBackendProtocol` 在其上扩展 shell 执行能力。上层[[ROS (Robot Operating System)|中间件]]和工具只依赖协议接口，不感知底层是内存状态、本地磁盘还是远程沙箱——实现 [[Agent Harness模式]] 中"后端换皮、工具不变"的设计原则。

## 关键内容

### BackendProtocol（文件类 API）

| 方法 | 职责 |
|------|------|
| `ls(path)` | 列目录，返回 `LsResult` |
| `read(path, offset=0, limit=2000)` | 分页读取，返回 `ReadResult` |
| `write(path, content)` | 新建文件（已存在则失败），返回 `WriteResult` |
| `edit(path, old, new, replace_all=False)` | 精确字符串替换，返回 `EditResult` |
| `grep(pattern, path=None, glob=None)` | 字面量子串搜索（非正则），返回 `GrepResult` |
| `glob(pattern, path="/")` | 路径 glob，返回 `GlobResult` |
| `upload_files(files)` | 批量上传，支持部分成功 |
| `download_files(paths)` | 批量下载，支持部分成功 |

每个同步方法均有 `a*` 异步变体（默认 `asyncio.to_thread` 包装，子类可覆盖）。

### SandboxBackendProtocol（执行扩展）

```python
class SandboxBackendProtocol(BackendProtocol):
    @property
    def id(self) -> str: ...          # 实例稳定标识
    def execute(command, timeout=None) -> ExecuteResponse: ...
    async def aexecute(...): ...
```

仅当 backend 实现此协议，`execute` 工具才对 Agent 可见（FilesystemMiddleware 在运行时动态检查）。`ExecuteResponse` 含 `output`（stdout+stderr 合并）、`exit_code`、`truncated`。

### 内置后端实现

| 实现 | 特点 |
|------|------|
| **StateBackend** | 文件内容存于 LangGraph 状态通道（ephemeral，线程内持久，无磁盘暴露）。`create_deep_agent` 的默认后端 |
| **FilesystemBackend** | 读写真实文件系统，支持 `virtual_mode` 等安全语义 |
| **CompositeBackend** | 按路径前缀路由到不同后端（如 `/memories/` → 持久存储后端） |
| **BaseSandbox** | 实现 `SandboxBackendProtocol`，接入具体沙箱；合作方包（libs/partners）在此扩展 |
| **LangSmithSandbox** | 专用于 LangSmith 评估环境 |

### 合作方沙箱（libs/partners/）

各自独立发版：`Daytona`、`Modal`、`QuickJS`、`Runloop`，均通过替换 Backend 层扩展执行环境，不改变上层工具语义。

### 关键数据类型

- **`FileData`（TypedDict）**：`content: str`（UTF-8 或 base64）、`encoding`、`created_at`/`modified_at`
- **`FileFormat`**：`"v1"`（旧，content 为 `list[str]` 按行分割）、`"v2"`（当前，content 为单 str + encoding）
- **`FileOperationError`**：规范化错误码 `file_not_found`/`permission_denied`/`is_directory`/`invalid_path`，便于 LLM 理解并重试
- **`BackendFactory`**：`Callable[[ToolRuntime], BackendProtocol]`，支持惰性构造后端

### 设计决策

1. **统一表面、多样实现**：中间件不感知磁盘与远程差异
2. **同步优先 + 默认线程卸载**：降低实现门槛
3. **批量与部分成功**：上传/下载返回列表，逐项含 `error` 字段
4. **执行能力分层**：文件协议与 shell 协议分离，非沙箱环境不误暴露执行面
5. **版本化文件载荷**：`FileFormat` v1/v2 明确，降低状态迁移成本

## 来源
- [[raw/books/deepagents-book-main/02-核心设计哲学与架构总览.md]]
- [[raw/books/deepagents-book-main/04-后端协议-BackendProtocol.md]]
- [[raw/books/deepagents-book-main/05-后端实现详解.md]]
- [[raw/books/deepagents-book-main/27-合作伙伴沙箱集成.md]]

## 相关
- [[DeepAgents]]
- [[Agent Harness模式]]
- [[DeepAgents中间件体系]]
