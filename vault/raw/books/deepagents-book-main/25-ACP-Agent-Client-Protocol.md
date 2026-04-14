# Agent Client Protocol（ACP）集成

## 文档来源与路径

| 类型 | 路径 |
|------|------|
| 包根目录 | `libs/acp/` |
| Python 包源码 | `libs/acp/deepagents_acp/` |
| 示例 | `libs/acp/examples/` |
| 测试 | `libs/acp/tests/` |
| 构建与依赖声明 | `libs/acp/pyproject.toml`、`libs/acp/uv.lock` |

---

## 概述

`libs/acp/` 为 Deep Agents 提供 **Agent Client Protocol（ACP）** 侧的服务端集成：在标准化协议之上，把 Deep Agent 的能力暴露给客户端，使「客户端—智能体」之间的会话、工具调用与消息流能够以统一方式交互。

仓库顶层 `AGENTS.md` 中将该目录记为协议相关能力；本包通过 PyPI 依赖 `agent-client-protocol` 使用官方 ACP 协议实现（见 `pyproject.toml` 中的 `agent-client-protocol`）。

---

## 包与构建

- **发行包名**：`deepagents-acp`（`pyproject.toml` 中 `[project].name`）。
- **构建后端**：Hatchling（`[build-system]` 中 `hatchling.build`）。
- **可安装模块命名空间**：`deepagents_acp/`（与发行名中的连字符对应为下划线导入路径）。

### 设计取舍

- **独立子包**：ACP 与核心 SDK 解耦，便于单独版本化、单独测试，且依赖 `deepagents` 时通过 `[tool.uv.sources]` 指向可编辑的 `../deepagents`，符合 monorepo 本地开发习惯。
- **协议优先**：服务端逻辑集中在 `server.py`，与 `acp` 库的 schema、会话生命周期 API 对齐，减少自研协议分叉。

---

## 运行方式

可通过模块入口直接启动（对应 `deepagents_acp/__main__.py`）：

```bash
python -m deepagents_acp
```

`__main__.py` 调用 `server` 中的 `_serve_test_agent()`，用于拉起可演示/可测试的 ACP 服务端行为。

---

## 模块关系（核心文件）

| 模块 / 文件 | 职责 |
|-------------|------|
| `deepagents_acp/__init__.py` | 包说明与对外符号（当前以包级文档字符串为主）。 |
| `deepagents_acp/__main__.py` | CLI/模块运行入口，`main()` → 异步服务。 |
| `deepagents_acp/server.py` | ACP 服务端实现：对接 `acp` 库的 Agent、会话、工具调用与 Deep Agents 的 `create_deep_agent`、后端组合等。 |
| `deepagents_acp/utils.py` | 服务端辅助逻辑。 |

**与上游的关系**：`server.py` 依赖 `deepagents.create_deep_agent` 以及 `deepagents.backends`（如 `CompositeBackend`、`FilesystemBackend`、`StateBackend`），将 Deep Agents 图编译结果接入 ACP 的消息与工具协议。

---

## 示例与测试

- **示例**（`libs/acp/examples/`）：如 `demo_agent.py`、`local_context.py`，展示如何结合本地上下文或演示代理使用 ACP 集成。
- **测试**（`libs/acp/tests/`）：覆盖主流程、工具、模型切换、命令白名单、危险模式检测等（如 `test_main.py`、`test_agent.py`、`test_model_switching.py` 等）。

---

## 小结

`deepagents-acp` 把 Deep Agents **嵌入 ACP 服务端角色**，客户端按协议连接即可获得统一的智能体会话体验；源码以 `deepagents_acp.server` 为枢纽，示例与测试分别位于 `examples/` 与 `tests/`。
