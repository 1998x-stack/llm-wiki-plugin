---
type: concept
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 9
tags: [AI, Agent, 评估, LangSmith, 测试, Agent系统]
aliases: [deepagents evals, Agent评估框架, TrajectoryScorer]
relates_to:
  - target: "[[DeepAgents]]"
    type: part_of
    confidence: 0.95
  - target: "[[LLM-as-Judge]]"
    type: related_to
    note: LLMJudge 是 SuccessAssertion 的一种实现
    confidence: 0.95
supersedes: null
---

# DeepAgents 评估体系

## 概述

[[DeepAgents]] 的评估框架（`libs/evals/`），基于 pytest + LangSmith，将 Agent 一次运行表示为结构化"轨迹"（trajectory），用**两层断言模型**区分"对错"（成功断言，硬性失败）与"形态"（效率断言，仅记录不报红）。内置 7 个评估维度、外部基准测试集成（F[[rust-analyzer|RA]]MES/Nexus/BFCL v3/tau2-bench）、Harbor 框架和 Terminal Bench 2.0。

## 关键内容

### 两层断言模型（核心设计）

| 层 | 类型 | 语义 | 失败行为 |
|--|--|--|--|
| 成功断言（Success Assertions） | `SuccessAssertion` | 正确性检查 | `pytest.fail` 测试红 |
| 效率断言（Efficiency Assertions） | `EfficiencyAssertion` | 步数/工具调用形态期望 | LangSmith `log_feedback` 记录，测试不红 |

**设计意图**：防止 Agent 因探索性多走一步就整例标红，同时仍能在报表中观察效率偏差。

### 核心类型（`utils.py`）

**`AgentStep`**：`index`（从1起）、`action`（`AIMessage`）、`observations`（`list[ToolMessage]`）——一个决策回合。

**`AgentTrajectory`**：`steps` + `files`（路径→内容映射），`answer` 属性取最后一步文本，`pretty()` 生成人类可读摘要（供 [[LLM-as-Judge|LLM Judge]] 消费）。

**`TrajectoryScorer`**（不可变建造者）：
```python
scorer = (
    TrajectoryScorer()
    .expect(agent_steps=2, tool_call_requests=1)   # 效率断言（仅记录）
    .success(final_text_contains("three"))          # 成功断言（硬失败）
)
```

### 内置成功断言工厂

- `final_text_contains(substring, case_insensitive=False)` — 最终回复包含子串
- `file_equals(path, content)` — 文件内容等于预期
- `llm_judge(*criteria, judge_model=..., include_tool_calls=False)` — [[LLM-as-Judge]] 语义评分

### 入口函数 `run_agent`

1. 组装 `query` + `initial_files` → `agent.invoke`
2. 用 `thread_id` 生成轨迹（`AgentTrajectory`）
3. LangSmith 记录规范化 inputs/outputs
4. 执行 `_assert_[[期望值|expectation]]s`：先记录效率 feedback，再逐项运行成功断言

### 评估分类（`categories.json`）

| 分类 | 说明 |
|------|------|
| `file_operations` | 文件读写操作能力 |
| `retrieval` | 信息检索能力 |
| `tool_use` | 工具选择与使用 |
| `memory` | 记忆调用与持久化 |
| `conversation` | 对话理解能力 |
| `summarization` | 上下文压缩能力 |
| `unit_test` | SDK 单元行为（不含在雷达图中） |

雷达图（Radar）使用前 6 个分类（排除 `unit_test`），避免 SDK 行为与"模型能力"维度混淆。

### pytest 配置（`conftest.py`）

- **LangSmith 追踪门禁**：`LANGSMITH_TR[[Agent计算机接口|ACI]]NG` 环境变量必须为 `"true"`，否则整个会话退出码 1
- CLI 参数：`--model`（被测模型）、`--eval-category`（筛选分类）、`--openrouter-provider`
- 所有 eval 用例使用 `@pytest.mark.langsmith`

### 外部基准集成

- **FRAMES**：事实性多跳问答
- **Nexus**：多工具调用场景
- **BFCL v3**：函数调用基准
- **tau2-bench**：客服/零售场景长对话

### Harbor 框架（`libs/evals/` Harbor 集成）

`[[DeepAgents]]Wrapper` 将 Deep Agent 包装为 Harbor 基准的统一接口；`HarborSandbox` 提供沙箱后端。失败分类工具自动标注错误类型（工具调用错误、规划失败、上下文溢出等），LangSmith 脚本聚合统计。

### Terminal Bench 2.0

