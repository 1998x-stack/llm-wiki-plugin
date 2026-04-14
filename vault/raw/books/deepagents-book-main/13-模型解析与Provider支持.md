# 模型解析与 Provider 支持（`_models.py`）

**源码路径：** `libs/deepagents/deepagents/_models.py`

---

## 1. 模块定位

本模块提供 Deep Agents 共用的 **模型字符串解析**、**OpenRouter 版本与归因**、以及 **模型实例与 `provider:model` 规格比对** 等工具函数，供 SDK、`create_summarization_tool_middleware`、CLI 配置等复用。

---

## 2. `resolve_model(model: str | BaseChatModel) -> BaseChatModel`

### 2.1 行为摘要

1. **已是 `BaseChatModel`：** 原样返回。
2. **以 `openai:` 为前缀：** `init_chat_model(model, use_responses_api=True)`，即 OpenAI 路径下 **默认走 Responses API**。
3. **以 `openrouter:` 为前缀：** 先 `check_openrouter_version()`，再 `init_chat_model(model, **_openrouter_attribution_kwargs())`。
4. **其他字符串：** `init_chat_model(model)`，由 LangChain 根据字符串 **自动推断 provider**。

### 2.2 代码骨架

```72:96:libs/deepagents/deepagents/_models.py
def resolve_model(model: str | BaseChatModel) -> BaseChatModel:
    """Resolve a model string to a `BaseChatModel`.

    If `model` is already a `BaseChatModel`, returns it unchanged.

    String models are resolved via `init_chat_model`. OpenAI models
    (prefixed with `openai:`) default to the Responses API.

    OpenRouter models include default app attribution headers unless overridden
    via `OPENROUTER_APP_URL` / `OPENROUTER_APP_TITLE` env vars.
    ...
    """
    if isinstance(model, BaseChatModel):
        return model
    if model.startswith("openai:"):
        return init_chat_model(model, use_responses_api=True)
    if model.startswith("openrouter:"):
        check_openrouter_version()
        return init_chat_model(model, **_openrouter_attribution_kwargs())
    return init_chat_model(model)
```

---

## 3. OpenRouter 集成

### 3.1 最低版本

- 常量 **`OPENROUTER_MIN_VERSION = "0.2.0"`**（`langchain-openrouter`）。
- **`check_openrouter_version()`：** 若已安装包且版本 **低于** 该值，抛出 `ImportError` 并提示升级命令；若包未安装则跳过（后续由 `init_chat_model` 暴露缺失依赖错误）。

### 3.2 默认归因（App Attribution）

OpenRouter 建议通过 HTTP 头做应用归因（参见 [OpenRouter 文档](https://openrouter.ai/docs/app-attribution)）。本模块默认：

- **`app_url`：** `https://github.com/langchain-ai/deepagents`（对应 `HTTP-Referer` 类用途）
- **`app_title`：** `Deep Agents`（对应 `X-Title` 类用途）

### 3.3 环境变量覆盖

`_openrouter_attribution_kwargs` 仅在 **未设置** 对应环境变量时注入上述默认值：

- **`OPENROUTER_APP_URL`**：若已设置，不覆盖用户的 `app_url`。
- **`OPENROUTER_APP_TITLE`**：若已设置，不覆盖用户的 `app_title`。

这样显式构造参数 > 环境变量 > 本模块默认值 的优先级链与 `ChatOpenRouter.from_env()` 行为相容。

---

## 4. 辅助函数

### 4.1 `get_model_identifier(model: BaseChatModel) -> str | None`

- 通过 `model.model_dump()` 读取序列化配置，在 **`model_name`** 或 **`model`** 键上取非空字符串。
- **动机：** 各 provider 对「模型 ID 字段名」不统一，避免仅靠反射属性。

### 4.2 `model_matches_spec(model: BaseChatModel, spec: str) -> bool`

- 先取 `get_model_identifier`；若为 `None` 则不匹配。
- **`spec` 与 identifier 完全相等** → 匹配。
- 否则将 `spec` 按 **首个 `:`** 分割为 `provider` 与 `model_name`；若存在分隔符且 **`model_name` 与 identifier 相等**，也视为匹配（例如 `"openai:gpt-5"` 与 identifier `"gpt-5"`）。

**约定：** 项目内广泛使用 **`provider:model`** 单冒号形式的字符串规格。

---

## 5. 设计决策小结

| 主题 | 决策 |
|------|------|
| OpenAI 前缀 | 默认 `use_responses_api=True`，与 OpenAI 新 API 路径对齐 |
| OpenRouter | 强制最低包版本 + 默认归因，且尊重用户环境变量 |
| 标识符提取 | 走 `model_dump()`，兼容多 provider 字段名 |
| 规格匹配 | 支持完整 spec 或仅模型名与实例 identifier 对齐 |

---

## 6. 在仓库中的调用关系（示例）

- **`create_summarization_tool_middleware`**：当 `model` 为字符串时 `from deepagents._models import resolve_model`。
- **CLI / 配置**：可与 `OPENROUTER_MIN_VERSION`、`check_openrouter_version` 共享同一版本底线（模块注释中提及 CLI `config.py`）。

---

## 7. 依赖

- `langchain.chat_models.init_chat_model`
- `langchain_core.language_models.BaseChatModel`
- `packaging.version.Version`（版本比较）
- `importlib.metadata.version` / `PackageNotFoundError`（OpenRouter 包检测）
