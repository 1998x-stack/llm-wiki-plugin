# Hermes Agent 深度解析 · 第二篇：三层架构与 AIAgent 核心循环

> **系列导读**：本篇深入 Hermes Agent 的工程骨架——三层分离架构、同步 AIAgent 循环、三种 API 模式，以及覆盖 48 工具 / 40 工具集的执行体系。

---

## 一、宏观架构：三层分离设计

Hermes 的整体架构遵循严格的三层分离原则：

```
┌─────────────────────────────────────────────────────────────────┐
│                         入口层（Entry Points）                    │
│                                                                  │
│   CLI (cli.py)    Gateway (gateway/run.py)    ACP (acp_adapter/) │
│   Batch Runner    API Server                  Python Library      │
└──────────┬──────────────────┬────────────────────┬──────────────┘
           │                  │                    │
           ▼                  ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      核心层（AIAgent）                            │
│                      run_agent.py                                │
│                                                                  │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│   │ Prompt        │  │ Provider     │  │ Tool         │         │
│   │ Builder       │  │ Resolution   │  │ Dispatch     │         │
│   │ prompt_       │  │ runtime_     │  │ model_       │         │
│   │ builder.py    │  │ provider.py  │  │ tools.py     │         │
│   └──────┬────────┘  └──────┬───────┘  └──────┬───────┘        │
│          │                  │                  │                 │
│   ┌──────┴───────┐  ┌───────┴──────┐  ┌───────┴──────┐        │
│   │ Compression  │  │  3 API Modes │  │ Tool Registry│        │
│   │ & Caching    │  │  chat_compl  │  │ registry.py  │        │
│   │              │  │  codex_resp  │  │  48 tools    │        │
│   │              │  │  anthropic   │  │  40 toolsets │        │
│   └──────────────┘  └──────────────┘  └──────────────┘        │
└──────────────────────────────────────────┬──────────────────────┘
                                           │
           ┌───────────────────────────────┴─────────────────────┐
           ▼                                                       ▼
┌────────────────────┐                          ┌─────────────────────────┐
│   持久化层          │                          │  执行后端层              │
│ Session Storage    │                          │  Terminal (6 backends)  │
│ SQLite + FTS5      │                          │  Browser (5 backends)   │
│ hermes_state.py    │                          │  Web (4 backends)       │
│ gateway/session.py │                          │  MCP (dynamic)          │
└────────────────────┘                          │  File, Vision, etc.     │
                                                └─────────────────────────┘
```

---

## 二、代码规模：一个认真的工程项目

Hermes 的代码量说明这是一个成熟的工程项目，而非玩具 Demo：

| 文件 | 功能 | 代码量 |
|---|---|---|
| `run_agent.py` | AIAgent 核心会话循环 | ~9,200 行 |
| `cli.py` | HermesCLI 交互终端 UI | ~8,500 行 |
| `gateway/run.py` | GatewayRunner 消息分发 | ~7,500 行 |
| `hermes_cli/main.py` | 所有 `hermes` 子命令 | ~5,500 行 |
| `hermes_cli/setup.py` | 交互式安装向导 | ~3,100 行 |
| `tools/mcp_tool.py` | MCP 客户端实现 | ~2,200 行 |
| `tests/` | Pytest 测试套件 | ~3,000+ 测试 |

---

## 三、目录结构全景