90+ 真实终端任务基准，使用 LangSmith 工作流管理运行；含失败分类器与统计工具，可与雷达图联动分析。

### Harbor 分析工具链（`libs/evals/scripts/` + `deepagents_harbor/`）

**评测后数据闭环**：Harbor job 落盘 → `analyze.py` 本地汇总 → `add-feedback` 关联 LangSmith → 报表与文档再生。

**`scripts/analyze.py`（CLI 分析器）**：
- 扫描 `jobs/` trial 目录树，解析 `trajectory.json`（ATIF）、`result.json`、`exception.txt`
- 调用 `failure.py` 做失败归因，调用 `stats.py` 输出置信区间与 MDE
- 设计决策：退出码优先从 ATIF 结构化提取，避免对整段轨迹盲目正则导致误报

**`failure.py`——失败分类（`FailureCategory` 枚举）**：

| 类别 | 含义 |
|------|------|
| `CAPABILITY` | 模型能力/策略问题（无基础设施信号） |
| `INF[[rust-analyzer|RA]]_OOM` | exit 137 / OOM |
| `INF[[rust-analyzer|RA]]_TIMEOUT` | exit 124 / 超时 |
| `INF[[rust-analyzer|RA]]_SANDBOX` | 沙箱崩溃、网络不可达、exec failed |
| `UNKNOWN` | 有异常文本但无法归类 |

`is_infrastructure` 属性可在报表中剥离环境噪声，单独统计基础设施失败，避免污染模型能力评估。

**`stats.py`——统计严谨性**：
- **`wilson_ci(successes, total, z=1.96)`**：Wilson 置信区间，小样本或比例接近 0/1 时比正态近似更稳健（与 Anthropic 基础设施噪声研究建议一致）
- **`min_detectable_effect(total, z=1.96, p=0.5)`**：估计最小可检测效应（MDE）——若两次成功率差距 < MDE，可能无法与噪声区分。默认 `p=0.5` 取最保守基准，防止在 90 题级别上对 1~2 题的涨跌过度解读

**`harbor_langsmith.py`——LangSmith 对齐子命令**：

| 子命令 | 作用 |
|--------|------|
| `create-dataset` | 从 Harbor 拉取任务，在 LangSmith 创建数据集和 examples |
| `ensure-dataset` | 若不存在则创建，否则打印已存在 |
| `create-experiment` | 创建绑定数据集的实验会话，stdout 输出名称与 URL |
| `add-feedback` | 遍历 trial，按 `trial_name` 元数据找根 run，写入 `harbor_reward`（0.0~1.0），并去重 |

`add-feedback` 要求恰好一条根 run 匹配（多条或无匹配均记错误），防止分数打到错误 trace。

**生成类脚本**：
- `generate_radar.py`：从 `evals_summary.json` 生成雷达图 PNG（`--toy` 支持离线预览）
- `generate_eval_catalog.py`：重写 `EVAL_CATALOG.md`，`--check` 用于 CI 防漂移
- `generate_model_groups.py`：从 `.github/scripts/models.py` 注册表生成 `MODEL_[[生成式推荐|GR]]OUPS.md`

**工程化建议**：先确保轨迹与 `result.json` 完整再跑分析；解读分数时同时看 `format_ci` 与 MDE，并将 `is_infrastructure=True` 的 trial 单独分层统计。

### 编写评估用例（五步流程）

1. 定义任务描述（query）与初始文件状态
2. 选择成功断言（子串 / 文件 / LLM Judge）
3. 可选添加效率期望
4. 标注 `eval_category` 标记
5. 考虑"漂移测试"（对比新旧模型版本行为差异）

## 来源
- [[raw/books/deepagents-book-main/17-评估体系架构总览.md]]
- [[raw/books/deepagents-book-main/18-评估报告与指标系统.md]]
- [[raw/books/deepagents-book-main/19-内置评估用例详解.md]]
- [[raw/books/deepagents-book-main/20-外部基准测试集成.md]]
- [[raw/books/deepagents-book-main/21-LLM-as-Judge评估模式.md]]
- [[raw/books/deepagents-book-main/22-Harbor框架集成.md]]
- [[raw/books/deepagents-book-main/23-Terminal-Bench-2.0评估.md]]
- [[raw/books/deepagents-book-main/24-Harbor分析与统计工具.md]]
- [[raw/books/deepagents-book-main/30-编写评估用例指南.md]]

## 相关
- [[DeepAgents]]
- [[LLM-as-Judge]]
- [[DeepAgents评估设计哲学]]
