# 第 23 章：Terminal Bench 2.0 评估

> **主要参考源码路径**  
> - `libs/evals/README.md`（Terminal Bench 2.0、运行方式、LangSmith 工作流、失败模式表）  
> - `libs/evals/Makefile`（`run-terminal-bench-*` 目标与并发参数）  
> - `libs/evals/deepagents_harbor/deepagents_wrapper.py`（Harbor 智能体入口）  
> - `libs/evals/scripts/harbor_langsmith.py`（LangSmith CLI）

---

## 1. Terminal Bench 2.0 是什么

[Terminal Bench 2.0](https://github.com/laude-institute/terminal-bench-2) 是一个 **终端/计算机使用向** 的智能体评测基准，覆盖 **90+** 个任务，用于衡量智能体在 **真实或接近真实的命令行环境** 中 **理解任务、操作仓库、运行构建与测试、调试失败** 的综合能力。

### 1.1 领域与难度跨度

任务横跨 **软件工程、生物信息、安全、游戏** 等多个领域；同一套 harness 下，既有「写脚本即可」的小任务，也有需要 **多步推理、长链路工具调用与环境状态依赖** 的硬任务。

### 1.2 示例任务（README 与社区描述一致）

| 任务标识（示例） | 考察点（概括） |
|------------------|----------------|
| `path-tracing` | 从渲染图像 **反推/还原 C 程序** 一类逆向与实现能力 |
| `chess-best-move` | 调用棋类引擎或环境，求 **最优着法** |
| `git-multibranch` | **多分支 Git 操作**、合并冲突处理等版本控制实战 |
| `sqlite-with-gcov` | **构建 SQLite**、开启 gcov、分析覆盖率报告等工程链路 |

具体指令与 verifier 以 Harbor 下发的任务包为准；上表用于理解 **基准在测什么类型的「终端智能」**。

---

## 2. 在 Deep Agents 仓库中如何运行

工作目录建议为 **`libs/evals/`**（与 README、`Makefile` 一致）。需配置 **模型 API**（如 `ANTHROPIC_API_KEY`）与 **LangSmith 追踪**（`LANGSMITH_API_KEY`、`LANGSMITH_TRACING=true`）等；使用 Daytona 等云沙箱时再配置对应 API Key。

### 2.1 直接使用 `harbor run`

**Docker（本地、顺序 slot，README 示例 `-n 1`）**：

```bash
uv run harbor run --agent-import-path deepagents_harbor:DeepAgentsWrapper \
  --dataset terminal-bench@2.0 -n 1 --jobs-dir jobs/terminal-bench --env docker
```

**Daytona（云沙箱，可提高并发；README 示例 `-n 10`）**：

```bash
uv run harbor run --agent-import-path deepagents_harbor:DeepAgentsWrapper \
  --dataset terminal-bench@2.0 -n 10 --jobs-dir jobs/terminal-bench --env daytona
```

说明：

- **`-n`**：Harbor 侧的 **并发 trial 槽位数**（并行沙箱数量），**不是**「只跑前 n 个任务」；限制任务数量应使用 Harbor 的 **`-l N`**（README 注明）。
- **`--jobs-dir`**：job 输出根目录（含各次运行的 trial 子目录），后续 **分析脚本与 `add-feedback` 路径** 都依赖此结构。

### 2.2 Makefile 快捷目标

`libs/evals/Makefile` 封装了常用环境；注意 **各目标的默认并发与后端不同**：

| 目标 | 环境 | 默认 `-n`（并发槽） |
|------|------|---------------------|
| `make run-terminal-bench-docker` | `docker` | 1 |
| `make run-terminal-bench-daytona` | `daytona` | **40** |
| `make run-terminal-bench-modal` | `modal` | 4 |
| `make run-terminal-bench-runloop` | `runloop` | 10 |

本地调试可优先 **Docker + 小 `-n`**；大规模跑分可在 **Daytona / Modal** 上提高并发，但需权衡 **成本、配额与失败重试**。

`AGENT_MODE` 默认为 `cli`；通过 `AGENT_KWARG` 传入 `use_cli_agent` 与 CI 默认的 SDK 模式对齐。

---

## 3. 可用沙箱环境一览

Harbor `--env` 常见取值（与 README 一致）：

| 值 | 适用场景 |
|----|----------|
| `docker` | 本机 Docker，适合复现与调试 |
| `daytona` | Daytona 云沙箱，需 `DAYTONA_API_KEY` |
| `modal` | Modal 云端算力 |
| `runloop` | Runloop 沙箱 |

选择环境是 **「评测可信度 vs 成本/速度」** 的权衡：本地 Docker 更易排错，云环境更适合 **高并行 sweep**。

---

## 4. LangSmith 工作流（与 Harbor 奖励对齐）

整体链路：**Deep Agents → Harbor 评测 → LangSmith 追踪与分析 → 迭代提示词/工具/模型**。

### 4.1 创建数据集

从 Harbor registry 拉取任务定义，在 LangSmith 中生成与指令对齐的 examples（实现见 `deepagents_harbor/langsmith.py`）：

```bash
python scripts/harbor_langsmith.py create-dataset terminal-bench --version 2.0
```

### 4.2 创建实验会话

```bash
python scripts/harbor_langsmith.py create-experiment terminal-bench --name deepagents-baseline-v1
```

脚本会在标准输出打印 **实验名与对比 URL**（stdout 约定两行，供自动化解析）。

### 4.3 带追踪运行

将实验名设为环境变量，使 `DeepAgentsWrapper` 用 `langsmith.trace` 包裹运行：

```bash
set LANGSMITH_EXPERIMENT=deepagents-baseline-v1
make run-terminal-bench-daytona
```

（Linux/macOS 使用 `export`。）亦可在开发阶段改用 `LANGSMITH_PROJECT` 指向固定项目，获得更简单的项目视图（README 选项说明）。

### 4.4 回写 Harbor 奖励到 LangSmith

评测结束后，把各 trial 的 **`result.json` 奖励** 写成 Feedback **`harbor_reward`（0.0～1.0）**：

```bash
python scripts/harbor_langsmith.py add-feedback jobs/terminal-bench/2025-12-02__16-25-40 --project-name deepagents-baseline-v1
```

`--project-name` 须与 LangSmith 中存放该次追踪的 **项目名** 一致（与 README 中「实验名作为项目视图」的用法对齐；若以 `LANGSMITH_EXPERIMENT` 运行，通常传入同名实验名）。

---

## 5. Deep Agent harness：经 Terminal Bench 验证的默认模式

README 将下列四点总结为 **跨任务表现较好的默认组合**（与 SDK / CLI harness 设计理念一致）：

1. **细致的系统提示（Detailed System Prompt）**  
   明确工作目录、工具使用边界、何时列目录、何时测试等，减少 **无目的探索**。

2. **规划中间件（Planning Middleware，`write_todos`）**  
   把长链路任务拆成可勾选步骤，降低 **跳步实现与遗忘约束** 的概率。

3. **文件系统工具（Filesystem tools）**  
   `ls` / `read_file` / `write_file` / `edit_file` / `glob` / `grep` 等，支持 **大代码库导航与增量修改**。

4. **子智能体（SubAgents，`task` 工具）**  
   将子任务隔离在独立上下文中，减轻 **主线程上下文污染** 与 **工具调用纠缠**。

在 Harbor 集成中，CLI 模式会 **关闭** CLI 自有的 shell/skills/memory 部分能力，由 **`HarborSandbox` 提供执行与文件语义**；上述设计仍体现在 **默认工具组合与系统提示策略** 上。

---

## 6. 常见失败模式（README 归纳）

下列模式来自 `libs/evals/README.md` 的运维与排错经验，适合作为 **看轨迹时的检查清单**：

| 模式 | 典型症状 | 可能改进方向 |
|------|----------|--------------|
| **规划不足（Poor Planning）** | 未读需求直接改代码 | 提示词要求 **先复述目标与计划** 再动手 |
| **工具使用不当（Incorrect Tool Usage）** | 滥用 `bash cat` 而非 `read_file` | 强化 **工具说明与正反例** |
| **缺少增量测试（No Incremental Testing）** | 一次大改后才发现失败 | 要求 **每完成一小步就运行测试/检查** |
| **路径幻觉（Hallucinated Paths）** | 未确认文件存在就读取 | 规则化：**先 `ls` / `glob` 再 `read_file`** |
| **模型错配（Wrong Model）** | 复杂推理持续失败 | 对硬任务 **升级模型** 或 **拆分子任务** |

---

## 7. 本章与源码的对应关系

- **「跑起来」**：`Makefile` 的 `run-terminal-bench-*` + Harbor CLI；智能体类 **`deepagents_harbor:DeepAgentsWrapper`**。  
- **「可对齐 LangSmith」**：`scripts/harbor_langsmith.py` + `deepagents_harbor/langsmith.py`。  
- **「事后分析」**：第 24 章的 `scripts/analyze.py` 与 `failure` / `stats` 模块。

Terminal Bench 2.0 在工程上的价值，不仅是 **分数**，更是 **可复现的失败样本** 与 **ATIF 轨迹**，为 Deep Agents 的默认 harness 提供 **回归基线**。