```
hermes-agent/
├── run_agent.py              # ★ AIAgent 核心循环（~9,200 行）
├── cli.py                    # HermesCLI 交互终端
├── model_tools.py            # 工具发现、Schema 收集、分发
├── toolsets.py               # 工具集分组和平台预设
├── hermes_state.py           # SQLite 会话/状态库（含 FTS5）
├── hermes_constants.py       # HERMES_HOME、Profile 路径
├── batch_runner.py           # 批量轨迹生成
│
├── agent/                    # Agent 内部模块
│   ├── prompt_builder.py     # System Prompt 组装
│   ├── context_compressor.py # 上下文压缩算法
│   ├── prompt_caching.py     # Anthropic Prompt Cache
│   ├── auxiliary_client.py   # 辅助 LLM（视觉/摘要任务）
│   ├── model_metadata.py     # 模型上下文长度、Token 估算
│   ├── anthropic_adapter.py  # Anthropic Messages API 格式转换
│   ├── display.py            # KawaiiSpinner，工具预览格式化
│   ├── skill_commands.py     # Skill 斜杠命令
│   ├── memory_manager.py     # 记忆管理器编排
│   └── trajectory.py        # 轨迹保存工具
│
├── hermes_cli/               # CLI 子命令和配置
│   ├── main.py               # 所有 hermes 子命令入口
│   ├── config.py             # DEFAULT_CONFIG、迁移逻辑
│   ├── commands.py           # COMMAND_REGISTRY —— 斜杠命令定义中心
│   ├── auth.py               # PROVIDER_REGISTRY、凭证解析
│   ├── runtime_provider.py   # Provider → api_mode + 凭证
│   ├── models.py             # 模型目录、供应商模型列表
│   └── plugins.py            # PluginManager —— 发现、加载、Hooks
│
├── tools/                    # 工具实现（每个工具一个文件）
│   ├── registry.py           # 工具注册中心
│   ├── terminal_tool.py      # 终端编排
│   ├── file_tools.py         # read_file / write_file / patch / search_files
│   ├── web_tools.py          # web_search / web_extract
│   ├── browser_tool.py       # 11 个浏览器自动化工具
│   ├── code_execution_tool.py # execute_code 沙盒
│   ├── delegate_tool.py      # 子 Agent 委派
│   ├── mcp_tool.py           # MCP 客户端（~2,200 行）
│   └── environments/         # 终端后端实现
│       ├── local.py
│       ├── docker.py
│       ├── ssh.py
│       ├── modal.py
│       ├── daytona.py
│       └── singularity.py
│
├── gateway/                  # 消息平台网关
│   └── platforms/            # 15 个平台适配器
│
├── acp_adapter/              # ACP 服务（VS Code / Zed / JetBrains）
├── cron/                     # 调度器（jobs.py / scheduler.py）
├── plugins/memory/           # 记忆 Provider 插件
├── environments/             # RL 训练环境（Atropos）
├── skills/                   # 内置 Skills（始终可用）
└── optional-skills/          # 官方可选 Skills（需显式安装）
```

---

## 四、AIAgent 核心循环详解

### 循环结构

`run_agent.py` 中的 `AIAgent` 类是整个系统的心脏，实现一个**同步编排引擎**：

```python
# 简化的循环逻辑（概念示意，非原始代码）
class AIAgent:
    def run_conversation(self, user_message):
        # 1. 组装 System Prompt
        system_prompt = prompt_builder.build_system_prompt(
            soul=self.soul_md,
            memory=self.memory.load(),
            user_profile=self.user_md.load(),
            skills_list=self.skills.level0_list(),
            context_files=self.context_files.load(),
            tools_info=self.toolsets.active_tools(),
        )
        
        # 2. 解析 Provider
        provider = runtime_provider.resolve(self.config)
        
        # 3. 主执行循环（含 IterationBudget）
        while not done and iteration < budget:
            response = provider.call(
                system=system_prompt,
                messages=self.conversation_history,
            )
            
            if response.has_tool_calls:
                # 4. 工具执行
                for call in response.tool_calls:
                    result = model_tools.handle_function_call(call)
                    self.conversation_history.append(result)
                # 继续循环
            else:
                # 5. 最终响应
                done = True
        
        # 6. 持久化到 SessionDB
        self.state.save_session(self.conversation_history)
        return response.final_text
```

### IterationBudget（迭代预算）

`IterationBudget` 是防止 Agent 无限循环的安全机制。它跟踪：
- 当前迭代次数
- 总 Token 消耗
- 工具调用次数

当任何一个指标超出阈值，循环优雅终止并返回当前进度。

---

## 五、三种 API 模式

