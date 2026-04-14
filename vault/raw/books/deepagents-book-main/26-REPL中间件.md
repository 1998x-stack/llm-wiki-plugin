# REPL 中间件（langchain-repl）

## 文档来源与路径

| 类型 | 路径 |
|------|------|
| 包根目录 | `libs/repl/` |
| Python 包源码 | `libs/repl/langchain_repl/` |
| 测试 | `libs/repl/tests/`（含 `unit_tests/` 等） |
| 构建与依赖声明 | `libs/repl/pyproject.toml`、`libs/repl/uv.lock` |

---

## 概述

`libs/repl/` 提供 **`langchain-repl`** 包，为智能体运行时增加 **REPL 风格的可执行环境**：模型生成的代码可在受控解释器中执行，并通过中间件挂入 LangGraph / Deep Agents 的请求链路。

**典型用途**：在智能体会话中需要 **交互式执行代码**（验证片段、数据处理、快速试探 API 行为）时，由 `ReplMiddleware` 注入能力，由 `Interpreter` 负责实际执行语义。

---

## 包与对外 API

- **发行包名**：`langchain-repl`（见 `libs/repl/pyproject.toml`）。
- **公开导出**（`langchain_repl/__init__.py`）：
  - `Interpreter`：在 REPL 式环境中执行代码。
  - `ReplMiddleware`：将 REPL 能力以中间件形式接入智能体。
  - `__version__`：包版本字符串。

```text
langchain_repl/
├── __init__.py      # 导出 Interpreter, ReplMiddleware, __version__
├── interpreter.py   # 解释器实现
├── middleware.py    # ReplMiddleware
└── _foreign_function_docs.py  # 与外部函数/工具文档相关的辅助
```

---

## 核心概念

### Interpreter

- **职责**：在 **交互式、类 REPL** 的语义下执行代码（具体隔离级别与语言运行时由实现决定）。
- **关系**：被中间件或上层编排调用，是「执行」一层的核心抽象。

### ReplMiddleware

- **职责**：作为 **中间件**，把 REPL / 解释器能力接到智能体管道中（与消息、工具调用、系统提示等协同）。
- **关系**：依赖 `Interpreter` 的行为；测试中存在端到端用例（如 `tests/unit_tests/test_end_to_end.py`、`test_end_to_end_async.py`）以及系统提示快照测试，验证与无工具/混合外部函数等场景下的提示词与行为。

---

## 设计取舍

- **中间件而非单一工具**：REPL 能力以 **Middleware** 形式出现，便于与现有 Deep Agents / LangGraph 中间件链组合，而不是零散工具函数堆砌。
- **测试分层**：`unit_tests` 覆盖解释器、系统提示、外部函数文档等；`smoke_tests` 含快照，防止提示词或行为静默漂移。

---

## 测试布局

| 区域 | 说明 |
|------|------|
| `libs/repl/tests/unit_tests/test_interpreter.py` | 解释器行为。 |
| `libs/repl/tests/unit_tests/test_end_to_end.py`、`test_end_to_end_async.py` | 与智能体链路的端到端行为。 |
| `libs/repl/tests/unit_tests/smoke_tests/` | 系统提示等快照回归。 |

---

## 与 Deep Agents 生态的关系

`langchain-repl` 位于 `libs/repl/`，与 `libs/deepagents/` 核心 SDK **并列**，供需要在 **会话中执行代码** 的场景选用：在应用侧将 `ReplMiddleware` 加入 `create_deep_agent(..., middleware=[...])` 一类的中间件列表即可（具体参数名以 SDK 文档为准）。

---

## 小结

`langchain-repl` 通过 **`Interpreter` + `ReplMiddleware`** 提供可组合的 REPL 执行能力；源码集中在 `langchain_repl/`，质量由 `libs/repl/tests/` 单元测试与快照测试保障。
