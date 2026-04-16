---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [AI, 方法论, AI工程]
aliases:
- Trajectory Schema
- 轨迹 Schema
- .traj 格式
relates_to:
- target: "[[SWE-agent]]"
  type: implements
  confidence: 0.95
- target: "[[Agent 轨迹分析]]"
  type: uses
  confidence: 0.9
- target: "[[ReAct 风格循环]]"
  type: depends_on
  confidence: 0.85
supersedes: null
---

# Trajectory Schema

## 概述

Trajectory Schema 是 [[SWE-agent]] 定义的 Agent 运行轨迹数据结构（`.traj` 文件），记录每轮 thought/action/observation 的完整交互序列，用于事后分析、调试和复现。

## 关键内容

### 顶层字段

| 字段 | 含义 | 构造方式 |
|------|------|---------|
| `environment` | 运行环境标识（如 "swe_main"） | 初始化时从运行配置写入，run-level metadata |
| `trajectory` | 核心数组，存储每步交互记录 | 每完成一轮交互 append 一条记录 |

**建议补充的顶层工程化字段**：`instance_id`、`schema_version`、`run_id`、`agent_version`、`model_name`、`config_ref`、`info`。

### Step 级字段（trajectory[] 中每条记录）

#### 核心字段（官方支持）

| 字段 | 含义 | 构造方式 |
|------|------|---------|
| `response` | 模型原始输出（LM output） | 模型返回后原样保存，包含自然语言推理和动作文本 |
| `thought` | 从 response 解析出的"思考部分" | 用 action parser 按约定模板从 response 中抽取（如 ReAct 中 `Thought:` 后的文本） |
| `action` | 从 response 解析出的"动作部分"，实际执行的命令 | 由 parser 从 response 中抽取，标准化后传给环境执行器 |
| `observation` | 动作执行后的环境反馈 | 执行 action 后，把 stdout/stderr/工具返回值合成为字符串 |
| `state` | 动作执行后从环境抽取的状态 | 每轮完成后从环境对象读取关键状态（如 `open_file`、`working_dir`），序列化为 JSON |
| `query` | 当前 step 精确送给模型的输入消息列表 | 发模型请求前，把完整 messages 数组保存下来 |

#### 版本差异：message vs query

- **1.1.0 之前**：使用 `message` 字段，近似表示下一步输入
- **1.1.0 起**：改为 `query` 字段，表示当前 step 的精确输入
- **建议**：新写入只用 `query`，读取时同时兼容 `query` 和 `message`

#### 构造流水线（6 步）

1. **构造 query**：收集本轮发给模型的完整 messages
2. **拿到 response**：保存模型输出原文
3. **解析 thought 和 action**：按 action parser 规则拆分，失败时保留 response 并记录 parse_error
4. **执行动作，写入 observation**：交给环境执行器，反馈应 agent-friendly
5. **抽取环境状态，写入 state**：从环境对象拿关键状态
6. **append 到 trajectory**：落盘形成可复盘的轨迹

### 分析友好增强字段

**Step 级建议补充**：

| 字段 | 价值 |
|------|------|
| `step_id` | 步骤编号，便于定位 |
| `timestamp_start` / `timestamp_end` | 时间分析 |
| `parse_error` | 解析失败诊断 |
| `exit_code` | 命令执行状态 |
| `tool_name` / `tool_args` | 工具调用追踪 |
| `observation_type` | 反馈分类（shell_output / format_error / lint_error 等） |
| `cost` | 成本统计 |
| `tokens_prompt` / `tokens_completion` | Token 用量分析 |

### 实用 Schema 模板

```json
{
  "environment": "swe_main",
  "trajectory": [
    {
      "response": "Let's inspect the repository structure first...\nls -F",
      "thought": "Let's inspect the repository structure first...",
      "action": "ls -F\n",
      "observation": "AUTHORS.rst\nCHANGELOG.rst\nsrc/\ntests/\n",
      "state": "{\"open_file\": \"n/a\", \"working_dir\": \"/repo\"}",
      "query": [
        {"role": "system", "content": "You are a helpful assistant ..."},
        {"role": "user", "content": "Fix issue ..."}
      ]
    }
  ]
}
```

### 设计建议

1. **response 不要只存解析后的 thought/action**：response 对调 parser 错误、复盘格式错误、行为分析都非常重要。
2. **action 分两份存**：`action_raw`（模型原始给出的动作）和 `action`（经 parser/normalizer 后真正执行的动作）。
3. **observation 可拆细**：`observation_text`、`exit_code`、`observation_type`，更利于分析。
4. **state 推荐存对象而非 JSON 字符串**：解析更简单。
5. **query 是调试关键**：能回答"模型为什么会在这一步做出这个 response？"，没有它只能看结果无法复原输入条件。

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/08-trajectory常见字段 schema包含哪些，分别什么意思，分别如何构造.md]] — SWE-agent trajectory schema 详解

## 相关

- [[SWE-agent]] — implements（定义此 schema 的 Agent 系统）
- [[Agent 轨迹分析]] — uses（基于此 schema 进行轨迹分析）
- [[ReAct 风格循环]] — depends_on（schema 结构反映 ReAct 循环的 thought/action/observation 模式）