Hermes 支持三种 API 调用模式，对应不同的供应商和用例：

### 模式 1：`chat_completions`（最广泛）

```
适用：OpenAI、OpenRouter、Kimi、MiniMax、GLM、本地 Ollama 等
格式：OpenAI Chat Completions API 标准格式
特点：兼容性最广，200+ 模型均支持
```

### 模式 2：`codex_responses`（OpenAI 新格式）

```
适用：OpenAI Responses API
格式：新版 Responses API 格式
特点：支持 OpenAI 的最新功能（如 Reasoning tokens）
```

### 模式 3：`anthropic_messages`（Anthropic 原生）

```
适用：Claude 系列（通过 Anthropic 直连）
格式：Anthropic Messages API 原生格式
特点：支持 Prompt Caching、Extended Thinking、文档类型等 Claude 独有功能
```

切换方式：`hermes model` —— 无需更改任何应用代码，运行时动态解析。

---

## 六、工具体系：48 工具 + 40 工具集

### 工具注册机制

工具在 **导入时自动注册**，通过 `tools/registry.py` 统一管理：

```python
# 注册原理（概念示意）
@register_tool
def web_search(query: str, ...) -> str:
    """搜索网络，返回结果摘要。"""
    ...
```

`model_tools.py` 提供：
- `get_tool_definitions()` —— 收集所有工具的 JSON Schema，传给 LLM
- `handle_function_call(call)` —— 根据工具名分发执行

### 工具分类总览

| 类别 | 工具数量 | 代表工具 |
|---|---|---|
| 终端执行 | 6 | `terminal`（6 种后端） |
| 文件操作 | 4 | `read_file` / `write_file` / `patch` / `search_files` |
| 网络搜索 | 4 | `web_search` / `web_extract` / `web_fetch` / `web_screenshot` |
| 浏览器自动化 | 11 | `browser_navigate` / `browser_click` / `browser_fill` 等 |
| 代码执行沙盒 | 1 | `execute_code`（Python RPC，零上下文成本） |
| 子 Agent 委派 | 1 | `delegate_task` |
| 记忆管理 | 1 | `memory`（add / replace / remove） |
| Skills 管理 | 3 | `skills_list` / `skill_view` / `skill_create` |
| MCP 客户端 | 动态 | 来自连接的 MCP Server |
| 视觉 / 图像 | 若干 | `vision_analyze` / `image_generate` |
| 语音 | 若干 | TTS / STT（Voice Mode） |

### 工具集（Toolset）系统

工具集是一组工具的逻辑集合，40 个 Toolset 覆盖不同场景：

```bash
hermes tools list              # 查看所有可用工具
hermes tools enable web        # 启用 web 工具集
hermes tools disable browser   # 禁用 browser 工具集

# 在 chat 时按需指定工具集
hermes chat --toolsets terminal,web,skills
```

**不同场景的典型工具集配置：**

| 场景 | 推荐工具集 |
|---|---|
| 通用编程助手 | `terminal` + `file` + `web` |
| 网络研究 | `web` + `browser` |
| 数据分析 | `terminal` + `file` + `execute_code` |
| 消息平台 Agent | `terminal` + `skills` + `memory` |
| 最小化（节省 Token） | `skills` 仅 |

---

## 七、Prompt 组装系统

`prompt_builder.py` 负责将多个数据源组装成完整的 System Prompt：

```
System Prompt 组成（按注入顺序）
═══════════════════════════════════════════════════════
1. SOUL.md              → Agent 人格和行为准则
2. MEMORY.md            → 环境事实（冻结快照）
3. USER.md              → 用户档案（冻结快照）
4. Skills Level 0       → 技能名称+描述目录（~3k tokens）
5. Context Files        → AGENTS.md 等项目上下文文件
6. Active Tools Info    → 当前会话可用工具的说明
7. Current Date/Time    → 时间感知
8. Platform Metadata    → 当前运行平台（CLI / Telegram / ...）
═══════════════════════════════════════════════════════
```

**关键设计原则：冻结快照（Frozen Snapshot）**

MEMORY.md 和 USER.md 在会话开始时捕获一次，整个会话期间不变。这不是疏忽，而是**为了保护 LLM 的 KV Cache**。记忆文件在磁盘上实时更新，但下一次会话才会进入 Prompt。

---

## 八、上下文压缩与 Prompt 缓存

### 上下文压缩（Context Compression）

当会话历史增长到接近模型上下文窗口上限时，`context_compressor.py` 自动触发：

```
原始历史消息（长）
        ↓
识别可压缩的工具输出（通常是最冗长的部分）
        ↓
LLM 摘要压缩（辅助 LLM，不影响主流程）
        ↓
压缩后历史（短）→ 继续会话
```

压缩是递增的，优先压缩最早的、内容最冗余的工具输出，保留最近的消息完整。

### Prompt 缓存（Anthropic 专属）

`prompt_caching.py` 为 Anthropic API 模式实现前缀缓存：

- 标记 System Prompt 中的稳定前缀（SOUL.md + MEMORY.md + USER.md）
- 后续调用命中缓存，Token 成本大幅降低
- 对于长期运行的 Agent，累积节省极为可观

---

## 九、三条数据流完整追踪

### 数据流 A：CLI 会话

```
用户在终端输入消息
        ↓
HermesCLI.process_input()
        ↓ 解析斜杠命令 / 普通消息
AIAgent.run_conversation()
        ↓
prompt_builder.build_system_prompt()  ← 注入 SOUL / 记忆 / Skills
        ↓
runtime_provider.resolve_runtime_provider()  ← 选择 API 模式
        ↓
API 调用（三种模式之一）
        ↓
有工具调用？ → model_tools.handle_function_call() → 继续循环
没有？       → 最终响应
        ↓
display.render()  ← KawaiiSpinner / 工具预览格式化
        ↓
hermes_state.save_session()  ← 持久化到 SQLite
```

### 数据流 B：Gateway 消息

```
平台消息到达（如 Telegram）
        ↓
Adapter.on_message()  ← 平台特定适配器
        ↓
MessageEvent 标准化
        ↓
GatewayRunner._handle_message()
        ↓
用户授权验证（pairing.py）
        ↓
解析会话 Key（platform + user_id）
        ↓
从 SessionStore 加载历史消息
        ↓
创建 AIAgent（注入会话历史）
        ↓
AIAgent.run_conversation()
        ↓
delivery.send()  ← 通过适配器发回响应
```

### 数据流 C：Cron 定时任务

```
调度器 tick（cron/scheduler.py）
        ↓
从 jobs.json 加载到期任务
        ↓
创建全新 AIAgent（无历史，每次独立）
        ↓
注入任务附加的 Skills 作为上下文
        ↓
运行任务提示词
        ↓
delivery.send()  ← 投递到配置的目标平台
        ↓
更新 next_run 时间戳
```

---

## 十、小结

Hermes 的架构设计有几个值得关注的工程决策：

1. **同步编排引擎**：AIAgent 是单线程同步循环，而非异步事件驱动。这简化了状态管理，代价是单任务阻塞，多任务通过子 Agent 委派解决。

2. **入口层统一但不耦合**：CLI、Gateway、ACP、Batch Runner 四个入口都最终调用同一个 `AIAgent.run_conversation()`，但各自管理会话生命周期。

3. **工具在导入时注册**：利用 Python 模块加载机制实现工具的自动发现，无需手工维护工具列表。

4. **冻结快照保护缓存**：记忆系统的"不一致性"（会话内记忆更新但 Prompt 不变）是刻意权衡，换取的是 LLM 前缀缓存命中率。

5. **三种 API 模式共存**：不强迫所有供应商适配同一接口，而是为三种主流格式分别实现适配器。

---

*下一篇：[第三篇：分层记忆系统 —— MEMORY.md / USER.md / FTS5 跨会话召回](./03_hermes_memory.md)*

*基于 2026 年 4 月版本 · GitHub: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)*
